# Duckbot: jeřáb v0 – učební roadmapa

Datum rozhodnutí: 7. 9. 2026. Cesta je cíl: smyslem projektu je naučit se
robota postavit a rozumět mu, ne mít co nejdřív chodící kachnu. Koupený
Microduck zůstává jako možnost později, až bude jasné, co z něj chceme.

## Proč jeřáb a proč Dynamixel

Jeřáb má 2–3 klouby, nemusí držet rovnováhu a nespadne. Přesto na něm jde
vyzkoušet vše, co potřebuje chodící robot: sběrnici, limity, moment vs. délka
ramene, proud jako detekci zátěže, nouzové uvolnění a watchdog.

DYNAMIXEL XL330-M288-T je pro učení lepší než levnější Feetech:

- Dynamixel Wizard zobrazí celou řídicí tabulku serva živě (poloha, proud,
  teplota, limity) – rozumíš servu dřív, než napíšeš první řádek kódu.
- Protocol 2.0 je kompletně zdokumentovaný (rámce, CRC, instrukce) a dá se
  číst po bajtech.
- Hardwarový Bus Watchdog a limity v servu ukazují správný bezpečnostní
  model, který pak napodobíme ve vlastním firmware.
- Zůstává kompatibilita s Microduckem, pokud k němu později dojde.

Podrobné srovnání serv a ceny: `servo-comparison.md`.

## Režim práce

- Kód píše majitel projektu. Claude vysvětluje, co má další krok dělat a
  proč, a dělá review – nepíše kód za něj, pokud o to není výslovně požádán.
- Krok je hotový teprve tehdy, když majitel dokáže vlastními slovy vysvětlit,
  co kód dělá a co běží po drátech.
- Každý krok končí krátkým zápisem do `docs/` (co fungovalo, co ne, naměřené
  hodnoty). Tempo je 3–5× pomalejší než „nech to napsat", a to je v pořádku.

## Nákupní seznam (postupně)

| Položka | K čemu | Kč (orientačně) |
|---|---|---|
| OpenRB-150 Starter Kit = OpenRB-150 + 1× XL330-M288-T (první nákup) | kroky 1–4; deska je Arduino-kompatibilní, napájí XL330 z USB, z výroby funguje jako most pro Dynamixel Wizard | 1 194 (robotis.cz, ověřeno 8. 9. 2026) |
| USB kabel k OpenRB-150 | není v kitu | 100 |
| X3P kabely (balení 10 ks, po kroku 3) | propojení více serv řetězením; hub není potřeba | 570 |
| Závaží, provázek, hák, kuchyňská váha | měření momentu | 200 |
| 2× XL330-M288-T (po kroku 3) | otoč základny, naviják/chapadlo | 1 244 (robotis.cz 622 Kč/ks, ověřeno 8. 9. 2026) |
| Laboratorní zdroj 0–30 V / 5 A | proud v reálném čase, proudový limit jako ochrana | 1 500 |
| PETG, šrouby M2, ložiska, hliníkový profil | rám a díly jeřábu | 700 |
| ESP32-S3 DevKit + budič 74LVC2G241 (po kroku 7) | vlastní řídicí vrstva | 350 |
| Celkem | | ~5 900 |

## Kroky

1. Servo na stole, Dynamixel Wizard: ping, změna ID, ruční pohyb, sledování
   polohy a proudu. Bez kódu. Výstup: popis, co jednotlivé registry znamenají.
   Instalace Wizardu a dvojjazyčná řídicí tabulka: `xl330-ridici-tabulka.md`.
2. První program (OpenRB, Arduino IDE): přečíst polohu a napětí a vypsat je
   na sériový port.
3. Pohyb v limitech a torque-off: zadaný cíl se provede jen v povoleném
   rozsahu; tlačítko okamžitě uvolní servo.
4. Proud jako detekce zátěže: jeřáb zvedá závaží, měří se proud; po překročení
   prahu zastaví. Spočítat moment = síla × délka a porovnat s katalogovými
   0,52 Nm.
5. Druhé servo (otoč základny): koordinovaný pohyb, rychlostní profil, proč
   nesmí jet oba klouby naplno naráz.
6. Třetí servo a stavový automat: najeď – spusť – chytni – zvedni – otoč –
   pusť. První skutečné chování.
7. Heartbeat z PC: řízení z Pythonu přes sériový port; když PC přestane
   posílat, jeřáb do 500 ms zamrzne a uvolní. Odpovídá rozhodnutí 4 v
   `CLAUDE.md`.
8. Přechod na ESP32: totéž jako na OpenRB, ale s vlastním half-duplex
   budičem a PlatformIO.
9. MuJoCo model jeřábu: první porovnání simulace a reality (polohy, časy).
   Most k chodícímu robotu.

Po kroku 9 je vlastníma rukama napsané vše, co `CLAUDE.md` požaduje pro
„jeden aktuátor + bezpečnost", a rozhodnutí kachna vs. Microduck se dělá
s jinou jistotou.

## Bezpečnost i u jeřábu

- Zátěž může spadnout: nezvedat nad nohy ani nad elektroniku.
- Servo se při přetížení zahřívá; sledovat teplotu, používat proudový limit
  zdroje.
- Nouzové uvolnění musí být fyzické tlačítko nebo odpojení napájení, ne jen
  příkaz z PC.

## Odkazy

- XL330-M288-T e-Manual: `https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/`
- OpenRB-150: `https://emanual.robotis.com/docs/en/parts/controller/openrb-150/`
- Dynamixel Wizard 2.0: `https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/`
- Dynamixel Protocol 2.0: `https://emanual.robotis.com/docs/en/dxl/protocol2/`
