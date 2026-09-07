# Duckbot project context

## Project goal

Duckbot is a personal open-source experiment inspired by Pollen Robotics'
Microduck: a small walking duck robot that can eventually use simulation,
reinforcement learning, vision and voice commands.

The project owner already has experience with ESP32 and Arduino-style sensors.
The preferred approach is incremental: prove the hardware and safety first,
then add scripted walking, then MuJoCo and sim2real/RL. Do not jump directly to
an autonomous neural walking policy.

## Current repository

- GitHub: `https://github.com/Chucky42dev/Duckbot`
- Default branch: `main`
- Local project path: `D:\Projekty\Duckbot` (renamed from `D:\Projekty\Microduck`)
- Simulator web address: `http://duckbot.local` (XAMPP vhost -> `sim/web/dist`)
- Main research document: `docs/research-microduck.md`
- PDF output: `docs/research-microduck.pdf`
- PDF generator: `scripts/build_research_pdf.py`

The project currently contains documentation and PDF generation only. Firmware,
mechanical CAD, a MuJoCo model and a PlatformIO project have not been created
yet.

## Important decisions

1. ESP32 owns realtime and safety-critical work: IMU reads, servo commands,
   calibration, joint limits, fall detection, emergency stop, watchdog and
   command timeout.
2. A Raspberry Pi or another Linux SBC owns higher-level work: MuJoCo,
   ONNX inference, camera processing, voice recognition, logging and high-level
   intent conversion.
3. Higher layers send intents such as `stand`, `forward` and `turn`; they must
   not send unrestricted raw servo angles over Wi-Fi or from a voice model.
4. If the command heartbeat stops, the low-level controller must enter a safe
   state. A voice assistant or LLM must never be part of the stabilization loop.
5. Build order: one actuator and telemetry, safety layer, stable standing,
   scripted walking, accurate MJCF model, then PPO/RL and sim2real.

## Actuator identified from the reference photo

The photographed actuator is a ROBOTIS DYNAMIXEL XL330-M288-T. Relevant
official specifications:

- 3.7-6.0 V input, recommended 5 V
- 18 g, approximately 20 x 34 x 26 mm
- 0.52 Nm stall torque at 5 V and 1.47 A
- 4096 pulses per revolution and contactless absolute encoder
- TTL half-duplex multidrop bus, DYNAMIXEL Protocol 2.0
- position, velocity, current, voltage, temperature and trajectory feedback
- position, velocity, current-based position and PWM operating modes
- internal PID control and a configurable Bus Watchdog

Use the official model manual before designing around dimensions or addresses:

`https://docs.robotis.com/docs/dxl/model_reference/x_series/xl_series/xl330-m288/`

The ESP32 is a 3.3 V MCU. The actuator documentation describes a TTL bus and
recommends a suitable half-duplex circuit/level matching. Do not connect a
multi-servo bus directly without checking the electrical interface. For bench
testing, consider a ROBOTIS U2D2 or OpenRB-150 and the official Dynamixel SDK.

Power is a major design constraint. One stalled actuator can draw about 1.47 A
at 5 V; a multi-actuator robot needs a properly sized supply, distribution,
fuses/current protection and suitable wiring. Never test an assembled walking
robot without a physical support or emergency power cutoff.

## Microduck facts to preserve accurately

Official Microduck materials describe a roughly 25 cm, 800 g robot with 15
motors, camera, LiDAR, two IMUs, a 50 Hz onboard policy loop and ONNX policies.
The official runtime repository is mostly Rust and separates the motor/safety
owner from transports and peripheral services. It uses MuJoCo and PPO for
training policies according to the published project material.

Reported out-of-box behaviors include walking, sit/stand, kicking, beak-based
grasping, roller locomotion, recovery from a fall and sounds/quacking. These are
not automatically transferable to Duckbot: they depend on matching mechanics,
calibration, actuators, sensors and policy input/output shapes.

## Research links

- Microduck runtime: `https://github.com/pollen-robotics/microduck`
- Microduck simulator: `https://huggingface.co/spaces/pollen-robotics/microduck-simulator`
- Microduck product page: `https://pollen-robotics.com/microduck/`
- MuJoCo: `https://mujoco.readthedocs.io/en/stable/`
- TorchRL PPO: `https://docs.pytorch.org/rl/main/reference/generated/torchrl.objectives.ClipPPOLoss.html`
- XL330-M288-T manual: `https://docs.robotis.com/docs/dxl/model_reference/x_series/xl_series/xl330-m288/`

The exact public location of the separately referenced `microduck_rl` project
was not confirmed during the initial research. Verify the current official
link before treating it as a dependency.

## Dev Pack interpretation

Microduck's Dev Pack is a maintenance and experimentation kit, not a second
processor or a bundle of new robot capabilities. It includes three spare
motors, five motor cables, two batteries, a dual charger, ten NFC tags, Hugging
Face credit, a screwdriver and spare screws. It does not add a camera, LiDAR,
IMU or automatic learning system. NFC tags can act as software triggers for
behaviors; Hugging Face credit can pay for cloud jobs, but does not guarantee a
successful policy.

## Recommended next implementation

When implementation starts, create a small PlatformIO ESP32 firmware that can:

1. discover or ping one XL330 actuator;
2. read model ID, position, current, voltage and temperature;
3. move only inside a conservative position limit;
4. expose an emergency torque-off command;
5. log telemetry over USB;
6. add a command watchdog before connecting more actuators.

Do not begin with voice, camera or PPO. First make one actuator predictable,
measurable and electrically safe.

## Working conventions

- Keep documentation and code changes small and focused.
- Preserve user changes in existing files.
- Validate hardware assumptions against official manuals.
- Prefer Python for early simulation/tools and ESP32 C++/PlatformIO for the
  realtime firmware unless a later decision establishes another stack.
- Keep the repository and documentation in Czech where practical, while code
  identifiers and protocol fields may remain English.
- Before committing, run `git diff --check` and the narrowest available build or
  test command.
