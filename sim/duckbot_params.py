"""Parametry Duckbotu pro generátor MJCF.

Všechny hodnoty jsou ODHAD odvozený z MJCF modelu Microducka
(pollen-robotics/microduck-simulator, robot_allcollisions.xml) a z datasheetu
XL330-M288-T. Jednotky: metry, kilogramy, radiány. Osa x = dopředu, z = nahoru.

Až bude reálný hardware, přepiš hodnoty podle změřeného stroje. Struktura
(pořadí kloubů, názvy senzorů) je záměrně shodná s Microduckem, aby šel použít
stejný tréninkový kód a stejný 61/14 formát pozorování/akce.
"""

# --- Servo: XL330-M288-T, hodnoty identifikované Pollenem ("chosen_actuator") ---
# kp je nízké (0.55 Nm/rad): XL330 je poddajné, politika to kompenzuje.
# Pro tužší chování při ručních testech zvyš kp na ~2-5, forcerange nech.
SERVO = dict(
    kp=0.55,            # tuhost polohové regulace [Nm/rad]
    kv=0.0,             # tlumení regulátoru
    forcerange=0.96,    # max. moment [Nm] (stall 0.52 Nm @5 V je konzervativnější)
    ctrlrange=10.0,     # rozsah řídicího vstupu [rad], omezí až joint range
    damping=0.053,      # viskózní tlumení kloubu
    frictionloss=0.0048,
    armature=0.0018,    # setrvačnost rotoru a převodu
    mass=0.018,         # hmotnost jednoho serva [kg]
)

# Tuhé držení pro ruční testy a prohlížeč (bez politiky). S kp 0.55 robot bez
# politiky spadne: politika u Microducka posílá "virtuální" cíle až ±10 rad,
# aby z poddajného serva dostala moment. Pro stoj bez politiky stačí kp >= 2.
HOLD = dict(kp=5.0, kv=0.1)

# --- Trup (baterie NP-F550 ~90 g, ESP32/SBC, kabely, skořepina) ---
TRUNK = dict(
    size=(0.075, 0.060, 0.050),  # délka x, šířka y, výška z
    mass=0.200,
    z_stand=0.120,               # výška středu trupu při stoji
    hip_x=0.006,                 # posun kyčlí dopředu od středu trupu
    hip_y=0.0175,                # polovina rozteče kyčlí
    hip_z=-0.005,                # kyčelní yaw kloub pod středem trupu
)

# --- Noha (řetězec Microducka: hip_yaw -> hip_roll -> hip_pitch -> knee -> ankle) ---
LEG = dict(
    yaw_to_roll=0.0165,     # svislá vzdálenost yaw -> roll kloub
    roll_to_pitch=0.025,    # vzdálenost roll -> pitch kloub (bok)
    upper=0.042,            # délka stehna (pitch -> koleno)
    lower=0.049,            # délka holeně (koleno -> kotník)
    ankle_to_sole=0.018,    # kotník -> podrážka
    radius=0.012,           # poloměr kapslí nohou
    mass_yaw=0.023,         # servo yaw + držák
    mass_roll=0.006,        # držák roll
    mass_upper=0.048,       # servo pitch + stehno
    mass_lower=0.022,       # holeň
    mass_foot=0.030,        # servo kotníku + chodidlo
    foot_size=(0.060, 0.032, 0.006),  # chodidlo (box), délka x šířka x výška
    foot_x_offset=0.0,      # posun chodidla vůči kotníku (0 = přímo pod ním)
)

# --- Krk a hlava (kamera, ToF, dvě serva zobáku/hlavy, skořepina) ---
HEAD = dict(
    neck_base=(0.026, 0.0, 0.032),  # neck_pitch kloub vůči středu trupu
    neck=0.050,             # délka krku (neck_pitch -> head_pitch)
    head_pitch_to_yaw=0.019,
    yaw_to_roll=0.018,
    size=(0.080, 0.060, 0.050),  # hlava (box)
    mass_neck=0.037,
    mass_neck_pitch=0.006,
    mass_yaw=0.049,
    mass_head=0.189,
    head_offset=(0.025, 0.0, 0.010),  # střed hlavy vůči roll kloubu
)

# --- Rozsahy kloubů [rad] (Microduck) ---
JOINT_RANGE = dict(
    hip_yaw=(-0.436, 0.524),
    hip_roll=(-0.384, 0.384),
    hip_pitch=(-1.571, 1.571),
    knee=(-1.571, 1.571),
    ankle=(-1.571, 1.571),
    neck_pitch=(-1.571, 1.047),
    head_pitch=(-1.571, 1.571),
    head_yaw=(-2.967, 2.967),
    head_roll=(-0.436, 0.436),
)

# --- Pořadí kloubů = pořadí aktuátorů = pořadí v obs/action (Microduck) ---
JOINT_ORDER = [
    "left_hip_yaw", "left_hip_roll", "left_hip_pitch", "left_knee", "left_ankle",
    "neck_pitch", "head_pitch", "head_yaw", "head_roll",
    "right_hip_yaw", "right_hip_roll", "right_hip_pitch", "right_knee", "right_ankle",
]

# Výchozí póza "stand" po vzoru Microducka: rovné nohy skloněné dopředu
# (chodidla pod těžkou hlavou), kotník srovná chodidlo, roll rozšíří stoj.
# Konvence (osa y): kladný úhel naklání horní konec článku dopředu (+x),
# tj. hip_pitch záporné = koleno dopředu; krk dopředu, hlava zpět do roviny.
STAND_POSE = {
    "left_hip_yaw": 0.0, "left_hip_roll": 0.087, "left_hip_pitch": -0.30,
    "left_knee": 0.0, "left_ankle": 0.30,
    "neck_pitch": 0.35, "head_pitch": -0.35, "head_yaw": 0.0, "head_roll": 0.0,
    "right_hip_yaw": 0.0, "right_hip_roll": -0.087, "right_hip_pitch": -0.30,
    "right_knee": 0.0, "right_ankle": 0.30,
}

# --- Simulace ---
SIM = dict(
    timestep=0.005,     # 200 Hz fyzika
    decimation=4,       # 50 Hz řízení (jako Microduck)
    floor_friction=(0.8, 0.005, 0.0001),
)

# --- Barvy (Microduck: bílá skořepina, oranžové nohy a zobák) ---
COLORS = dict(
    shell="0.95 0.95 0.93 1",
    orange="0.98 0.55 0.10 1",
    dark="0.15 0.15 0.15 1",
    servo="0.25 0.25 0.28 1",
    eye="0.1 0.1 0.1 1",
)
