# Microduck a návrh Duckbotu

## Co je na Microducku technicky zajímavé

Podle oficiálních materiálů Pollen Robotics je Microduck přibližně 25 cm vysoký
robot s hmotností okolo 800 g. Používá 15 servomotorů, kameru, LiDAR, dvě IMU a
řídicí smyčku s frekvencí 50 Hz. Na palubě běží Rockchip RK3566 a pohybové
politiky se načítají jako ONNX modely.

Nejde tedy o jeden program v Arduinu. Systém má několik vrstev:

```text
hlas, ovladač, kamera nebo aplikace
                |
          příkaz / záměr
                |
       řídicí počítač robota
       stav, politika, bezpečnost
                |
       realtime řízení serv
                |
       serva + IMU + další senzory
```

Oficiální repozitář je dobrý hlavně jako studijní materiál pro architekturu.
Motorovou sběrnici a bezpečnost vlastní jedna řídicí služba, ostatní části jí
posílají záměry typu „jdi dopředu“ nebo „sedni si“, nikoli přímé zápisy do
motorů. To je důležitá vlastnost, kterou bychom měli převzít i pro Duckbot.

## Co umí hned

Oficiální Microduck uvádí tyto připravené pohyby:

- chůze podle rychlosti a směru,
- sednutí a postavení,
- kopnutí do míče,
- sebrání jednoduchého předmětu zobákem,
- jízda na kolečkách,
- postavení se po pádu,
- zvukové reakce a kvákání.

To neznamená, že každý nový robot tyto schopnosti automaticky získá. Jsou
výsledkem konkrétní mechaniky, kalibrace, senzorů a natrénovaných politik.
U vlastního Duckbotu musíme každou schopnost nejdřív naprogramovat nebo
natrénovat.

## Kam se podívat po simulátoru

1. **Microduck simulátor:**
   [Hugging Face Microduck Simulator](https://huggingface.co/spaces/pollen-robotics/microduck-simulator)

   Začal bych zde. Nejdřív si vyzkoušej model, scénu, ovládání a chování po
   pádu. Zapiš si, jaké vstupy simulátor používá a jaké akce vrací. Tyto rozměry
   budou později určovat firmware i síť pro Duckbot.

2. **Oficiální runtime a dokumentace:**
   [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck)

   Projdi hlavně README, `docs/design/architecture.md`,
   `docs/design/robotd-design.md`, `docs/robot/cheatsheet.md` a
   `docs/policy-manifest.md`.

3. **Sim2real a RL:**
   Oficiální web odkazuje na samostatný projekt `microduck_rl`. V době průzkumu
   byl přímý odkaz na GitHubu nedostupný, takže je lepší začít Hugging Face
   simulátorem a dokumentací hlavního repozitáře. Neber název repozitáře jako
   záruku, že je stále veřejný nebo že odpovídá aktuální verzi runtime.

4. **MuJoCo:**
   [MuJoCo documentation](https://mujoco.readthedocs.io/en/stable/)

   To je fyzikální simulátor. Nejprve stačí umět načíst model, spustit scénu,
   číst stav kloubů a IMU a posílat cíle do serv. PPO a vlastní trénink přijdou
   až po ověření, že model odpovídá skutečné mechanice.

## Jak bych programoval Duckbot

### ESP32: bezpečný realtime základ

ESP32 by měl vlastnit nízkoúrovňové řízení:

- čtení IMU,
- řízení servomotorů,
- kalibraci nulových poloh,
- omezení úhlů a rychlosti,
- detekci pádu,
- nouzové vypnutí serv,
- watchdog a timeout příkazů.

ESP32 nesmí čekat na Wi-Fi, hlasový model ani pomalý server. Když nepřijde
příkaz například 200 ms, musí přejít do bezpečného režimu a zastavit pohyb.

Pro první pokusy stačí MPU6050. Pro stabilnější měření bych později použil
BNO085 nebo podobnou IMU s vlastní fúzí senzorů. Akcelerometr sám o sobě při
chůzi nestačí: dynamika pohybu způsobuje zrychlení, které se plete s gravitací.

### Raspberry Pi nebo jiný SBC: mozek a komunikace

Raspberry Pi 5, případně podobný Linuxový počítač, by řešil:

- MuJoCo a testovací nástroje,
- inference ONNX politiky,
- kameru a rozpoznávání objektů,
- hlasové rozpoznávání,
- převod vysokých příkazů na bezpečné záměry,
- logování a aktualizace.

ESP32 a SBC mohou komunikovat přes USB sériovou linku, UART nebo CAN. Pro první
verzi je nejjednodušší USB serial s řádky JSON. Až bude protokol stabilní, lze
přejít na binární rámce nebo CAN.

Příklad příkazu, který má smysl posílat:

```json
{"type":"intent","mode":"stand","forward":0.0,"turn":0.0,"ttl_ms":200}
```

Příklad příkazu, který bych neposílal z hlasového asistenta ani z Wi-Fi:

```json
{"servo":7,"angle":1.42}
```

Přímé úhly musí zůstat pod kontrolou bezpečnostní vrstvy na ESP32 nebo v
lokálním řídicím procesu.

## Co bude Duckbot umět v jednotlivých etapách

### Duckbot v0.1: stolní prototyp

- číst náklon a teplotu IMU,
- řídit dva až čtyři servomotory,
- nastavit bezpečnou nulovou polohu,
- reagovat na tlačítko a nouzové vypnutí,
- posílat telemetrii do počítače.

Tady ještě netrénujeme chůzi. Cílem je ověřit napájení, mechaniku, servo limity
a komunikaci.

### Duckbot v0.2: stabilní stoj

- vícekloubové nohy,
- stoj podle předem připravené pózy,
- kompenzace náklonu pomocí jednoduchého PID regulátoru,
- detekce pádu,
- bezpečné uvolnění nebo vypnutí motorů.

Toto je nejdůležitější milník. Když robot bezpečně nestojí, reinforcement
learning pouze urychlí ničení serv a převodů.

### Duckbot v0.3: předprogramovaná chůze

- krok dopředu a dozadu,
- otočení na místě,
- sednutí a postavení,
- ovládání gamepadem,
- záznam kloubů, IMU a příkazů.

Nejdřív použijeme trajectory-based řízení: ručně navržené trajektorie kloubů,
interpolaci a stabilizační korekci. To je levnější a lépe laditelné než okamžité
trénování neurální sítě.

### Duckbot v0.4: simulace a sim2real

- přesný MJCF model v MuJoCo,
- stejné názvy kloubů a stejné pořadí akcí jako ve firmware,
- náhodné tření, hmotnost, zpoždění serv, síla motorů a šum senzorů,
- trénink PPO v simulaci,
- export politiky do ONNX,
- opatrné testování na zavěšeném nebo jištěném robotu.

Teprve tady se dostáváme k principu Microducku: politika neříká „nastav servo
na přesný úhel“, ale z pozorovaného stavu vypočítá další akci. Pozorování může
obsahovat úhly a rychlosti kloubů, orientaci z IMU, rychlost těla a požadovaný
směr chůze.

## Co můžeš robota naučit

### Nejprve klasickým programováním

- stát a sedět,
- reagovat na tlačítka,
- otočit hlavu za zvukem nebo světlem,
- sledovat barevný míček,
- přijet nebo přijít k cíli,
- kvákat podle události,
- bezpečně se zastavit při pádu nebo slabé baterii.

### Později učením v simulaci

- stabilní chůzi,
- sledování rychlosti a směru,
- překonání mírně jiné podlahy,
- kopnutí do míče,
- vstávání z vybraných pádových poloh,
- chování při změně hmotnosti nebo tření.

### Hlasový asistent

Hlasový asistent by měl být vysoká vrstva, ne stabilizační smyčka. Příkaz
„Duckbote, pojď dopředu“ se převede na `forward=0.2`, zatímco ESP32 stále
hlídá náklon, limity a timeout. Příkaz „pojď za mnou“ bude potřebovat kameru
nebo vzdálenostní senzor a vlastní lokální řízení; samotný LLM neumí bezpečně
řídit serva v realtime.

První hlasové příkazy mohou být:

- „stůj“,
- „sedni“,
- „postav se“,
- „jdi dopředu“,
- „otoč se doleva“,
- „kvákni“.

## Doporučené pořadí práce

1. Spustit Microduck simulátor a pochopit pozorování, akce a reset epizody.
2. V Duckbotu rozchodit IMU, jedno servo a telemetrii.
3. Přidat bezpečnostní limity, watchdog a nouzové vypnutí.
4. Postavit stojící mechanismus a změřit skutečné úhly, vůle a odběr.
5. Napsat ruční stoj a jednoduchý krok.
6. Teprve potom vytvořit MJCF model vlastní mechaniky.
7. Porovnat simulovanou a skutečnou odezvu serv.
8. Trénovat nejprve stoj, potom chůzi, nakonec triky jako kopnutí nebo vstávání.
9. Hlas a kameru přidat až nad stabilní pohybový základ.

## Realistické rozhodnutí

Vlastní Duckbot může napodobit hlavní myšlenku Microducku, ale ne jeho hotové
schopnosti za cenu několika ESP32 součástek. Nejtěžší část bude mechanika,
serva, napájení, kalibrace a sim2real. Výhoda vlastního projektu je, že každou
vrstvu pochopíš a můžeš ji měnit.

Microduck bych proto bral jako referenční implementaci a testovací etalon.
Duckbot bych stavěl tak, aby první funkční verze nevyžadovala neurální síť.
Když bude v0.3 bezpečně chodit s ruční trajektorií, bude mít smysl investovat
čas do MuJoCo a PPO.

## Odkazy

- [Microduck: oficiální repozitář](https://github.com/pollen-robotics/microduck)
- [Microduck: oficiální produktová stránka](https://pollen-robotics.com/microduck/)
- [Microduck Simulator na Hugging Face](https://huggingface.co/spaces/pollen-robotics/microduck-simulator)
- [MuJoCo dokumentace](https://mujoco.readthedocs.io/en/stable/)
- [TorchRL PPO dokumentace](https://docs.pytorch.org/rl/main/reference/generated/torchrl.objectives.ClipPPOLoss.html)