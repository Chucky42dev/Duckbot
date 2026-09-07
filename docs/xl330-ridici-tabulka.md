# XL330-M288-T: nákup, Dynamixel Wizard a řídicí tabulka (CZ/EN)

Datum: 7. 9. 2026. Anglické pojmy jsou ponechány záměrně – v manuálu, ve
Wizardu i v kódu se s nimi pracuje anglicky. České vysvětlení je vedle, aby se
daly naučit oba tvary. Ceny z Generation Robots byly ověřeny v den sepsání,
přepočet cca 25 Kč/€.

## 1. Kde koupit (Where to buy)

První nákup (first purchase) je jedno servo a OpenRB-150 – a přesně to
prodává ROBOTIS jako **OpenRB-150 Starter Kit** (kód 902-0184-000). Český
oficiální prodejce **ROBOTIS CZ Store by MegaRobot** ho má skladem za
1 194 Kč s DPH (986,85 Kč bez DPH), což je zhruba polovina ceny obou dílů
z Generation Robots. V kitu nejsou baterie, USB kabel k desce ani napájecí
kabel.

Serva řady X mají dva konektory a řetězí se za sebou (daisy chain), OpenRB-150
má čtyři porty – pro tři serva jeřábu tedy **není potřeba hub**.

| Položka (Item) | Obchod | Cena | Odkaz |
|---|---|---|---|
| **OpenRB-150 Starter Kit** (OpenRB-150 + XL330-M288-T) – doporučený první nákup | robotis.cz (ROBOTIS CZ Store by MegaRobot, skladem) | **1 194 Kč** s DPH | [1] |
| OpenRB-150 Starter Kit | ROBOTIS US | $49,90 + doprava, DPH, clo | [2] |
| DYNAMIXEL XL330-M288-T (1 ks, v balení 1 kabel X3P 180 mm) | robotis.cz | **622 Kč** s DPH (513,85 bez DPH) | [1] |
| OpenRB-150 Embedded Controller | robotis.cz | **648 Kč** s DPH (535,35 bez DPH) | [1] |
| DYNAMIXEL XL330-M288-T | Generation Robots (FR, EU, 24–48 h) | €40,20 ≈ 1 000 Kč | [3] |
| OpenRB-150 Embedded Controller | Generation Robots | €43,47 ≈ 1 090 Kč | [4] |
| 10× kabel X3P 180 mm (convertible) | Generation Robots | €22,78 ≈ 570 Kč | [5] |
| 10× kabel X3P 240 mm | Generation Robots | €31,20 ≈ 780 Kč | [6] |
| XL330-M288-T přímo od výrobce | ROBOTIS US ($23,90 + doprava, DPH, clo; 20 dní) | ~700–800 Kč | [7] |
| OpenRB-150 přímo od výrobce | ROBOTIS US | $24,90 + doprava, DPH, clo | [8] |
| Alternativní EU prodejce | RoboSavvy (UK, po brexitu clo) | – | [9] |
| Přehled všech kabelů | Generation Robots – Dynamixel cables | – | [10] |

Odkazy k nákupu:

- [1] `https://www.robotis.cz/176-openrb-150-starter-kit` (ostatní položky
  přes vyhledávání v obchodě)
- [2] `https://www.robotis.us/openrb-150-starter-kit/`
- [3] `https://www.generationrobots.com/en/403817-dynamixel-xl330-m288-t-servo-motor.html`
- [4] `https://www.generationrobots.com/en/404029-openrb-150-embedded-controller-arduino-compatible.html`
- [5] `https://www.generationrobots.com/en/402896-pack-of-10-dynamixel-x3p-cables-convertible.html`
- [6] `https://www.generationrobots.com/en/403191-10-x-180-mm-cable-x3p.html`
- [7] `https://www.robotis.us/dynamixel-xl330-m288-t/`
- [8] `https://www.robotis.us/openrb-150/`
- [9] `https://robosavvy.co.uk/robotis-openrb-150.html`
- [10] `https://www.generationrobots.com/en/268-dynamixel-cables`

Pozor na konektory (connectors): řada X používá **X3P** (JST EH, rozteč 2,5 mm).
Starší „3P" hub a kabely pro AX/MX (Molex) do XL330 nepasují. Kupovat jen
položky s označením X3P nebo „for Dynamixel X series (TTL)". Kabel přibalený
k servu na první kroky stačí; balení 10 ks kupovat až s dalšími servy.

Z běžných českých e-shopů (Botland, RPishop, HWKitchen, LaskaKit) Dynamixel
nikdo nevede. Cesta v ČR je robotis.cz („ROBOTIS CZ Store by MegaRobot"),
prověřeno 8. 9. 2026: provozovatel INMENET13 s.r.o., IČO 01890280, DIČ
CZ01890280, nám. Jiřího z Lobkovic 2164/3, Praha 3; v ARES založena
12. 7. 2013, aktivní plátce DPH, bez insolvence. Tel. +420 721 774 776,
info@robotis.cz. Je to malý dovozce zaměřený na školy (megarobot.cz je druhý
e-shop téhož provozovatele): soukromníci platí 100 % předem, dobírka není,
doprava Zásilkovna / PPL / TopTrans. Před první objednávkou se vyplatí zavolat
a ověřit skladovost. Generation Robots (FR) a Mouser EU jsou záloha pro
položky, které robotis.cz nemá.

## 2. Dynamixel Wizard 2.0 – instalace a první spuštění

Wizard je oficiální program ROBOTISu, který zobrazí řídicí tabulku (control
table) každého serva živě a umožní ji měnit bez psaní kódu. Je to krok 1
roadmapy.

Požadavky (requirements): Windows 10/11 64-bit, Linux Ubuntu 22.04/24.04
nebo macOS 13+.

1. Stáhnout instalátor: `https://www.robotis.com/service/download.php?no=1670`
   (položka „DYNAMIXEL Wizard 2.0 – Windows X64"). Dokumentace:
   `https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/`.
2. Spustit instalátor a projít průvodce (setup wizard). Na Linuxu ještě
   `sudo usermod -aG dialout <uživatel>` a restart.
3. Připojit OpenRB-150 přes USB. Z výroby má nahraný sketch
   `usb_to_dynamixel`, takže funguje jako USB-to-Dynamixel most (bridge) –
   Windows ho uvidí jako sériový port COMx. U2D2 není potřeba.
4. Zapojit servo do jednoho z portů DYNAMIXEL na OpenRB-150. Kabely
   připojovat jen při vypnutém napájení („Do not connect or disconnect
   DYNAMIXEL cables while power is being supplied").
5. Ve Wizardu: `Tools > Options` (F4) – nastavit Protocol 2.0, vybrat port
   COMx, baudrate 57600 (výchozí, default) a rozsah ID 0–20 (rychlejší sken).
6. `Device > Scan` (skenovat). Servo se objeví vlevo jako ID 1, model
   XL330-M288-T.
7. Kliknout na servo, v prostředním sloupci je řídicí tabulka. Hodnoty se
   mění posuvníkem (slider), kolečkem, šipkami nebo přepsáním a potvrzením
   Enter.
8. Změna ID: buď přepsat položku `ID` (servo musí mít `Torque Enable = 0`,
   protože EEPROM je při zapnutém momentu zamčená), nebo `Tools > ID
   Inspection` pro více serv se stejným ID.
9. Aktualizace firmwaru (firmware update) a obnova (recovery) jsou v menu
   Tools; během nich nikdy neodpojovat napájení.

Napájení z USB (5 V) stačí pro jedno XL330 bez zátěže. Jakmile jeřáb něco
zvedá, nebo jsou serva tři, napájet přes svorky VIN (3,7–12,6 V) – ale **XL330
snese max. 6 V**, takže na VIN patří 5 V zdroj nebo 1S LiPo (3,7–4,2 V), nikdy
2S. OpenRB-150 dává na porty DYNAMIXEL max. 3 A.

## 3. OpenRB-150 pro Arduino IDE (krok 2 roadmapy)

- MCU SAMD21 Cortex-M0+ 48 MHz, 256 kB flash, 32 kB RAM; I/O jen 3,3 V.
- Čtyři porty DYNAMIXEL TTL až 1 Mb/s; napájení serv spínané FETem s LED.
- Arduino IDE: `File > Preferences > Additional Boards Manager URLs` přidat
  `https://raw.githubusercontent.com/ROBOTIS-GIT/OpenRB-150/master/package_openrb_index.json`,
  pak `Tools > Board > Boards Manager` nainstalovat „Arduino SAMD" a
  „OpenRB", v Library Manageru knihovnu **DYNAMIXEL2Arduino**.
- Příklady (examples) knihovny: `scan_dynamixel`, `position_mode`,
  `current_mode`, `read_write_ControlTableItem`. Přesně tyto koncepty jsou
  kroky 2–4 roadmapy.
- Reset dvojklikem přepne do bootloaderu; když se ztratí COM port, tímto se
  vrací.
- Manuál: `https://emanual.robotis.com/docs/en/parts/controller/openrb-150/`

## 4. Řídicí tabulka (Control Table) XL330-M288-T

Zdroj: `https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/` (sekce Control
Table of EEPROM Area / RAM Area). Servo je „paměť s adresami": čtením a
zápisem položek (items) na dané adrese se čte stav a řídí pohyb.

Dvě oblasti (areas):

- **EEPROM Area** – nastavení, které přežije vypnutí (ID, limity, režim).
  Zapisovat lze jen při `Torque Enable = 0`. Životnost zápisů je omezená,
  neměnit v běhu.
- **RAM Area** – hodnoty pro provoz (cíle, aktuální stav, zesílení). Po vypnutí
  se vrátí na výchozí.

Jednotky (units): 1 pulse = 1/4096 otáčky ≈ 0,088°; rychlost 0,229 rev/min
(otáčky za minutu); proud 1 mA; napětí 0,1 V; teplota 1 °C.

Hvězdička * = položka důležitá pro jeřáb v0 a bezpečnost.

### 4.1 EEPROM Area (trvalé nastavení)

| Adr. | Data Name (EN) | Česky / význam | B | R/W | Výchozí | Jednotka |
|---|---|---|---|---|---|---|
| 0 | Model Number | Číslo modelu; 1200 = XL330-M288 | 2 | R | 1200 | – |
| 2 | Model Information | Informace o modelu | 4 | R | – | – |
| 6 | Firmware Version | Verze firmwaru | 1 | R | – | – |
| 7 | * ID | Identifikátor serva na sběrnici; 0–252, 254 = broadcast (všem) | 1 | RW | 1 | – |
| 8 | * Baud Rate | Přenosová rychlost: 0 = 9 600, 1 = 57 600, 2 = 115 200, 3 = 1 M, 4 = 2 M, 5 = 3 M, 6 = 4 M | 1 | RW | 1 | – |
| 9 | Return Delay Time | Zpoždění odpovědi serva; 250 × 2 µs = 500 µs, pro rychlou sběrnici nastavit 0 | 1 | RW | 250 | 2 µs |
| 10 | Drive Mode | Režim pohonu: bit 0 obrácený směr (reverse), bit 2 časový profil (time-based profile), bit 3 torque on by goal update | 1 | RW | 0 | – |
| 11 | * Operating Mode | Provozní režim (viz 4.3); výchozí 3 = řízení polohy | 1 | RW | 3 | – |
| 12 | Secondary (Shadow) ID | Vedlejší ID – více serv reaguje na jeden zápis; 255 = vypnuto | 1 | RW | 255 | – |
| 13 | Protocol Type | Typ protokolu; 2 = Protocol 2.0 | 1 | RW | 2 | – |
| 20 | Homing Offset | Posun nuly – přičte se k poloze, umožní nastavit „nulu" jeřábu | 4 | RW | 0 | pulse |
| 24 | Moving Threshold | Prah rychlosti, pod kterým se servo považuje za stojící (příznak Moving) | 4 | RW | 10 | 0,229 rpm |
| 31 | * Temperature Limit | Teplotní limit; při překročení chyba a vypnutí (Shutdown) | 1 | RW | 70 | °C |
| 32 | * Max Voltage Limit | Horní napěťový limit (70 = 7,0 V) | 2 | RW | 70 | 0,1 V |
| 34 | * Min Voltage Limit | Dolní napěťový limit (35 = 3,5 V) | 2 | RW | 35 | 0,1 V |
| 36 | PWM Limit | Limit PWM (885 = 100 %) | 2 | RW | 885 | 0,113 % |
| 38 | * Current Limit | Proudový limit – strop pro Goal Current a režim 5; pro jeřáb snížit (např. 600 mA) | 2 | RW | 1750 | mA |
| 44 | * Velocity Limit | Rychlostní limit; 445 ≈ 102 rpm | 4 | RW | 445 | 0,229 rpm |
| 48 | * Max Position Limit | Horní polohový limit v režimu 3; pro jeřáb zúžit | 4 | RW | 4095 | pulse |
| 52 | * Min Position Limit | Dolní polohový limit v režimu 3 | 4 | RW | 0 | pulse |
| 60 | Startup Configuration | Konfigurace při startu: bit 0 zapnout moment po startu, bit 1 obnovit RAM | 1 | RW | 0 | – |
| 62 | PWM Slope | Strmost náběhu PWM – tlumí rázy | 1 | RW | 140 | 1,977 mV/ms |
| 63 | * Shutdown | Které chyby vypnou moment (bitová maska, viz 4.4); 53 = přepětí/podpětí, přehřátí, zkrat, přetížení | 1 | RW | 53 | – |

### 4.2 RAM Area (provozní hodnoty)

| Adr. | Data Name (EN) | Česky / význam | B | R/W | Výchozí | Jednotka |
|---|---|---|---|---|---|---|
| 64 | * Torque Enable | Zapnutí momentu: 1 = servo drží a hýbe se, EEPROM zamčená; 0 = volné (torque off = nouzové uvolnění) | 1 | RW | 0 | – |
| 65 | LED | Kontrolka; 1 = svítí | 1 | RW | 0 | – |
| 68 | Status Return Level | Kdy servo odpovídá: 0 jen na Ping, 1 jen na Read, 2 na všechno | 1 | RW | 2 | – |
| 69 | Registered Instruction | Čeká zaregistrovaná instrukce (Reg Write → Action) | 1 | R | 0 | – |
| 70 | * Hardware Error Status | Stav hardwarové chyby – bity jako v Shutdown (4.4); nenulové = servo se vypnulo a je nutný reboot | 1 | R | 0 | – |
| 76 | Velocity I Gain | Integrační zesílení rychlostního regulátoru | 2 | RW | 1600 | – |
| 78 | Velocity P Gain | Proporcionální zesílení rychlostního regulátoru | 2 | RW | 180 | – |
| 80 | Position D Gain | Derivační zesílení polohového PID | 2 | RW | 0 | – |
| 82 | Position I Gain | Integrační zesílení polohového PID | 2 | RW | 0 | – |
| 84 | Position P Gain | Proporcionální zesílení polohového PID – „tuhost"; nižší = měkčí | 2 | RW | 400 | – |
| 88 | Feedforward 2nd Gain | Dopředné zesílení od zrychlení | 2 | RW | 0 | – |
| 90 | Feedforward 1st Gain | Dopředné zesílení od rychlosti | 2 | RW | 0 | – |
| 98 | * Bus Watchdog | Hlídač sběrnice: 1–127 × 20 ms; když v té době nepřijde zápis, servo zastaví a Goal položky odmítá; 0 = vypnuto, −1 = vypršel | 1 | RW | 0 | 20 ms |
| 100 | Goal PWM | Cílové PWM (režim 16) | 2 | RW | – | – |
| 102 | Goal Current | Cílový proud (režim 0) nebo strop proudu (režim 5) | 2 | RW | – | mA |
| 104 | Goal Velocity | Cílová rychlost (režim 1) | 4 | RW | – | 0,229 rpm |
| 108 | * Profile Acceleration | Zrychlení pohybového profilu; 0 = bez omezení (ráz). Pro jeřáb nastavit | 4 | RW | 0 | 214,577 rev/min² |
| 112 | * Profile Velocity | Rychlost pohybového profilu; 0 = maximum. Pro jeřáb omezit | 4 | RW | 0 | 0,229 rpm |
| 116 | * Goal Position | Cílová poloha (režim 3/5) – musí být mezi Min a Max Position Limit | 4 | RW | – | pulse |
| 120 | Realtime Tick | Čítač času v servu (přetéká po 32 767 ms) | 2 | R | – | ms |
| 122 | Moving | 1 = servo se pohybuje | 1 | R | 0 | – |
| 123 | Moving Status | Stav pohybu: bit 0 In-Position (dojelo), bit 3 Following Error (nestíhá), bity 4–5 typ profilu | 1 | R | 0 | – |
| 124 | Present PWM | Aktuální PWM | 2 | R | – | – |
| 126 | * Present Current | Aktuální proud – XL330 ho měří na vstupu napájení, ne ve vinutí; roste se zátěží → detekce přetížení jeřábu | 2 | R | – | mA |
| 128 | Present Velocity | Aktuální rychlost | 4 | R | – | 0,229 rpm |
| 132 | * Present Position | Aktuální poloha (0–4095 v režimu 3) | 4 | R | – | pulse |
| 136 | Velocity Trajectory | Plánovaná rychlost dle profilu | 4 | R | – | 0,229 rpm |
| 140 | Position Trajectory | Plánovaná poloha dle profilu | 4 | R | – | pulse |
| 144 | * Present Input Voltage | Vstupní napětí (50 = 5,0 V) – pokles pod Min Voltage Limit = chyba | 2 | R | – | 0,1 V |
| 146 | * Present Temperature | Teplota serva | 1 | R | – | °C |
| 147 | Backup Ready | Záloha nastavení připravena | 1 | R | – | – |
| 168–222 | Indirect Address 1–28 | Nepřímé adresy – umožní sestavit vlastní blok položek pro jedno hromadné čtení (Sync Read) | 2 | RW | 224–251 | – |
| 224–251 | Indirect Data 1–28 | Nepřímá data – hodnoty položek z Indirect Address | 1 | RW | 0 | – |

### 4.3 Operating Mode (provozní režimy)

| Hodnota | Název (EN) | Česky | Použití na jeřábu |
|---|---|---|---|
| 0 | Current Control Mode | Řízení proudu (momentu) | měření, „měkký" naviják |
| 1 | Velocity Control Mode | Řízení rychlosti (kolo) | naviják bez koncové polohy |
| 3 | Position Control Mode | Řízení polohy v jedné otáčce (0–4095), výchozí | výložník, otoč – kroky 2–6 |
| 4 | Extended Position Control Mode | Rozšířená poloha, více otáček (±256) | naviják s odměřením délky lana |
| 5 | Current-based Position Control Mode | Poloha s omezením proudu | bezpečné zvedání: servo nikdy nepřekročí Goal Current |
| 16 | PWM Control Mode | Přímé PWM (napětí) | jen experimenty |

Změna režimu jde jen při `Torque Enable = 0` (EEPROM).

### 4.4 Shutdown / Hardware Error Status – bity

| Bit | Název (EN) | Česky | Ve výchozím Shutdown (53) |
|---|---|---|---|
| 0 | Input Voltage Error | Chyba vstupního napětí (mimo Min/Max Voltage Limit) | ano |
| 2 | Overheating Error | Přehřátí (nad Temperature Limit) | ano |
| 3 | Motor Encoder Error | Chyba enkodéru motoru | ne |
| 4 | Electrical Shock Error | Elektrický zkrat / proudová špička | ano |
| 5 | Overload Error | Přetížení – dlouhodobě vysoký proud | ano |

Po chybě servo vypne moment a LED bliká; obnoví se až příkazem Reboot nebo
vypnutím napájení. Na jeřábu je tedy „Overload" očekávaná situace, ne
porucha – proto je lepší přetížení odhalit dřív pomocí Present Current.

## 5. Slovníček pojmů (Glossary)

| English | Česky | Poznámka |
|---|---|---|
| actuator / servo | aktuátor / servo | pohonná jednotka s regulátorem |
| torque | (točivý) moment, síla otáčení | Nm nebo kg·cm; torque on/off = zapnout/vypnout držení |
| stall torque / stall current | moment / proud při zablokování | maximum, které servo dá těsně před zastavením |
| goal / present | cílový / aktuální (současný) | Goal Position vs. Present Position |
| limit / threshold | limit, mez / prah | limit se nesmí překročit; prah přepíná stav |
| offset | posun, ofset | Homing Offset = posun nuly |
| pulse / tick | pulz (krok enkodéru) / tik | 4096 pulzů na otáčku |
| revolution (rev), rpm | otáčka, otáčky za minutu | rev/min |
| encoder | enkodér, snímač polohy | v XL330 bezkontaktní magnetický, absolutní |
| control table | řídicí tabulka | paměť serva s adresovanými položkami |
| item / address / size | položka / adresa / velikost (v bajtech) | „item at address 116, size 4" |
| EEPROM / RAM area | trvalá / provozní oblast | EEPROM přežije vypnutí |
| read / write | číst / zapsat | instrukce Read (0x02) a Write (0x03) |
| ping | ping – „jsi tam?" | instrukce 0x01, servo odpoví modelem a firmwarem |
| sync read / sync write | hromadné čtení / zápis více serv jedním paketem | důležité pro více kloubů |
| instruction packet / status packet | paket instrukce (z řídicí desky) / stavový paket (odpověď) | základ Protocolu 2.0 |
| CRC | kontrolní součet | chrání paket proti chybě přenosu |
| baud rate | přenosová rychlost (baud) | 57 600 výchozí, 1 M pro robota |
| half-duplex | poloduplex | jeden vodič pro oba směry, mluví vždy jen jeden |
| TTL bus | sběrnice TTL | 3 vodiče: GND, VDD, DATA |
| daisy chain | řetězení za sebou | servo → servo → servo, žádný hub |
| ID / broadcast ID | identifikátor / všeobecné ID (254) | broadcast oslovuje všechna serva |
| watchdog | hlídač (časový) | vyprší → bezpečný stav |
| fail-safe / safe state | bezpečné selhání / bezpečný stav | co se stane, když spojení vypadne |
| heartbeat | tlukot srdce – pravidelný „žiju" signál | krok 7 roadmapy |
| firmware | firmware (program v servu / desce) | update / recovery |
| bootloader | zavaděč | dvojklik na reset OpenRB-150 |
| operating mode | provozní režim | poloha, rychlost, proud, PWM |
| profile velocity / acceleration | profilová rychlost / zrychlení | tvar pohybu – rampa místo skoku |
| P / I / D gain | zesílení proporcionální / integrační / derivační | ladění regulátoru |
| feedforward | dopředná vazba | přidá akci předem podle plánu, ne až podle chyby |
| overload / overheating | přetížení / přehřátí | chybové bity |
| reboot | restart serva | jediná cesta z Hardware Error |
| hub | rozbočovač | pro X3P u tří serv nepotřebný |
| connector / cable | konektor / kabel | X3P = JST EH 2,5 mm |
| power supply / VIN | napájecí zdroj / vstupní napájení | XL330 max. 6 V |

## 6. Zdroje

- XL330-M288-T e-Manual (control table): `https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/`
- XL330-M288-T v novém ROBOTIS Docs: `https://docs.robotis.com/docs/dxl/model_reference/x_series/xl_series/xl330-m288/`
- DYNAMIXEL Protocol 2.0: `https://emanual.robotis.com/docs/en/dxl/protocol2/`
- Dynamixel Wizard 2.0: `https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/`
- Wizard download: `https://www.robotis.com/service/download.php?no=1670`
- OpenRB-150: `https://emanual.robotis.com/docs/en/parts/controller/openrb-150/`
- DYNAMIXEL2Arduino: `https://github.com/ROBOTIS-GIT/Dynamixel2Arduino`
- Generation Robots – XL330-M288-T: `https://www.generationrobots.com/en/403817-dynamixel-xl330-m288-t-servo-motor.html`
- Generation Robots – OpenRB-150: `https://www.generationrobots.com/en/404029-openrb-150-embedded-controller-arduino-compatible.html`
