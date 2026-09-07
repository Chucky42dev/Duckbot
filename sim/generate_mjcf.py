"""Vygeneruje MJCF model Duckbotu z parametrů v duckbot_params.py.

Použití:
    python sim/generate_mjcf.py          # zapíše sim/model/duckbot.xml

Model používá jen primitivní geometrie (box, kapsle, koule), žádné STL.
Strom kloubů, jejich pořadí, názvy aktuátorů a senzorů kopírují Microduck,
takže model je kompatibilní s formátem pozorování 61 -> akce 14.
"""

from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

import mujoco
import numpy as np

import duckbot_params as P

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "model" / "duckbot.xml"          # změřená serva, pro trénink
OUTPUT_HOLD = ROOT / "model" / "duckbot_hold.xml"  # tuhá serva, ruční testy a web


def fmt(*values):
    return " ".join(f"{v:.5g}" for v in values)


def sub(parent, tag, **attrs):
    return ET.SubElement(parent, tag, {k: str(v) for k, v in attrs.items()})


def build_leg(trunk, side):
    """Levá (side=+1) nebo pravá (side=-1) noha, řetězec jako u Microducka."""
    name = "left" if side > 0 else "right"
    L, T, S, C = P.LEG, P.TRUNK, P.SERVO, P.COLORS
    r = L["radius"]

    # hip_yaw: servo pod trupem, osa svislá
    hip_yaw = sub(trunk, "body", name=f"{name}_hip_yaw",
                  pos=fmt(T["hip_x"], side * T["hip_y"], T["hip_z"]))
    sub(hip_yaw, "joint", name=f"{name}_hip_yaw", axis="0 0 1",
        range=fmt(*P.JOINT_RANGE["hip_yaw"]))
    sub(hip_yaw, "geom", type="box", size=fmt(0.012, 0.010, 0.008),
        pos=fmt(0, 0, -L["yaw_to_roll"] / 2), rgba=C["servo"], mass=L["mass_yaw"],
        **{"class": "visual"})

    # hip_roll: osa podélná (x), naklání nohu do stran
    hip_roll = sub(hip_yaw, "body", name=f"{name}_hip_roll",
                   pos=fmt(0, 0, -L["yaw_to_roll"]))
    sub(hip_roll, "joint", name=f"{name}_hip_roll", axis="1 0 0",
        range=fmt(*P.JOINT_RANGE["hip_roll"]))
    sub(hip_roll, "geom", type="box", size=fmt(0.010, 0.014, 0.006),
        rgba=C["dark"], mass=L["mass_roll"], **{"class": "visual"})

    # hip_pitch: stehno, osa příčná (y)
    upper = sub(hip_roll, "body", name=f"{name}_upper_leg",
                pos=fmt(0, 0, -L["roll_to_pitch"] / 2))
    sub(upper, "joint", name=f"{name}_hip_pitch", axis="0 1 0",
        range=fmt(*P.JOINT_RANGE["hip_pitch"]))
    sub(upper, "geom", type="box", size=fmt(0.013, 0.010, 0.017),
        pos=fmt(0, side * 0.004, 0), rgba=C["servo"], mass=S["mass"],
        **{"class": "visual"})
    sub(upper, "geom", type="capsule", size=fmt(r),
        fromto=fmt(0, 0, 0, 0, 0, -L["upper"]), rgba=C["shell"],
        mass=L["mass_upper"] - S["mass"], **{"class": "visual"})

    # knee: holeň
    lower = sub(upper, "body", name=f"{name}_lower_leg", pos=fmt(0, 0, -L["upper"]))
    sub(lower, "joint", name=f"{name}_knee", axis="0 1 0",
        range=fmt(*P.JOINT_RANGE["knee"]))
    sub(lower, "geom", type="capsule", size=fmt(r * 0.85),
        fromto=fmt(0, 0, 0, 0, 0, -L["lower"]), rgba=C["dark"],
        mass=L["mass_lower"], **{"class": "collision"})

    # ankle: servo kotníku + oranžové chodidlo
    foot = sub(lower, "body", name=f"{name}_foot", pos=fmt(0, 0, -L["lower"]))
    sub(foot, "joint", name=f"{name}_ankle", axis="0 1 0",
        range=fmt(*P.JOINT_RANGE["ankle"]))
    sub(foot, "geom", type="box", size=fmt(0.010, 0.013, 0.009),
        rgba=C["servo"], mass=S["mass"], **{"class": "visual"})
    fx, fy, fz = P.LEG["foot_size"]
    sub(foot, "geom", name=f"{name}_sole", type="box", size=fmt(fx / 2, fy / 2, fz / 2),
        pos=fmt(L["foot_x_offset"], 0, -L["ankle_to_sole"] + fz / 2),
        rgba=C["orange"], mass=L["mass_foot"] - S["mass"], friction="1.0 0.005 0.0001",
        **{"class": "collision"})
    sub(foot, "site", name=f"{name}_foot_site", type="box", size=fmt(fx / 2, fy / 2, 0.001),
        pos=fmt(L["foot_x_offset"], 0, -L["ankle_to_sole"]), group=4)


def build_head(trunk):
    H, C, S = P.HEAD, P.COLORS, P.SERVO

    neck = sub(trunk, "body", name="neck", pos=fmt(*H["neck_base"]))
    sub(neck, "joint", name="neck_pitch", axis="0 1 0",
        range=fmt(*P.JOINT_RANGE["neck_pitch"]))
    sub(neck, "geom", type="capsule", size="0.009",
        fromto=fmt(0, 0, 0, 0, 0, H["neck"]), rgba=C["shell"],
        mass=H["mass_neck"], **{"class": "visual"})

    head_pitch = sub(neck, "body", name="head_pitch", pos=fmt(0, 0, H["neck"]))
    sub(head_pitch, "joint", name="head_pitch", axis="0 1 0",
        range=fmt(*P.JOINT_RANGE["head_pitch"]))
    sub(head_pitch, "geom", type="box", size=fmt(0.010, 0.012, 0.010),
        rgba=C["servo"], mass=H["mass_neck_pitch"], **{"class": "visual"})

    head_yaw = sub(head_pitch, "body", name="head_yaw", pos=fmt(0, 0, H["head_pitch_to_yaw"]))
    sub(head_yaw, "joint", name="head_yaw", axis="0 0 1",
        range=fmt(*P.JOINT_RANGE["head_yaw"]))
    sub(head_yaw, "geom", type="box", size=fmt(0.012, 0.012, 0.009),
        rgba=C["servo"], mass=H["mass_yaw"], **{"class": "visual"})

    head = sub(head_yaw, "body", name="head", pos=fmt(0, 0, H["yaw_to_roll"]))
    sub(head, "joint", name="head_roll", axis="1 0 0",
        range=fmt(*P.JOINT_RANGE["head_roll"]))
    hx, hy, hz = H["size"]
    ox, oy, oz = H["head_offset"]
    sub(head, "geom", name="head_shell", type="box", size=fmt(hx / 2, hy / 2, hz / 2),
        pos=fmt(ox, oy, oz), rgba=C["shell"], mass=H["mass_head"], **{"class": "collision"})
    # zobák a oči: jen vizuální, bez hmotnosti
    sub(head, "geom", type="box", size=fmt(0.018, 0.022, 0.006),
        pos=fmt(ox + hx / 2 + 0.014, 0, oz - 0.012), rgba=C["orange"], mass=0,
        **{"class": "visual"})
    for s in (1, -1):
        sub(head, "geom", type="sphere", size="0.007",
            pos=fmt(ox + hx / 2 - 0.004, s * (hy / 2 - 0.004), oz + 0.008),
            rgba=C["eye"], mass=0, **{"class": "visual"})
    sub(head, "site", name="camera_site", pos=fmt(ox + hx / 2, 0, oz), group=4)
    sub(head, "camera", name="eye", pos=fmt(ox + hx / 2 + 0.01, 0, oz + 0.005),
        xyaxes="0 -1 0 0 0 1", fovy="90")


def build_model(hold=False):
    """hold=True: tuhé PD držení (P.HOLD) místo identifikovaných zisků serva."""
    T, S, C = P.TRUNK, P.SERVO, P.COLORS
    kp, kv = (P.HOLD["kp"], P.HOLD["kv"]) if hold else (S["kp"], S["kv"])
    root = ET.Element("mujoco", model="duckbot_hold" if hold else "duckbot")
    sub(root, "compiler", angle="radian", autolimits="true")
    sub(root, "option", timestep=P.SIM["timestep"], integrator="implicitfast")
    visual = sub(root, "visual")
    sub(visual, "global", offwidth=1280, offheight=720)

    default = sub(root, "default")
    sub(default, "joint", damping=S["damping"], frictionloss=S["frictionloss"],
        armature=S["armature"])
    sub(default, "position", kp=kp, kv=kv,
        forcerange=fmt(-S["forcerange"], S["forcerange"]),
        ctrlrange=fmt(-S["ctrlrange"], S["ctrlrange"]))
    vis = sub(default, "default", **{"class": "visual"})
    sub(vis, "geom", contype=0, conaffinity=0, group=1)
    col = sub(default, "default", **{"class": "collision"})
    sub(col, "geom", contype=1, conaffinity=1, group=1, condim=3)

    asset = sub(root, "asset")
    sub(asset, "texture", name="grid", type="2d", builtin="checker", width=512, height=512,
        rgb1="0.12 0.12 0.13", rgb2="0.18 0.18 0.2")
    sub(asset, "material", name="grid", texture="grid", texrepeat="20 20",
        texuniform="true", reflectance="0.1")

    world = sub(root, "worldbody")
    sub(world, "light", pos="0.5 -0.5 1.5", dir="-0.3 0.3 -1", diffuse="0.8 0.8 0.8")
    sub(world, "light", pos="-0.5 0.5 1.0", dir="0.3 -0.3 -1", diffuse="0.4 0.4 0.4")
    sub(world, "geom", name="floor", type="plane", size="3 3 0.05", material="grid",
        friction=fmt(*P.SIM["floor_friction"]), contype=1, conaffinity=1)
    sub(world, "camera", name="side", pos="0.42 -0.42 0.24", mode="targetbody", target="trunk")
    sub(world, "camera", name="front", pos="0.55 0 0.18", mode="targetbody", target="trunk")

    trunk = sub(world, "body", name="trunk", pos=fmt(0, 0, T["z_stand"]))
    sub(trunk, "freejoint", name="root")
    tx, ty, tz = T["size"]
    sub(trunk, "geom", name="trunk_shell", type="box", size=fmt(tx / 2, ty / 2, tz / 2),
        rgba=C["shell"], mass=T["mass"], **{"class": "collision"})
    sub(trunk, "site", name="imu", pos="0 0 0", size="0.005", group=4)
    sub(trunk, "camera", name="track", mode="trackcom", pos="0.45 -0.55 0.30",
        xyaxes="0.77 0.63 0 -0.28 0.34 0.9")

    build_leg(trunk, +1)
    build_head(trunk)
    build_leg(trunk, -1)

    actuator = sub(root, "actuator")
    for joint in P.JOINT_ORDER:
        sub(actuator, "position", name=joint, joint=joint)

    sensor = sub(root, "sensor")
    sub(sensor, "framequat", name="orientation", objtype="site", objname="imu", noise=0.001)
    sub(sensor, "gyro", name="angular-velocity", site="imu", noise=0.005)
    sub(sensor, "gyro", name="imu_ang_vel", site="imu")
    sub(sensor, "velocimeter", name="imu_lin_vel", site="imu")
    sub(sensor, "accelerometer", name="imu_accel", site="imu")
    sub(sensor, "subtreeangmom", name="root_angmom", body="trunk")
    for name in ("left", "right"):
        sub(sensor, "touch", name=f"{name}_foot_contact", site=f"{name}_foot_site")

    keyframe = sub(root, "keyframe")
    qpos = [0, 0, T["z_stand"], 1, 0, 0, 0] + [P.STAND_POSE[j] for j in P.JOINT_ORDER]
    ctrl = [P.STAND_POSE[j] for j in P.JOINT_ORDER]
    sub(keyframe, "key", name="stand", qpos=fmt(*qpos), ctrl=fmt(*ctrl))
    return root


def settle_stand_height(xml_text):
    """Spočítá výšku trupu tak, aby podrážky ležely přesně na podlaze."""
    model = mujoco.MjModel.from_xml_string(xml_text)
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, 0)
    mujoco.mj_kinematics(model, data)
    lowest = np.inf
    for name in ("left_sole", "right_sole"):
        gid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, name)
        half_h = model.geom_size[gid][2]
        # spodní hrana boxu (chodidlo je vodorovné ve stand póze)
        lowest = min(lowest, data.geom_xpos[gid][2] - half_h)
    return data.qpos[2] - lowest


def write_model(path, hold):
    root = build_model(hold=hold)
    z = settle_stand_height(ET.tostring(root, encoding="unicode"))

    key = root.find("keyframe/key")
    qpos = key.get("qpos").split()
    qpos[2] = f"{z:.5g}"
    key.set("qpos", " ".join(qpos))
    root.find("worldbody/body[@name='trunk']").set("pos", fmt(0, 0, z))

    pretty = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(pretty, encoding="utf-8")
    print(f"zapsáno {path.relative_to(ROOT.parent)}")
    return z


def main():
    z = write_model(OUTPUT, hold=False)
    write_model(OUTPUT_HOLD, hold=True)
    model = mujoco.MjModel.from_xml_path(str(OUTPUT))
    total = sum(model.body_mass)
    print(f"klouby: {model.nu} aktuátorů, {model.nq} qpos, {model.nsensordata} hodnot senzorů")
    print(f"celková hmotnost: {total * 1000:.0f} g, výška trupu při stoji: {z * 1000:.1f} mm")


if __name__ == "__main__":
    main()
