# UFM 10mL PROTOTYPE - COMPLETE SCHEMATICS
## April 10, 2026

---

## 1. OVERALL SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     COMPLETE SYSTEM                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐        ┌──────────────────┐
│  12V DC Power    │        │   555 Timer      │
│  Supply (1A)     │───────▶│  Oscillator      │
│                  │        │  1 kHz output    │
└──────────────────┘        └────────┬─────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   ZVS Driver    │
                            │   Circuit       │
                            │ (10-15V peak)   │
                            └────────┬────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
            │  Tungsten    │  │  Glass Vial  │  │  Light       │
            │  Electrodes  │  │  (10mL)      │  │  Detector    │
            │  (Arc)       │  │  +10g Water  │  │  (Photo)     │
            └──────────────┘  └──────────────┘  └──────────────┘
                    │                │                │
                    └────────────┬───┴────────────┬───┘
                                 ▼
                        ┌─────────────────────┐
                        │  Data Acquisition   │
                        │  - Temperature      │
                        │  - Light intensity  │
                        │  - Pressure (opt)   │
                        └──────────┬──────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  Computer/Oscillator │
                        │  FFT Analysis        │
                        │  & Display           │
                        └──────────────────────┘
```

---

## 2. ELECTRICAL SCHEMATICS

### 2A. 12V DC Power Input

```
Wall AC             AC-DC Step Down       12V DC Bus with
120V AC             Transformer           Filtering
───────             + Rectifier                │
(or USB)                                      ▼
   │                    │                 ┌────────┐
   │                    │            ─────┤  +12V  │
   ├─[Fuse 2A]─────────┤            │    └────────┘
   │                    │            │
   │                    ▼            │ ┌───────────┐
   │                 [Bridge]──────┬─┼─┤ C1: 1000μ │
   │                 Rectifier     │ │ │ F (16V)   │
   │                    │          │ │ └───────────┘
   │                    │          ▼ │
   │              ┌─────┴────────────┴──────┐
   │              │ 7812 Voltage Regulator  │
   │              │ (provides clean 12V)    │
   │              └───────────┬─────────────┘
   │                          │
   └──────[Power LED]◄───────(─)GND
                              │
                         ┌────┴────┐
                         │ Ground   │
                         │ Plane    │
                         └──────────┘
```

**Bill of Materials (Power)**:
- Transformer: 12V, 1A minimum
- Bridge rectifier: 4A rated
- 7812 regulator: 1A (TO-220 package)
- C1: 1000μF/16V (electrolytic)
- C2: 100nF (ceramic, across regulator output)
- Fuse: 2A automotive
- LED + 470Ω resistor (power indicator)

---

### 2B. 555 Timer Oscillator Circuit (1 kHz)

```
         +12V
          │
          ├─────[1kΩ R1]─┬─────[100kΩ R2]─┐
          │              │                │
          │         ┌────┼────┐           │
          │         │  8 555  │           │
          │    ┌────┤8       4├──┐        │
          │    │    │         │ │        │
          │    │    │  TIMER  │ │        │
          │    │    │   IC    │ │   ┌────┴────┐
          │    │    │         │ │   │ C1: 10μ │
          │    │    │5       6├─┼───┤ F       │
      ┌───┴────┼────┤       2│ │   └─────┬───┘
      │        │    │       7├─┘         │
      │        │    │       3├──────────(◄)── Output to ZVS
      │        │    └────┤1 │
      │        │         └──┘
      │        │          │
      │        └────────────┴──────┴─ GND
      │
      └─ +12V supply

Frequency calculation:
f = 1.44 / ((R1 + 2*R2) * C1)
f = 1.44 / ((1k + 200k) * 10μ) = 1.44 / 2.01 = ~715 Hz

For exactly 1 kHz, use:
R1 = 1kΩ
R2 = 68kΩ (use 68k + 10k trim pot in series for fine tuning)
C1 = 10μF

Output: Pin 3 (square wave, 0-12V, 1 kHz, 50% duty cycle)
```

**Bill of Materials (555 Timer)**:
- NE555 IC (8-pin DIP)
- R1: 1 kΩ, 1/4W
- R2: 68 kΩ, 1/4W
- R_trim: 10 kΩ trim potentiometer (optional, for fine freq adjustment)
- C1: 10 μF/16V (electrolytic)
- C2: 100 nF (ceramic, bypass across IC power)
- Breadboard or PCB

---

### 2C. ZVS (Zero-Voltage Switching) Driver Circuit

```
Input from 555 Timer (0-12V, 1 kHz square wave)
           │
           ▼
      ┌────────────┐
      │   Base     │
      │ Driver IC  │  (e.g., IR2110 or TL494)
      │ (Gate      │
      │ Driver)    │  - Provides high-current gate pulse
      └──┬─┬───┬──┘  - Isolates logic from power stage
         │ │   │
    ┌────┘ │   └────┐
    │      │        │
    ▼      ▼        │
┌──────────────┐    │
│ MOSFETs or   │◄───┘
│ IGBTs        │  (Parallel pair)
│              │  - Q1 and Q2
│ (ZVS Stage)  │  - Forms half-bridge
└──┬───────┬──┘
   │       │
   │    (GND)
   │
   ▼ (High voltage pulse output
     to arc electrodes)
   
   ┌──────────────┐
   │ LC Tank      │ (Resonant circuit)
   │ Circuit      │ - Ensures zero-voltage switching
   │              │ - L: inductor (~1μH)
   │              │ - C: capacitor (~1nF)
   │              │ - Creates resonance for soft switching
   └──┬───────┬──┘
      │       │
      ▼       ▼
   ┌─────────────┐
   │  High-Volt  │ (Transformer or 
   │  Transformer│ direct output)
   │  (10:1)     │
   └─┬───────┬──┘
     │       │
     ▼       ▼
  ELECTRODE PAIR
  (~100-200V peak)
```

**Bill of Materials (ZVS Driver)**:
- Gate driver IC: IR2110 (high-side/low-side) or TL494
- Power MOSFETs: 2× IRFZ44N or similar (40V rated minimum)
- Resonant inductance: 1 μH ferrite core inductor
- Resonant capacitance: 1 nF ceramic (high-voltage rated)
- High-voltage transformer (if boosting voltage): 10:1 step-up
- Flyback diode: 1N4007 (across transformer primary)
- Snubber capacitors: 10 nF across MOSFET drains

**Alternative (Simpler)**: 
Use a commercial ZVS module (eBay ~$15-30):
- 12V input, 100-200V adjustable output
- Direct AC output suitable for arc
- Pre-tuned resonant tank

---

## 3. ELECTRODE & CHAMBER DESIGN

### 3A. Glass Vial Chamber (10mL)

```
TOP VIEW (looking down)
                    ╔═══════════╗
                    ║           ║
                    ║ Metal Cap ║ (stainless steel,
                    ║ (sealed)  ║  vented with
                    ║           ║  1mm hole)
                    ╚═════╤═════╝
                          │
                    ┌─────┼─────┐
                    │  Sealing  │
                    │  O-ring   │
                    └─────┼─────┘
                          │
                  ╔═══════╩═══════╗
                  ║               ║
              ┌───╫───┐       ┌───╫───┐
              │ ◄──║──► ElectrodePair (tungsten)
              │   ║   │       │   ║   │ Gap: 1mm
              │   ║   │       │   ║   │
              │   ║   └───┐   └───╫───┤
              │   ║       │       ║   │
              │   ╠═══════════════╣   │
              │   ║       10mL    ║   │
              │   ║       Water   ║   │
              │   ║               ║   │
              │   ║  ◄ Light      ║   │
              │   ║    Detective  ║   │
              │   ║    (if used)  ║   │
              │   ║               ║   │
              │   ║  ◄ Thermo-    ║   │
              │   ║    couple     ║   │
              │   ║    (optional) ║   │
              │   ║               ║   │
              │   ║               ║   │
              │   ║               ║   │
              │   ║               ║   │
              │   ║               ║   │
              │   ╚═══════════════╝   │
              │   Glass cylinder      │
              │   (10mL borosilicate)│
              │   Internal diameter: │
              │   ~13mm, Length: ~75mm│
              └───────────────────────┘
                       │
                   ┌───┴────┐
                   │ Sealed  │
                   │ Bottom  │
                   └─────────┘

SIDE VIEW (cross-section)
           Metal Cap (stainless steel)
               │
         ┌─────═════─────┐ ─ 67mm height
         │               │
         │  ┌───────┐    │
         │  │ ◄ ► E │    │ ─ Electrode pair
         │  │   l  │    │   inside vial
     ┌───┼──┤e  e  ├────┼───┐
     │   │  │ c c  │    │   │ ─ Light entry
     │   │  │ t t  │    │   │   (9mm diameter
     │   │  │ r r  │    │   │    window hole
     │   │  │ o o  │    │   │    in side)
     │   │  │ d d  │    │   │
     │   │  │ e e  │    │   │
     │   │  │       │    │   │
     │   │  │       │    │   │
     │   │  │ Water │    │   │
     │   │  │       │    │   │
     │   │  │       │    │   │
     │   │  │       │    │   │
     │   └──┤       ├────┘   │
     │      └───────┘        │
     │      Glass cylinder   │
     │      Borosilicate     │
     │      10mL capacity    │
     │                       │
     └───────────────────────┘
```

**Chamber Specifications**:
- Material: Borosilicate glass (lab-grade)
- Capacity: 10 mL (exact volume important for pressure calc)
- Dimensions: ~13mm ID × 75mm height
- Top cap: Stainless steel (316 or 304), sealed with O-ring
- Vent hole: 1mm diameter (allows pressure release if overpressure)
- Window: 9mm optical-quality hole in side (for light detector entry)
- Material cost: $10-15 (or use existing lab glassware)

**Sources**:
- Search: "10mL glass vial borosilicate lab"
- amazon.com: Lab-grade vials
- ebay: NMR sample tubes (perfect size)

---

### 3B. Electrode Design

```
ELECTRODE ASSEMBLY (detail)

Each electrode:
┌──────────────────┐
│  Tungsten Wire   │ ─ Material: W (melting point 3695K)
│  1.6mm diameter  │ ─ Length: 30mm total
│  (AWG #11)       │ ─ Resistance per cm: ~0.002Ω
└────┬─────────────┘
     │
     ├─ Insulated section (15mm)
     │  (PTFE tubing or mica wrap)
     │
     ├─ Bare tip (10mm inside electrode)
     │  (Submerged in water)
     │
     └─ Connection point (5mm)
        (For electrical lead)

GAP CONFIGURATION:

     Electrode 1          Electrode 2
     (positive)           (negative)
         ║                  ║
      ┌──║──┐           ┌──║──┐
      │  ║  │           │  ║  │
      │  ║  └─ 1mm gap ─┘  ║  │
      │  ║                  ║  │
      └──║──────────────────║──┘
         ║                  ║
      (High V)          (GND)

Mounting:
- Electrodes held in ceramic insulator block (0.5mm per electrode from glass wall)
- Seal: Ceramic-to-glass with high-temperature epoxy
- Electrical connection: Copper wire leads soldered to electrode bases
- Each lead goes to ZVS output (positive/negative or HV direct)
```

**Electrode Bill of Materials**:
- Tungsten rod: 1.6mm diameter (tungsten is cheap, ~$2/meter)
- PTFE tubing: 2mm ID (for insulation)
- Ceramic insulator block: Custom or 3D-printed (or use zirconia spacer)
- High-temp epoxy: For sealing electrodes
- Copper leads: 18 AWG, rated for arc voltage

---

## 4. SENSING & DATA ACQUISITION

### 4A. Temperature Measurement

```
Thermocouple (Type T: Copper-Constantan)
Mounted inside vial, 5mm from electrode gap

         ┌─────────────────────┐
         │    Sealed via       │
         │  High-temp epoxy    │
         │  (doesn't add heat) │
         └──────────┬──────────┘
                    │
           ┌────────┴────────┐
           │                 │
        Copper          Constantan
      (+) lead          (-) lead
           │                 │
           ▼                 ▼
      ┌─────────────────────────┐
      │  K-type Thermocouple    │
      │  Adapter Board          │
      │  (converts mV to temp)  │
      │  0.1°C resolution       │
      └────────────┬────────────┘
                   │
                   ▼
              Oscilloscope
              or ADC
              (computer)

Signal: 
  mV output ≈ 41 μV/°C
  Temperature rise 5-10K → 200-400 μV signal
  Easily measurable at kHz resolution
```

**Temperature Sensor Bill of Materials**:
- Type T thermocouple wire: ~$5 (small quantity)
- MAX31856 thermocouple amplifier module: ~$20 (on eBay)
- Gives 0-3V analog output proportional to temperature
- Digital version available (I2C interface)

---

### 4B. Light Detection (Photon Cascade Signature)

```
UV Photodiode (solar blind, 256-400nm range)

Light path from electrode arc
               │
               ▼
              Glass
              window
               │
              └─ 9mm diameter hole
                 in vial wall
                 │
                 │ (UV photons escape)
                 │
                 ▼
           ┌──────────────┐
           │  Photodiode  │ (SBD, solar blind)
           │  Active area:│ Model: SFH 2701
           │  2mm²        │ 256nm peak response
           └──┬──────────┘
              │
              ├─ Anode (via transimpedance amp)
              │
        ┌─────┴─────┐
        │    I/V    │
   ┌────┤ Converter │────┐
   │    │ OP-AMP    │    │
   │    │ (TL072)   │    │ Gain: 10^6 to 10^7
   │    └────┬──────┘    │ (converts nA to V)
   │         │           │
   │    [Feedback R]     │
   │         │           │
   └─────────┴───────────┘
        Output: 0-5V
        (proportional to
        photon flux)
```

**Light Detector Bill of Materials**:
- UV Photodiode: SFH 2701 (or similar) ~$15
- Transimpedance amplifier: TL072 + resistor feedback ~$5
- 9-pin feedthrough: For window in vial side (or pre-drilled chamber)
- Signal conditioning: Op-amp circuit with ~10^6 V/A gain

**Alternative (Simpler)**:
- Regular Si photodiode (BPW34)
- Less sensitive but cheaper ($2)
- Can still detect arc events

---

### 4C. Pressure Sensor (Optional)

```
Piezoelectric polymer (PVDF) film
Mounted on inside of vial cap

              Cap
           ┌──────┐
           │ PVDF │ ─ 0.5mm thick
           │ film │   area: 1cm²
           │      │   generates voltage
           └──┬───┴──┐   when deformed
              │      │   by pressure pulse
           Electrode  │
           feedthrough│
              │       │
              ├─ Vcc  │
              │       │
              └─ VOut ─────► Oscilloscope
                      │
                     GND

Output: ~0.1V per 10 kPa pressure change
For 2.7 atm rise = 27 kPa → ~0.27V signal
(Detectable but not required for proof of concept)

Alternative: Pressure transducer (0-5 psi rated)
Cost: ~$30 but more robust
```

---

### 4D. Data Acquisition Setup

```
┌──────────────────────────────────┐
│    Oscilloscope or            │
│    Computer with USB DAQ      │
│                               │
│    Channels:                  │
│    1) Temperature (Ther)      │◄──[Thermocouple adapter]
│    2) Light (Photodiode)      │◄──[Transimpedance output]
│    3) Pressure (optional)     │◄──[Piezo sensor]
│    4) Oscillator gate signal  │◄──[555 timer output]
│                               │
│    Sampling rate: 10 kHz min  │
│    (capture 1 kHz oscillation │
│    with 10× oversampling)     │
│                               │
│    FFT Resolution: ≥0.1 Hz    │
│    (to measure beat frequency)│
└──────────────────────────────────┘
              │
              │ USB
              │
         ┌────▼────┐
         │ Computer │
         │ (Python) │
         │ Analyze: │
         │ - Peak temp frequency
         │ - Light pulse timing
         │ - Decay rate
         │ - FFT for dominant freq
         └──────────┘
```

**Data Acquisition Options**:
1. **USB Oscilloscope**: $200-500 (professional)
2. **Arduino + AD converters**: $30-50 (DIY)
3. **Hantek USB scope**: $50-100 (budget)
4. **Thermal camera**: $200-300 (if budget allows)

---

## 5. FULL ASSEMBLY DIAGRAM

```
COMPLETE BENCHTOP SETUP

┌────────────────────────────────────────────────────────────────┐
│                    POWER & CONTROL SECTION                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [12V Power    [555 Timer     [ZVS Driver     [High-V          │
│   Supply]       Oscillator]    Circuit]       Transformer]     │
│     │               │              │              │            │
│     └───────────────┴──────────────┴──────────────┘            │
│                     │                                           │
└─────────────────────┼───────────────────────────────────────────┘
                      │
         1 kHz Square Wave Output
         ┌────────────┴────────────┐
         │                         │
         ▼                         │
    ┌────────────┐                │
    │  Vial      │                │ (Optional trigger for
    │  Chamber   │                │  external oscilloscope)
    │  (10mL)    │                │
    │            │                │ ┌──────────────┐
    │ ┌────────┐ │                │ │ Oscilloscope │
    │ │ ++Arc  │ │                └─►              │
    │ │Electrodes   │◄──────────────┘              │
    │ │  Gap:1mm│ │                      Data      │
    │ │ +10g W  │ │                     Display    │
    │ └────────┘ │                      (Temperature,
    │            │                       Light, Freq)
    │ [Light     │                  │
    │  Window]◄──┼───┐              │
    │            │   │              │
    │ (Thermo    │   │              │
    │  optional) │   │              │
    │            │   ▼              │
    └────────────┘   Light Sensor   │
      Temperature    (photodiode +   │
      Sensor (Therm- transimpedance) │
      ocouple)                       │
                                     │
                    ┌────────────────┘
                    │
                    ▼
              (Computer Analysis)
```

**Physical Layout on Benchtop**:
1. Power supply: Back-left (12V, grounded)
2. Control circuits: Front-left (555 Timer + ZVS on breadboard)
3. High-voltage transformer: Center-left (HV output isolated)
4. Vial chamber: Center (in safety cage if possible)
5. Light detector: Right of vial (on optical rail)
6. Oscilloscope: Front-center (for live monitoring)
7. Thermocouple leads: Top of vial (strain-relieved)
8. Ground plane: Copper tape across breadboard (for EMI reduction)

---

## 6. ELECTRICAL CONNECTIONS SUMMARY

```
Power distribution:
12V (+)  ──────┬──────────────────────────────────┐
               │                                  │
         [Fuse 2A]                               │
               │                                  │
         ┌─────┴─────┐                           │
         │           │                           │
    [7812 Reg]   [555 IC]                   [ZVS IGBTs]
         │           │                           │
      (GND output)   │                    (High-V output
                     │                      100-200V peak)
                     │                           │
                     ▼                           │
            [1 kHz square wave]                  │
                     │                           │
                     └──────────────────────────►│
                                                 │
                    (High-V Transformer)         │
                                                 │
                                                 ▼
                                           ┌──────────┐
                                           │ Electrodes│
                                           │ (Arc gap)│
                                           └──────────┘

Ground connections:
All grounds connected to single common rail (star topology)
┌─ 7812 output (-)
├─ 555 IC ground (pin 1)
├─ ZVS IC ground
├─ All sensor grounds
└─ High-voltage transformer primary return

This prevents ground loops and EMI.
```

---

## 7. SAFETY INTERLOCKS

```
Optional but RECOMMENDED:

┌─────────────────────────────┐
│  Safety Interlock System    │
├─────────────────────────────┤
│                             │
│  Photodiode + Threshold     │
│  Detects arc ignition       │
│         │                   │
│         ▼                   │
│  ┌─────────────┐            │
│  │ Comparator  │            │
│  │ (LM393)     │            │
│  │ Threshold:  │            │
│  │ 1V above    │            │
│  │ baseline    │            │
│  └──────┬──────┘            │
│         │                   │
│    YES: Arc detected        │
│         │                   │
│         ├──► LED blinks     │
│         │                   │
│         └──► Enable timer   │
│              (allow to      │
│               continue)     │
│                             │
│    NO: No arc               │
│         │                   │
│         ├──► Kill oscillator│
│         │    (stop ZVS)     │
│         │                   │
│         └──► Buzzer alarm   │
│                             │
└─────────────────────────────┘

This ensures system only energized when arc is confirmed stable.
```

---

## 8. PARTS LIST (COMPLETE)

### POWER & CONTROL
| Component | Part Number | Qty | Cost | Notes |
|-----------|-------------|-----|------|-------|
| AC-DC Power Supply | 12V/1A | 1 | $15 | Any reputable brand |
| Fuse + Holder | 2A automotive | 1 | $2 | |
| 7812 Voltage Reg | TO-220 | 1 | $0.50 | |
| Capacitors | 1000μF 16V | 1 | $1 | Electrolytic |
| Capacitors | 100nF ceramic | 3 | $0.30 | Bypass |
| NE555 Timer IC | DIP-8 | 1 | $0.50 | |
| Resistors | 1kΩ, 68kΩ | 2 | $0.20 | 1/4W |
| Trim pot | 10kΩ | 1 | $1 | Fine frequency adjust |
| **Subtotal Power** | | | **$21** | |

### ZVS DRIVER (if custom)
| Component | Part Number | Qty | Cost | Notes |
|-----------|-------------|-----|------|-------|
| Gate driver IC | IR2110 | 1 | $5 | or use module |
| Power MOSFETs | IRFZ44N | 2 | $2 | 40V rated |
| Resonant inductor | 1μH ferrite | 1 | $1 | |
| Resonant capacitor | 1nF HV ceramic | 1 | $2 | |
| Rectifier | 1N4007 | 2 | $0.10 | |
| Snubber caps | 10nF HV | 2 | $1 | |
| **Subtotal ZVS (custom)** | | | **$12** | |
| **OR ZVS Module** | Pre-built | 1 | **$25** | Recommended |

### CHAMBER & ELECTRODES
| Component | Description | Qty | Cost | Notes |
|-----------|-------------|-----|------|-------|
| Glass vial | 10mL borosilicate | 1 | $10 | Lab-grade |
| Stainless cap | 316L screw-top | 1 | $5 | Sealed design |
| O-ring | Silicone #12 | 1 | $1 | |
| Tungsten rod | 1.6mm diameter | 0.3m | $2 | Cu solder |
| PTFE tubing | 2mm ID insulation | 1m | $2 | |
| Ceramic spacer | Custom or 3D print | 1 | $1 | Zirconia OK |
| High-temp epoxy | Ceramabond | 1 tube | $8 | Seals electrodes |
| Copper wire | 18 AWG leads | 2m | $1 | Arc connections |
| **Subtotal Chamber** | | | **$30** | |

### SENSORS
| Component | Part Number | Qty | Cost | Notes |
|-----------|-------------|-----|------|-------|
| Type T Thermocouple | Solid | 1m | $5 | Temperature |
| Thermo amplifier | MAX31856 module | 1 | $20 | Converts to V |
| UV Photodiode | SFH 2701 | 1 | $15 | Light detector |
| Transimpedance amp | TL072 + resistor | 1 | $5 | Photodiode circuit |
| Pressure sensor | PVDF film (opt) | 1 | $5 | Optional |
| Oscilloscope | Hantek USB 6022-BL | 1 | $75 | Budget option |
| **Subtotal Sensors** | | | **$125** | USB scope recommended |

### MISC & ASSEMBLY
| Item | Qty | Cost | |
|------|-----|------|---|
| Breadboard + jumpers | 1 | $10 | For circuits |
| Solder + flux | | $5 | |
| Scrap copper (heat sink) | | $2 | For EMI |
| Safety cage/enclosure | 1 | $10 | Cardboard OK for PoC |
| USB cable + adapter | as needed | $5 | |
| **Subtotal Misc** | | **$32** | |

### **TOTAL COST: $245-330**
(Depending on whether you use ZVS module or build custom)

**Budget breakdown**:
- Power/control circuits: ~$50
- Chamber + electrodes: ~$30
- Sensors + data acquisition: ~$125-165
- Miscellaneous + safety: ~$32

---

## 9. ASSEMBLY PROCEDURE

### Step 1: Build Control Circuits (1 hour)
1. Breadboard the 555 timer (1 kHz oscillator)
2. Add ZVS driver (custom or module)
3. Test: 12V → 1 kHz output confirmed on scope

### Step 2: Prepare Chamber (30 minutes)
1. Drill 1mm vent hole in stainless cap
2. Drill 9mm optical window in glass vial side (if needed)
3. Mount electrode assembly in ceramic spacer
4. Epoxy electrodes to vial (use jig to maintain 1mm gap)
5. Mount thermocouple inside vial with high-temp epoxy
6. Seal cap with O-ring

### Step 3: Assemble Sensors (1 hour)
1. Mount photodiode on optical rail (9mm from window)
2. Build transimpedance amplifier circuit on breadboard
3. Connect thermocouple to MAX31856 module
4. Connect both to oscilloscope (USB or Hantek)

### Step 4: Connect High Voltage (30 minutes)
1. Connect ZVS output to electrode leads
2. Isolate HV connections (no bare wire)
3. Test arc initiation (use variable voltage source first)
4. Adjust ZVS frequency trim for stable ~20 kHz oscillation (internal resonance)

### Step 5: Safety Check (15 minutes)
1. Vial seated in safety cage
2. All HV leads isolated
3. 555 oscillator disconnected (manual trigger first)
4. Ground straps in place
5. Oscilloscope isolated from AC mains (USB only)

### Step 6: Bootstrap Test (30 minutes)
1. Manual arc trigger: Brief ZVS pulse
2. Monitor temperature rise (should see +2-5K in 1-10ms)
3. Monitor light output (should see UV pulse on photodiode)
4. If thermally stable→ proceed to oscillator test

### Step 7: Continuous Operation Test (30 minutes)
1. Enable 555 timer at 1 kHz
2. Monitor for 1-5 minutes
3. Record all signals (temperature, light, frequency)
4. Analyze for natural oscillation frequency

---

## 10. EXPECTED SIGNALS

### Temperature Signal
```
Oscilloscope channel 1 (Thermocouple)

    ▲ Temp
    │      ╱╲      ╱╲      ╱╲
    │     ╱  ╲    ╱  ╲    ╱  ╲     +5K rise per pulse
    │    ╱    ╲  ╱    ╲  ╱    ╲
    │───┴──────┴┴──────┴┴──────┴─── Baseline (baseline=0V)
    │
    │ Time → (frequency: 100Hz - 10kHz expected)
```

### Light Signal
```
Oscilloscope channel 2 (Photodiode)

    ▲ Light
    │  ┌─┐   ┌─┐   ┌─┐   ┌─┐
    │  │ │   │ │   │ │   │ │      UV flash ~1μs
    │  │ │   │ │   │ │   │ │      peak voltage: 0.5-2V
    │  │ │   │ │   │ │   │ │
    │  │ │   │ │   │ │   │ │      Decay: exponential ~10-100μs
    │  │ │   │ │   │ │   │ │
    └──┴─┴───┴─┴───┴─┴───┴─┴───►
       │ │   │ │   │ │   │ │
     1 μs gap (shows dissociation
              followed by recomb)

    Time
    Frequency: Same as driving ZVS
```

### Expected Behavior
- **IF system self-sustains**: Temperature and light continue oscillating after 555 timer is disabled
- **IF external trigger needed**: Oscillations stop when ZVS pulses stop

---

**Schematics complete. Ready for fabrication.**

---

**Document**: UFM 10mL Prototype - Complete Schematics  
**Date**: April 10, 2026  
**Status**: Ready for benchtop assembly
