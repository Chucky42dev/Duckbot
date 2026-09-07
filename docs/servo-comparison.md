# Duckbot: srovnání serv a kusovníky pro chodící spodek

Datum: 7. 9. 2026. Ceny jsou v Kč včetně DPH, bez dopravy. Položky označené
„ověřeno" byly zkontrolovány přímo v e-shopu v den sepsání, ostatní ceny jsou
orientační odhady z běžných CZ/EU cen a mohou se lišit o 10–20 %.

## 1. Kandidátní serva

Microduck od Pollen Robotics používá 15× DYNAMIXEL XL330-M288-T (14 kloubů
řízených politikou + zobák); potvrzuje to mesh `xl330.stl` v oficiálním
simulátoru i rozbory BOM. Jeho předchůdce Open Duck Mini v2 používá Feetech
STS3215. Waveshare prodává Feetech serva pod vlastním označením (SC09 = SCS09,
ST3215 = STS3215).

| Parametr | Waveshare SC09 (Feetech SCS09) | Waveshare ST3215 / Feetech STS3215 | DYNAMIXEL XL330-M288-T |
|---|---|---|---|
| Moment | 2,3 kg·cm ≈ 0,23 Nm @ 6 V | 19,5 kg·cm ≈ 1,9 Nm @ 7,4 V (30 kg·cm @ 12 V u 12 V verze) | 0,52 Nm ≈ 5,3 kg·cm @ 5 V |
| Napájení | 4,8–8,4 V | 6–12,6 V (2S LiPo přímo) | 3,7–6 V (z 2S nutný step-down) |
| Stall proud | 1,0 A | ~2,7 A | 1,47 A |
| Rychlost naprázdno | 100 ot/min @ 6 V | ~45–50 ot/min @ 7,4 V | 103 ot/min @ 5 V |
| Snímač polohy | potenciometr, 1024 kroků / 300° | magnetický, 4096 kroků / 360°, multi-turn | bezkontaktní magnetický, 4096 / 360° |
| Zpětná vazba | poloha, zátěž, rychlost, napětí | poloha, rychlost, zátěž, napětí, proud, teplota | poloha, rychlost, proud, napětí, teplota, trajektorie |
| Režimy řízení | poloha, kontinuální otáčení | poloha, rychlost, PWM, multi-turn | poloha, rychlost, current-based position, PWM; interní PID |
| Bezpečnost v servu | – | limity napětí/teploty/zátěže | + hardwarový Bus Watchdog |
| Protokol | Feetech SCS, half-duplex TTL UART | Feetech STS, half-duplex TTL UART, až 1 Mb/s | DYNAMIXEL Protocol 2.0, half-duplex TTL |
| Rozměry / hmotnost | 23 × 12 × 25,5 mm, ~13 g | 45 × 25 × 35 mm, ~60 g | 20 × 34 × 26 mm, 18 g |
| Cena za kus | 278 Kč LaskaKit (ověřeno) | 648–678 Kč LaskaKit (ověřeno); ~350–400 Kč Feetech přímo | ~1 000 Kč Generation Robots (€40,20, ověřeno); ROBOTIS US $23,90 + DPH a clo |

Poznámky:

- „19,5 kg" a „30 kg" ST3215 je totéž servo ve dvou vinutích (7,4 V a 12 V).
  Pro robota na 2S LiPo je správná 7,4 V verze. U LaskaKitu byla 7,4 V verze
  v den sepsání vyprodaná, 12 V verze skladem 1 ks.
- SC09 má méně než polovinu momentu XL330-M288 a potenciometrický snímač;
  pro nohy chodícího robota není vhodné. Hodí se na hlavu, zobák nebo jako
  levné cvičné servo pro sběrnici (protokol se ale liší od Dynamixelu).
- MJCF Microducku má pro serva `forcerange ±0,96 Nm` – to je simulační ladicí
  hodnota, ne reálná schopnost XL330 (katalogový stall 0,52 Nm).

## 2. Tři cesty ke kompletnímu robotu

Společný základ pro DIY varianty (ESP32, RPi Zero 2 W, IMU, kamera, baterie,
nabíječka, kabeláž, filament, spojovací materiál) vychází na ~4–5,5 tis. Kč.

| Položka | A) Microduck klon – 15× XL330-M288-T | B) Open Duck Mini v2 – 14× STS3215 | C) Koupit Microduck |
|---|---|---|---|
| Serva | 15 × 1 000 = 15 000 (EU) / ~11 000 (USA) | 14 × 660 = 9 200 (LaskaKit) / ~5 300 (Feetech přímo) | v ceně |
| Sběrnicové rozhraní | U2D2 ~1 400, OpenRB-150 ~800 nebo vlastní budič 74LVC2G241 ~50 | Waveshare Bus Servo Driver 148 (ověřeno) | – |
| Napájení serv | step-down 5 V / ≥ 15 A ~500 | 2S LiPo přímo | – |
| Společný základ | ~5 000 | ~5 000 | – |
| Celkem | ~17–22 tis. Kč | ~11–15 tis. Kč | $399 ≈ 9,5 tis. + DPH a doprava ≈ 12–13 tis. Kč |
| Náhradní servo | ~1 000 Kč | ~400–660 Kč | Dev Pack (3 ks) |

### A) Microduck klon (XL330-M288-T)

Plusy:

- Pollenův MJCF, ONNX politiky a simulátor sedí 1:1 – nejkratší cesta k RL a
  sim2real, které už někomu fungují.
- Nejlepší serva ve srovnání: Protocol 2.0, interní PID, current-based position,
  hardwarový Bus Watchdog, teplota, výborná dokumentace.
- Malý a lehký robot (800 g): nejmenší škody při pádu, nejmenší proudy.

Mínusy:

- Nejdražší: samotná serva stojí víc než celý hotový Microduck.
- CAD Microducku není kompletně veřejný, mechaniku je nutné odvodit z STL
  v simulátoru.
- 0,52 Nm je na hraně (vstávání z pádu); politika je na to laděná.
- ESP32 (3,3 V) potřebuje pro TTL sběrnici budič; serva potřebují 5 V
  step-down z 2S s rezervou ≥ 15 A.

### B) Open Duck Mini v2 (STS3215)

Plusy:

- Kompletně open source: Onshape CAD, STL, BOM, MJCF, trénink v Open Duck
  Playground. Pro DIY stavbu nejsnazší start.
- 3,7× větší moment než XL330-M288, velká rezerva; 2S LiPo přímo bez
  regulátoru.
- Nejlevnější na servo, obrovská komunita (LeRobot SO-101 používá totéž
  servo), snadno dostupné náhradní díly.
- ESP32 komunikuje přímo přes adaptér za 148 Kč.

Mínusy:

- Robot je ~40 cm a 1,3–1,5 kg: pády víc bolí, 14 × 2,7 A stall vyžaduje
  pořádnou baterii, pojistky a silné vodiče.
- Pollenův simulátor a politiky nelze použít 1:1; je nutný Open Duck
  Playground a jeho model.
- Feetech: horší dokumentace registrů, žádný hardwarový watchdog (řeší ESP32
  firmware), slabší možnosti nastavení regulátoru.
- 7,4 V verze u LaskaKitu občas není skladem; z Číny se čeká 2–4 týdny.

### C) Koupit Microduck

Plusy:

- Nejlevnější cesta k fungujícímu chodícímu robotu s RL, 100 % kompatibilní se
  simulátorem; okamžitě lze trénovat vlastní politiky.
- Ušetří desítky hodin mechaniky a ladění.

Mínusy:

- Není to stavba: učení o ESP32, sběrnici a napájení odpadá nebo se omezí.
- Rust runtime na RPi; plánovaná ESP32 bezpečnostní vrstva tam není.
- Dostupnost a čekací doba, servis závislý na Dev Packu.

### Doporučení

Je-li cílem naučit se robota postavit, dává smysl cesta B. Koupit nejdřív jedno
ST3215 (7,4 V) s adaptérem a splnit krok 1 z plánu (ping, telemetrie, limity,
torque-off, watchdog). Servo zůstane v robotu. Zbytek objednat hromadně až po
ověření. Je-li cílem co nejdřív experimentovat s RL politikami, je levnější
koupit Microduck než stavět jeho klon.

## 3. Kusovníky: chodící spodek (od pasu dolů)

Konfigurace odpovídá nohám Microducku / Open Duck Mini: 5 stupňů volnosti na
nohu (kyčel yaw, kyčel roll, kyčel pitch, koleno, kotník), celkem 10 serv, plus
trup s elektronikou a baterií. Cílem této fáze je stabilní stoj a skriptovaná
chůze na závěsu; kamera, RPi a hlava přijdou později.

### 3.1 Společné položky (všechny varianty)

| Položka | Specifikace / poznámka | Ks | Cena Kč |
|---|---|---|---|
| ESP32-S3 DevKitC-1 (N8R8) | realtime řízení serv, IMU, bezpečnost; 3 HW UART | 1 | 300 |
| IMU BNO055 (alternativně ICM-42688-P ~150 Kč) | fúze orientace v čipu, I2C; pro RL později raději surová data z ICM | 1 | 350 |
| Step-down 5 V / 3 A pro ESP32 | mini buck (MP1584 / Pololu D24V22F5), vstup z 2S | 1 | 80 |
| LiPo 2S 7,4 V 2 200 mAh, ≥ 35C, XT60 | ~120 g; při 10 servech dává rezervu i pro stall špičky | 1 | 450 |
| Nabíječka LiPo s balancérem | ISDT / iMAX B6 nebo podobná | 1 | 700 |
| LiPo safe bag | nabíjení a skladování | 1 | 120 |
| Pojistka + držák | ATO/mini blade 15 A (varianta A: 10 A na 5 V větvi) | 1 | 60 |
| Hlavní vypínač / XT60 klíč | fyzické odpojení napájení serv – nouzový stop | 1 | 80 |
| Konektory XT60 + XT30, sada | baterie, rozvod, servisní odbočka | 1 | 100 |
| Silikonový kabel 16 AWG, červený + černý, 2 m | hlavní rozvod k servům | 1 | 120 |
| Rozvodná deska / svorkovnice | rozbočení napájení k větvím serv | 1 | 100 |
| Filament PETG 1 kg | trup, stehna, lýtka, chodidla, držáky | 1 | 550 |
| Šrouby M2, M2,5, M3 + matice (sada) | serva, ložiska, skořepiny | 1 | 250 |
| Kuličková ložiska (10 ks) | volné strany kloubů; typ dle CAD (Microduck 22×16×4 mm) | 1 | 250 |
| Závitové vložky, distanční sloupky | do 3D tisku | 1 | 100 |
| Zkušební závěs / stojan | hliníkový profil nebo PVC rám + lano; robot nikdy netestovat bez závěsu | 1 | 300 |
| Součet společných položek | | | ~3 900 |

Pozdější fáze (nejsou v součtech): Raspberry Pi Zero 2 W ~700 Kč, kamera
~500 Kč, druhá IMU, LiDAR, reproduktor.

### 3.2 Varianta ROBOTIS (DYNAMIXEL XL330-M288-T)

| Položka | Specifikace / poznámka | Ks | Cena Kč |
|---|---|---|---|
| DYNAMIXEL XL330-M288-T | 0,52 Nm @ 5 V, 18 g; v balení 1 kabel X3P 180 mm | 10 | 10 000 (ověřeno €40,20/ks) |
| Budič half-duplex TTL pro ESP32 | 74LVC2G241 nebo 74HC126 dle ROBOTIS referenčního zapojení; 3,3 V logika | 1 | 50 |
| Step-down 5 V / ≥ 15 A pro serva | 10 × 1,47 A stall = 14,7 A teoreticky; 2× Pololu D36V50F5 (5 A) paralelně na větve, nebo buck 5 V / 20 A | 1 | 500 |
| Rozbočovače X3P (3-pin JST EH) | sběrnicové huby nebo vlastní deska | 2 | 200 |
| Kabely X3P různých délek | doplnění k přibaleným | 1 | 150 |
| Volitelně: OpenRB-150 | Arduino-kompatibilní deska s DYNAMIXEL TTL, pro ladění a Dynamixel Wizard | 1 | 800 |
| Volitelně: U2D2 + U2D2 Power Hub | oficiální USB rozhraní pro Dynamixel SDK a Wizard | 1 | 2 050 |
| Součet bez volitelných | | | ~10 900 |
| Součet s OpenRB-150 | | | ~11 700 |
| Celkem se společnými položkami | | | ~14 800 (~15 600 s OpenRB) |

Poznámky: XL330 potřebuje 5 V větev s velkou rezervou, protože stall proud
všech serv přesahuje 14 A. Reálný odběr při chůzi bude 3–5 A, ale zdroj musí
zvládnout špičky bez poklesu napětí (jinak serva resetují). Alternativou k
step-downu je 1S LiPo + boost, což ale zhoršuje účinnost.

### 3.3 Varianta Waveshare (ST3215, 7,4 V)

| Položka | Specifikace / poznámka | Ks | Cena Kč |
|---|---|---|---|
| Waveshare ST3215 Serial Bus Servo 19,5 kg (7,4 V) | 1,9 Nm, magnetický enkodér 4096, ~60 g; kabel v balení | 10 | 6 480 (ověřeno 648/ks) |
| Waveshare Serial Bus Servo Driver Board | TTL sběrnice pro ESP32 UART; vstup 6–12 V | 1 | 148 (ověřeno) |
| Servo kabely 3-pin, různé délky | doplnění k přibaleným | 1 | 100 |
| Volitelně: Waveshare Servo Driver with ESP32 | integrovaný ESP32 + sběrnice + napájení; může nahradit DevKit i adaptér | 1 | 500 |
| Součet | | | ~6 730 |
| Celkem se společnými položkami | | | ~10 600 |

Poznámky: serva běží přímo z 2S LiPo, odpadá výkonový step-down. Pojistku
dimenzovat na 15 A; při stall všech serv teoretické maximum 27 A, reálně při
chůzi 4–8 A. Waveshare má české skladové zastoupení (LaskaKit), reklamace
řeší česky.

### 3.4 Varianta Feetech přímo / no-name (STS3215, 7,4 V)

| Položka | Specifikace / poznámka | Ks | Cena Kč |
|---|---|---|---|
| Feetech STS3215 7,4 V | totéž servo jako ST3215; oficiální Feetech store na AliExpress | 10 | 3 800 (~380/ks) |
| Feetech FE-URT-1 nebo generická TTL bus deska | USB + UART TTL sběrnice; lze i Waveshare adaptér 148 Kč | 1 | 250 |
| Servo kabely 3-pin, různé délky | | 1 | 100 |
| Rezerva na dopravu / celní poplatky | u zásilek nad 150 € se počítá clo | 1 | 400 |
| Součet | | | ~4 550 |
| Celkem se společnými položkami | | | ~8 450 |

Poznámky: nejlevnější varianta, ale dodání 2–4 týdny, reklamace přes Čínu a
riziko klonů od jiných prodejců. Kupovat pouze z oficiálního Feetech
obchodu; ověřit, že jde o STS3215 (magnetický enkodér), nikoli SCS15 nebo
STS3032. Pro první bench test se vyplatí koupit 1 ks lokálně (Waveshare) a
zbytek dovézt.

### 3.5 Přehled variant spodku

| | ROBOTIS XL330 | Waveshare ST3215 | Feetech STS3215 přímo |
|---|---|---|---|
| Cena serv (10 ks) | 10 000 | 6 480 | 3 800 |
| Celkem se společným základem | ~14 800 | ~10 600 | ~8 450 |
| Hmotnost 10 serv | 180 g | ~600 g | ~600 g |
| Napájení serv | 5 V step-down ≥ 15 A | 2S přímo | 2S přímo |
| Kompatibilita se simulátorem Microduck | ano | ne (Open Duck Playground) | ne (Open Duck Playground) |
| Dostupnost náhradních dílů | EU 24–48 h, ~1 000 Kč | CZ sklad, ~650 Kč | Čína 2–4 týdny, ~380 Kč |
| Riziko | cena, výkon na hraně | hmotnost, velikost robota | dodání, záruka, klony |

## 4. Napájení a bezpečnost (platí pro všechny varianty)

- Nouzové vypnutí musí být fyzické (vypínač nebo XT60 klíč), nezávislé na
  firmware.
- Pojistka na hlavní větvi serv; ESP32 napájet z vlastního bucku, aby pokles
  napětí na servech nerestartoval řídicí desku.
- Před připojením více serv otestovat jedno servo: ping, čtení polohy,
  napětí, teploty a proudu/zátěže, pohyb v úzkém limitu, torque-off a
  command timeout.
- Nikdy nespouštět chůzi bez závěsu a bez možnosti okamžitého odpojení
  baterie.

## 5. Zdroje

- LaskaKit – Waveshare: `https://www.laskakit.cz/waveshare/`
- LaskaKit – ST3215 30 kg: `https://www.laskakit.cz/en/waveshare-st3215-serial-bus-servo-30kg/`
- LaskaKit – SC09: `https://www.laskakit.cz/en/waveshare-sc09-serial-bus-servo-2-3kg-300/`
- Generation Robots – XL330-M288-T: `https://www.generationrobots.com/en/403817-dynamixel-xl330-m288-t-servo-motor.html`
- ROBOTIS e-Manual XL330-M288-T: `https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/`
- Waveshare wiki ST3215: `https://www.waveshare.com/wiki/ST3215_Servo`
- Open Duck Mini v2: `https://github.com/apirrone/Open_Duck_Mini`
- Open Duck Playground: `https://github.com/apirrone/Open_Duck_Playground`
- Microduck: `https://pollen-robotics.com/microduck/`
