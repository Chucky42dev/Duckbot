"""Kontrola vygenerovaného modelu: stoj bez politiky a render obrázku.

Použití:
    python sim/check_model.py                 # duckbot_hold.xml, test stoje + PNG
    python sim/check_model.py --sysid         # duckbot.xml se změřeným kp 0.55 (spadne)
    python sim/check_model.py --kp 3          # přepsat tuhost ručně

Serva drží STAND_POSE jen svým PD regulátorem, bez politiky.
"""

import argparse
from pathlib import Path

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parent
MODEL_HOLD = ROOT / "model" / "duckbot_hold.xml"
MODEL_SYSID = ROOT / "model" / "duckbot.xml"


def projected_gravity(data, model):
    """Gravitace v souřadnicích trupu, obs[3:6] jako u Microducka."""
    sid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, "imu")
    rot = data.site_xmat[sid].reshape(3, 3)
    return rot.T @ np.array([0, 0, -1.0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kp", type=float, default=None, help="přepsat tuhost serv")
    ap.add_argument("--seconds", type=float, default=3.0)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--sysid", action="store_true", help="model se změřenými zisky serv")
    args = ap.parse_args()

    path = MODEL_SYSID if args.sysid else MODEL_HOLD
    model = mujoco.MjModel.from_xml_path(str(path))
    if args.kp is not None:
        model.actuator_gainprm[:, 0] = args.kp
        model.actuator_biasprm[:, 1] = -args.kp
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, 0)

    z0 = data.qpos[2]
    mujoco.mj_forward(model, data)
    com = data.subtree_com[1]  # těžiště celého robota (trunk = body 1)
    soles = [data.geom_xpos[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, n)]
             for n in ("left_sole", "right_sole")]
    feet = np.mean(soles, axis=0)
    print(f"těžiště: x {com[0]*1000:+.1f} mm, y {com[1]*1000:+.1f} mm | střed chodidel: "
          f"x {feet[0]*1000:+.1f} mm | rozteč chodidel {abs(soles[0][1]-soles[1][1])*1000:.1f} mm")
    steps = int(args.seconds / model.opt.timestep)
    min_z = z0
    for _ in range(steps):
        mujoco.mj_step(model, data)
        min_z = min(min_z, data.qpos[2])

    g = projected_gravity(data, model)
    z = data.qpos[2]
    upright = g[2] < -0.85
    print(f"trup: start {z0*1000:.1f} mm, po {args.seconds:.0f} s {z*1000:.1f} mm "
          f"(min {min_z*1000:.1f} mm, pokles {(z0-z)*1000:.1f} mm)")
    print(f"gravitace v trupu: {np.round(g, 3)}  ->  {'STOJÍ' if upright else 'SPADL'}")
    left = data.sensor("left_foot_contact").data[0]
    right = data.sensor("right_foot_contact").data[0]
    print(f"kontakt chodidel: L {left:.2f} N, P {right:.2f} N (tíha {sum(model.body_mass)*9.81:.2f} N)")
    q = data.qpos[7:]
    target = data.ctrl
    print(f"max. odchylka kloubu od cíle: {np.degrees(np.abs(q - target).max()):.1f}°")

    if args.no_render:
        return
    try:
        renderer = mujoco.Renderer(model, height=720, width=1280)
        renderer.update_scene(data, camera="side")
        image = renderer.render()
        from PIL import Image
        out = path.with_suffix(".png")
        Image.fromarray(image).save(out)
        print(f"obrázek: {out.relative_to(ROOT.parent)}")
    except Exception as exc:  # render je jen bonus, bez GL kontextu ho přeskočíme
        print(f"render přeskočen: {exc}")


if __name__ == "__main__":
    main()
