# Duckbot simulátor

Vlastní MuJoCo model Duckbotu, generovaný z parametrů. Předlohou je Microduck:
stejný strom 14 kloubů, stejné názvy senzorů, stejný formát pozorování (61)
a akce (14), takže na model půjde později napojit tréninkový kód `microduck_rl`.

Všechny rozměry a hmotnosti jsou **odhad** odvozený z MJCF Microducka. Až bude
skutečný hardware, přepiš [duckbot_params.py](duckbot_params.py) podle
změřeného stroje a model znovu vygeneruj.

## Soubory

| Soubor | Účel |
|---|---|
| `duckbot_params.py` | jediné místo s parametry: rozměry, hmotnosti, serva, rozsahy kloubů, výchozí póza |
| `generate_mjcf.py` | z parametrů vygeneruje `model/duckbot.xml` a `model/duckbot_hold.xml` |
| `check_model.py` | test stoje bez politiky, diagnostika těžiště a kontaktů, render PNG |
| `model/duckbot.xml` | model se **změřenými** zisky serv XL330 (kp 0.55) – pro trénink politiky |
| `model/duckbot_hold.xml` | model s **tuhými** servy (kp 5) – ruční testy a prohlížeč |
| `web/` | simulátor v prohlížeči (MuJoCo WASM + three.js) |

## Python (generování a kontrola)

```bash
pip install mujoco pillow
python sim/generate_mjcf.py     # přegeneruje oba modely
python sim/check_model.py       # test stoje + sim/model/duckbot_hold.png
python sim/check_model.py --sysid   # se změřeným kp 0.55: bez politiky spadne, to je správně
python -m mujoco.viewer --mjcf sim/model/duckbot_hold.xml   # interaktivní 3D okno
```

## Prohlížeč

```bash
cd sim/web
npm install
npm run dev        # http://localhost:5180
```

Ovládání: myš otáčí kameru, slidery nastavují cílové úhly serv, tlačítka
Reset / Pauza / Šťouch / Dřep / Krok na místě, klávesy `R`, mezerník, `P`.
Panel ukazuje přesně těch 61 čísel, která by dostávala politika.

Statická verze pro XAMPP nebo jiný webserver:

```bash
npm run build      # vytvoří sim/web/dist/
```

Obsah `dist/` zkopíruj třeba do `C:\xampp\htdocs\duckbot\` a otevři
`http://localhost/duckbot/`. Stránka nepotřebuje žádný backend.

## Co model umí a neumí

- Umí: stát, držet pózu, reagovat na šťouchnutí, ukázat, co vidí politika.
- Neumí: chodit. „Krok na místě“ je otevřená smyčka bez zpětné vazby z IMU
  a po pár krocích spadne. Přesně tuhle mezeru vyplní natrénovaná politika.

## Proč dva modely

Pollen identifikoval XL330 jako velmi poddajné servo (kp 0.55 Nm/rad). Robot
s takovým servem sám o sobě nestojí; politika mu posílá „virtuální“ cíle až
±10 rad, aby z něj dostala potřebný moment. Pro trénink je tedy nutný
poddajný model (`duckbot.xml`), pro ruční hraní tuhý (`duckbot_hold.xml`).

## Další kroky

1. Ověřit rozměry proti skutečnému CAD modelu Duckbotu.
2. Změřit parametry serv (tuhost, tlumení, max. moment) na jednom XL330.
3. Napojit `microduck_rl` (mjlab) na `duckbot.xml` a natrénovat stoj, potom chůzi.
4. Exportovat politiku do ONNX a spustit ji v `web/` přes onnxruntime-web,
   stejně jako to dělá Microduck sandbox.
