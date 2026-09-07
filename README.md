# Duck v0.1

Experimentální platforma pro malou chodící kachnu s ESP32, IMU senzorem a servomotory.

## Cíl první verze

- měřit náklon pomocí IMU,
- řídit servomotory,
- udržet stabilní stoj,
- připravit bezpečný základ pro pozdější chůzi a hlasové příkazy.

## Stav projektu

Projekt je na začátku. Nejprve vznikne malý funkční prototyp, teprve potom složitější mechanika a chůze.

## Simulátor

Ve složce [sim/](sim/) je vlastní MuJoCo model Duckbotu generovaný z parametrů
a jeho verze pro prohlížeč. Viz [sim/README.md](sim/README.md).

```bash
python sim/generate_mjcf.py && python sim/check_model.py   # model + test stoje
cd sim/web && npm install && npm run dev                    # http://localhost:5180
```

## Dokumentace

- [Průzkum Microducku a plán Duckbotu](docs/research-microduck.md)
- [Průzkum ve formátu PDF](docs/research-microduck.pdf)
