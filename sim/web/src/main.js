// Duckbot simulátor v prohlížeči: MuJoCo (WASM) + three.js.
// Stejná technologie jako Microduck sandbox, ale bez politiky: serva drží
// cílové úhly ze sliderů PD regulátorem. Fyzika 200 Hz, řízení 50 Hz.

import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import loadMujoco from "@mujoco/mujoco";
import mujocoWasmUrl from "@mujoco/mujoco/mujoco.wasm?url";

const MODEL_URL = "/duckbot_hold.xml";
const DECIMATION = 4;

const $ = (id) => document.getElementById(id);

// ── MuJoCo ────────────────────────────────────────────────────────────
const mujoco = await loadMujoco({
  locateFile: (p) => (p.endsWith(".wasm") ? mujocoWasmUrl : p),
});
const xml = await (await fetch(MODEL_URL)).text();
const model = mujoco.MjModel.from_xml_string(xml);
const data = new mujoco.MjData(model);
const OBJ = mujoco.mjtObj;
const GEOM = mujoco.mjtGeom;

const trunkId = mujoco.mj_name2id(model, OBJ.mjOBJ_BODY.value, "trunk");
const nu = model.nu;
const jointNames = [];
const qposAdr = [];
const dofAdr = [];
for (let i = 0; i < nu; i++) {
  const name = mujoco.mj_id2name(model, OBJ.mjOBJ_ACTUATOR.value, i);
  const jid = mujoco.mj_name2id(model, OBJ.mjOBJ_JOINT.value, name);
  jointNames.push(name);
  qposAdr.push(model.jnt_qposadr[jid]);
  dofAdr.push(model.jnt_dofadr[jid]);
}
const defaultPose = Float64Array.from(model.key_ctrl.subarray(0, nu));
const gyroAdr = model.sensor("imu_ang_vel").adr;
const touchAdr = ["left_foot_contact", "right_foot_contact"].map((n) => model.sensor(n).adr);
const timestep = model.opt.timestep;

function setKp(kp) {
  for (let i = 0; i < nu; i++) {
    model.actuator_gainprm[i * 10] = kp;
    model.actuator_biasprm[i * 10 + 1] = -kp;
  }
}

function reset() {
  mujoco.mj_resetDataKeyframe(model, data, 0);
  mujoco.mj_forward(model, data);
  target.set(defaultPose);
  sliders.forEach((s, i) => s.set(defaultPose[i]));
  demo = null;
  simTime = 0;
  syncButtons();
}

// ── three.js ──────────────────────────────────────────────────────────
const canvas = $("canvas");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b0b0d);
scene.fog = new THREE.Fog(0x0b0b0d, 1.5, 4);

const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 20);
camera.up.set(0, 0, 1);
camera.position.set(0.45, -0.45, 0.28);
const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 0, 0.12);
controls.enableDamping = true;

scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const sun = new THREE.DirectionalLight(0xffffff, 1.6);
sun.position.set(0.6, -0.5, 1.2);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = sun.shadow.camera.bottom = -0.6;
sun.shadow.camera.right = sun.shadow.camera.top = 0.6;
sun.shadow.camera.near = 0.1;
sun.shadow.camera.far = 4;
scene.add(sun);
const fill = new THREE.DirectionalLight(0xffe0c0, 0.4);
fill.position.set(-0.5, 0.6, 0.8);
scene.add(fill);

function gridTexture() {
  const c = document.createElement("canvas");
  c.width = c.height = 512;
  const g = c.getContext("2d");
  g.fillStyle = "#101012";
  g.fillRect(0, 0, 512, 512);
  g.strokeStyle = "#2a2a30";
  g.lineWidth = 1;
  for (let i = 0; i <= 512; i += 64) {
    g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke();
    g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke();
  }
  g.strokeStyle = "#f58c1a";
  g.lineWidth = 2;
  g.strokeRect(0, 0, 512, 512);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(20, 20);
  t.anisotropy = 8;
  return t;
}

// Jedna three.js síť na každý MuJoCo geom; poloha se každý snímek přepíše
// z data.geom_xpos / geom_xmat. Kapsle a válce mají v MuJoCo osu Z, v three
// osu Y, proto rotace geometrie o 90° kolem X.
const meshes = [];
const alignZ = new THREE.Matrix4().makeRotationX(Math.PI / 2);
for (let g = 0; g < model.ngeom; g++) {
  const type = model.geom_type[g];
  const s = model.geom_size.subarray(g * 3, g * 3 + 3);
  const rgba = model.geom_rgba.subarray(g * 4, g * 4 + 4);
  let geometry, material;
  if (type === GEOM.mjGEOM_PLANE.value) {
    geometry = new THREE.PlaneGeometry(6, 6);
    material = new THREE.MeshStandardMaterial({ map: gridTexture(), roughness: 0.9 });
  } else {
    if (type === GEOM.mjGEOM_BOX.value) geometry = new THREE.BoxGeometry(2 * s[0], 2 * s[1], 2 * s[2]);
    else if (type === GEOM.mjGEOM_SPHERE.value) geometry = new THREE.SphereGeometry(s[0], 24, 16);
    else if (type === GEOM.mjGEOM_CAPSULE.value) {
      geometry = new THREE.CapsuleGeometry(s[0], 2 * s[1], 8, 20).applyMatrix4(alignZ);
    } else if (type === GEOM.mjGEOM_CYLINDER.value) {
      geometry = new THREE.CylinderGeometry(s[0], s[0], 2 * s[1], 24).applyMatrix4(alignZ);
    } else continue; // mesh/hfield tady nepoužíváme
    material = new THREE.MeshStandardMaterial({
      color: new THREE.Color(rgba[0], rgba[1], rgba[2]), roughness: 0.55, metalness: 0.05,
    });
  }
  const mesh = new THREE.Mesh(geometry, material);
  mesh.matrixAutoUpdate = false;
  mesh.castShadow = type !== GEOM.mjGEOM_PLANE.value;
  mesh.receiveShadow = true;
  scene.add(mesh);
  meshes.push({ mesh, g });
}

const _m = new THREE.Matrix4();
function syncMeshes() {
  const xpos = data.geom_xpos, xmat = data.geom_xmat;
  for (const { mesh, g } of meshes) {
    const p = g * 3, r = g * 9;
    _m.set(
      xmat[r], xmat[r + 1], xmat[r + 2], xpos[p],
      xmat[r + 3], xmat[r + 4], xmat[r + 5], xpos[p + 1],
      xmat[r + 6], xmat[r + 7], xmat[r + 8], xpos[p + 2],
      0, 0, 0, 1,
    );
    mesh.matrix.copy(_m);
  }
}

function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== w || canvas.height !== h) {
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
}

// ── Řízení ────────────────────────────────────────────────────────────
const target = Float64Array.from(defaultPose); // cílové úhly ze sliderů
const lastAction = new Float64Array(nu);
let demo = null; // "squat" | "step" | null
let paused = false;
let pushUntil = -1;
let simTime = 0;

const idx = Object.fromEntries(jointNames.map((n, i) => [n, i]));
function demoTargets(t, out) {
  out.set(target);
  if (demo === "squat") {
    // hip -a, knee +2a, ankle -a: chodidlo zůstává vodorovné
    const a = 0.35 * (1 - Math.cos(2 * Math.PI * t / 2.5)) / 2;
    for (const side of ["left", "right"]) {
      out[idx[`${side}_hip_pitch`]] -= a;
      out[idx[`${side}_knee`]] += 2 * a;
      out[idx[`${side}_ankle`]] -= a;
    }
  } else if (demo === "step") {
    // přenášení váhy rollem + střídavé pokrčení kolena; bez zpětné vazby
    // z IMU to dlouho nevydrží, přesně proto je potřeba politika.
    const w = 2 * Math.PI * 1.2 * t;
    const sway = 0.10 * Math.sin(w);
    out[idx.left_hip_roll] += sway;
    out[idx.right_hip_roll] += sway;
    const liftL = Math.max(0, Math.sin(w)) * 0.35;
    const liftR = Math.max(0, -Math.sin(w)) * 0.35;
    out[idx.left_hip_pitch] -= liftL; out[idx.left_knee] += 2 * liftL; out[idx.left_ankle] -= liftL;
    out[idx.right_hip_pitch] -= liftR; out[idx.right_knee] += 2 * liftR; out[idx.right_ankle] -= liftR;
  }
  return out;
}

const ctrlBuf = new Float64Array(nu);
let stepCounter = 0;
function controlStep() {
  demoTargets(simTime, ctrlBuf);
  for (let i = 0; i < nu; i++) {
    data.ctrl[i] = ctrlBuf[i];
    lastAction[i] = ctrlBuf[i] - defaultPose[i];
  }
}

function physicsStep() {
  if (stepCounter % DECIMATION === 0) controlStep();
  const f = trunkId * 6;
  data.xfrc_applied[f] = simTime < pushUntil ? 4.0 : 0; // 4 N dopředu
  mujoco.mj_step(model, data);
  simTime += timestep;
  stepCounter++;
}

// ── Pozorování (formát Microduck: 61 hodnot) ──────────────────────────
const obs = new Float32Array(3 + 3 + nu * 3 + 13);
const _q = new THREE.Quaternion();
const _g = new THREE.Vector3();
function buildObs() {
  let i = 0;
  for (let a = 0; a < 3; a++) obs[i++] = data.sensordata[gyroAdr + a];
  const xq = data.xquat.subarray(trunkId * 4, trunkId * 4 + 4); // [w x y z]
  _q.set(xq[1], xq[2], xq[3], xq[0]).conjugate();
  _g.set(0, 0, -1).applyQuaternion(_q);
  obs[i++] = _g.x; obs[i++] = _g.y; obs[i++] = _g.z;
  for (let j = 0; j < nu; j++) obs[i++] = data.qpos[qposAdr[j]] - defaultPose[j];
  for (let j = 0; j < nu; j++) obs[i++] = data.qvel[dofAdr[j]];
  for (let j = 0; j < nu; j++) obs[i++] = lastAction[j];
  for (let c = 0; c < 13; c++) obs[i++] = 0; // příkaz: rychlosti, hlava... zatím nula
  return obs;
}

// ── UI ────────────────────────────────────────────────────────────────
const sliders = [];
const slidersEl = $("sliders");
const jointRange = (i) => {
  const jid = mujoco.mj_name2id(model, OBJ.mjOBJ_JOINT.value, jointNames[i]);
  return [model.jnt_range[jid * 2], model.jnt_range[jid * 2 + 1]];
};
jointNames.forEach((name, i) => {
  const [lo, hi] = jointRange(i);
  const row = document.createElement("div");
  row.className = "slider";
  row.innerHTML = `<label title="${name}">${name}</label>
    <input type="range" min="${deg(lo).toFixed(0)}" max="${deg(hi).toFixed(0)}" step="1" />
    <output></output>`;
  const input = row.querySelector("input"), out = row.querySelector("output");
  const set = (rad) => { input.value = deg(rad).toFixed(0); out.textContent = deg(rad).toFixed(0); };
  input.addEventListener("input", () => {
    target[i] = rad(parseFloat(input.value));
    out.textContent = input.value;
  });
  set(defaultPose[i]);
  slidersEl.appendChild(row);
  sliders.push({ set });
});

function deg(r) { return r * 180 / Math.PI; }
function rad(d) { return d * Math.PI / 180; }

$("reset").onclick = reset;
$("pause").onclick = () => { paused = !paused; syncButtons(); };
$("push").onclick = () => { pushUntil = simTime + 0.15; };
$("squat").onclick = () => { demo = demo === "squat" ? null : "squat"; simTime = 0; syncButtons(); };
$("step").onclick = () => { demo = demo === "step" ? null : "step"; simTime = 0; syncButtons(); };
$("kp").oninput = (e) => {
  const kp = parseFloat(e.target.value);
  $("kp-out").textContent = kp.toFixed(1);
  setKp(kp);
};
function syncButtons() {
  $("pause").textContent = paused ? "Pokračovat" : "Pauza";
  $("pause").classList.toggle("on", paused);
  $("squat").classList.toggle("on", demo === "squat");
  $("step").classList.toggle("on", demo === "step");
}
addEventListener("keydown", (e) => {
  if (e.key === "r") reset();
  if (e.key === " ") { e.preventDefault(); $("pause").click(); }
  if (e.key === "p") $("push").click();
});

const stateEl = $("state"), obsEl = $("obs"), statusEl = $("status");
let uiTimer = 0;
function updateUi(dt, fps) {
  uiTimer += dt;
  if (uiTimer < 0.1) return;
  uiTimer = 0;
  const o = buildObs();
  const upright = o[5] < -0.85;
  let maxDev = 0;
  for (let j = 0; j < nu; j++) maxDev = Math.max(maxDev, Math.abs(data.qpos[qposAdr[j]] - data.ctrl[j]));
  const rows = [
    ["výška trupu", `${(data.qpos[2] * 1000).toFixed(1)} mm`],
    ["gravitace v trupu z", `<span class="${upright ? "ok" : "bad"}">${o[5].toFixed(2)} ${upright ? "STOJÍ" : "SPADL"}</span>`],
    ["gyro [rad/s]", `${o[0].toFixed(2)} ${o[1].toFixed(2)} ${o[2].toFixed(2)}`],
    ["kontakt L / P", `${data.sensordata[touchAdr[0]].toFixed(2)} / ${data.sensordata[touchAdr[1]].toFixed(2)} N`],
    ["max. odchylka kloubu", `${deg(maxDev).toFixed(1)}°`],
    ["čas simulace", `${simTime.toFixed(2)} s`],
  ];
  stateEl.innerHTML = rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("");
  obsEl.textContent = Array.from(o, (v) => v.toFixed(2)).join(" ");
  statusEl.textContent = `${fps.toFixed(0)} fps · fyzika ${(1 / timestep).toFixed(0)} Hz · řízení ${(1 / (timestep * DECIMATION)).toFixed(0)} Hz`;
}

// ── Smyčka ────────────────────────────────────────────────────────────
reset();
$("boot").remove();
let last = performance.now();
let acc = 0;
let fps = 60;
function frame(now) {
  requestAnimationFrame(frame);
  const dt = Math.min((now - last) / 1000, 0.1);
  last = now;
  fps = 0.9 * fps + 0.1 / Math.max(dt, 1e-3);
  if (!paused) {
    acc += dt;
    while (acc >= timestep) { physicsStep(); acc -= timestep; }
  }
  resize();
  syncMeshes();
  controls.update();
  renderer.render(scene, camera);
  updateUi(dt, fps);
}
requestAnimationFrame(frame);
