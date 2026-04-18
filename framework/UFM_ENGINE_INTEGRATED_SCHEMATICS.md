# UFM ENGINE - INTEGRATED ELECTRICAL + MECHANICAL SCHEMATICS
**Water Dissociation Prototype - Fabrication Ready**  
**April 10, 2026**

---

## ◇ CORE OPERATING PRINCIPLE: NOTHING IS BY FORCE

**The UFM engine operates entirely through natural energy gradients. No external mechanical forcing. No coerced motion.**

- **Arc provides energy environment** → Water naturally dissociates via thermodynamic gradient
- **Pressure gradient from dissociation** → Piston responds naturally, zero forced actuation
- **Spring constant k=300 N/m** → Assists return but does not force against pressure decay
- **Every transition** follows $-\nabla E$ (energy minimization)

**System Architecture follows physics, not design impositions.**  
If a mechanism requires forcing → gradient is wrong. Reanalyze.

This is not a design choice. It is the operating constraint.

---

## 0. QUICK REFERENCE - PINOUT & CONNECTIONS

### Power Distribution
```
12V Supply → 555 Timer + ZVS Driver + Data Logger
GND (Common Return)
```

### 555 Timer Output → ZVS Driver
```
Pin 3 (555 Output) → Pin 1 (ZVS Input, 1kHz square wave)
ZVS Output → Tungsten Electrodes (bipolar arc)
```

### Sensors → Data Logger (USB/Serial)
```
Thermocouple → Analog Input (CH0)
Photodiode → Analog Input (CH1)
Hall Effect → Analog Input (CH2)
```

---

## 1. COMPLETE SYSTEM ARCHITECTURE

### 1A. Component Interconnection Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    UFM ENGINE SYSTEM                         │
└──────────────────────────────────────────────────────────────┘

POWER SOURCE (12V/1A)
    │
    ├─[Fuse 2A]──────────────┐
    │                         │
    ▼                         ▼
    ┌──────────────┐    ┌──────────────┐
    │ 555 Timer    │    │ ZVS Driver   │
    │ Oscillator   │    │ Circuit      │
    │ 1 kHz output │    │ (Arc ignition)
    └──────┬───────┘    └──────┬───────┘
           │                   │
           │ (1 kHz pulse)     │
           └───────────────────┼─→ Tungsten Electrodes (Arc)
                               │
                               ▼
                        ┌──────────────────────┐
                        │  CHAMBER ASSEMBLY    │
                        │  ┌──────────────┐    │
                        │  │ Borosilicate │    │
                        │  │ Tube 10mL    │    │
                        │  │              │    │
                        │  │ +10g Water   │    │
                        │  │              │    │
                        │  │ Arc produces │    │
                        │  │ H₂ + O₂ + ↔  │    │
                        │  │ Heat + Light │    │
                        │  └──────────────┘    │
                        └──────────┬───────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
            │Thermocouple │ │ Photodiode  │ │ Hall Effect  │
            │Temperature  │ │ UV/Light    │ │ Position     │
            │Sensor       │ │ Intensity   │ │ Sensor       │
            └──────┬──────┘ └──────┬──────┘ └───────┬──────┘
                   │              │               │
                   └──────────────┬───────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │  PISTON MECHANISM    │
                        │  ┌────────────────┐  │
                        │  │ PTFE Piston    │  │
                        │  │ Compressed by  │  │
                        │  │ pressure/heat  │  │
                        │  │ from arc       │  │
                        │  └────────────────┘  │
                        │         ▼            │
                        │  ┌─────────────────┐ │
                        │  │ Piston rod     │ │
                        │  │ slides on      │ │
                        │  │ 20mm rails     │ │
                        │  └─────────────────┘ │
                        │         ▼            │
                        │  ┌─────────────────┐ │
                        │  │ Spring return   │ │
                        │  │ (k=300 N/m)    │ │
                        │  └─────────────────┘ │
                        └──────────────────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │  Data Acquisition &  │
                        │  Analysis            │
                        │  (PC/Oscilloscope)   │
                        └──────────────────────┘
```

---

## 2. DETAILED ELECTRICAL SCHEMATICS

### 2A. 12V Power Supply & Distribution

```
Wall AC (120V, 60Hz)
     │
     ├─[Fuse 2A @ 120V]
     │
     ▼
┌─────────────────────┐
│ Step-Down Transformer
│ 120V AC → 18V AC    │
│ (1A minimum)        │
└──────┬──────────────┘
       │
       ├─────[D1: Diode 1N4007]──┐ (Positive half-cycle)
       │                         │
       ├─────[D2: Diode 1N4007]──┤ (Negative half-cycle)
       │     (Bridge Rectifier)  │
       │                         │
    (─)AC Return ───────────────┘
       │
       ▼
    ┌──────────────────┐
    │ Electrolytic Cap │
    │ C1: 1000μF/25V   │ ← Smoothing
    │ Voltage doubler  │
    │ effect           │
    └────┬─────────────┘
         │
         ├─ +17V ─────────────┬──────────────┬─────────┐
         │                    │              │         │
         ▼                    ▼              ▼         ▼
    ┌─────────┐          ┌─────────┐   ┌────────┐ ┌────────┐
    │ 7812 Reg│          │ 555 Timer   │Ceramic │ │DC Bulk │
    │TO-220   │          │(+12V input) │Cap 0.1 │ │Cap 10μ │
    │Input +17│          │            │ for    │ │for     │
    │Output +12          │            │filter  │ │supply  │
    │GND -    │          │            │        │ │        │
    └────┬────┘          └─────────────┘────────┘ └────────┘
         │                   │              │
         ├───[LED]─[470Ω]───(─ GND ─────────┴────────┴────────┘
         │
         └─ +12V (Main Bus) ──┬──────────────────┐
                              │                  │
                              ▼                  ▼
                        ┌──────────────┐   ┌──────────────┐
                        │ 555 Timer    │   │ ZVS Driver   │
                        │ +12V input   │   │ +12V input   │
                        └──────────────┘   └──────────────┘
```

**Component List (Power Section)**:
- Transformer: 18V AC, 1A (RadioShack or equivalent)
- 1N4007 Diodes: 4x (bridge rectifier)
- C1: 1000μF/25V electrolytic
- 7812 voltage regulator: TO-220 package
- C2: 100nF ceramic (filter, at regulator output)
- C3: 10μF ceramic (bulk supply bypass)
- Fuse: 2A automotive (120V side)
- LED: 5mm red + 470Ω resistor (power indicator)
- Heatsink: Small aluminum (for 7812 if drawing >500mA sustained)

---

### 2B. 555 Timer Oscillator (1 kHz, 50% Duty Cycle)

```
            +12V
             │
             ├──[10kΩ R1]──┬────────[100kΩ R2]──┐
             │             │                    │
    VCC ─────┤1            8├────────────────────┤
             │                                   │
     TRIG ───┤2                              DISCH
             │    555      │               ┌─────┤7
   (GND) ────┤6──────────  │  THRESH ──────┤
             │             ├─────────┬──────
    RESET ───┤4        OUT │         │
             │     (PIN 3) │    ┌────┴────┐
             │                 │C1: 1μF  │
             │             GND │(Timing) │
         GND ┤5              GND
             │
         CV ─┤5
             └──[100nF]
                  ││
                 GND

           ┌──────────────────────┐
           │ Connected Internally │
           │     in 555 Timer     │
           │  (TRIG = THRESH)     │
           └──────────────────────┘
```

**555 Timer Configuration - ASTABLE MODE (Free-running oscillator)**

**Formulas**:
- Charge Time (HIGH): t_H = 0.693 × (R1 + R2) × C1
- Discharge Time (LOW): t_L = 0.693 × R2 × C1
- Frequency: f = 1 / (t_H + t_L) ≈ 1.44 / [(R1 + 2R2) × C1]
- Duty Cycle: D = (t_H) / (t_H + t_L)

**For 1 kHz with 50% duty cycle**:
```
Target: f = 1000 Hz, D ≈ 50%

Using C1 = 1μF:
  1000 = 1.44 / [(R1 + 2R2) × 1×10⁻⁶]
  R1 + 2R2 = 1440 ohms

  For 50% duty: R1 ≈ R2 (simpler calculation)
  Use: R1 = 470Ω, R2 = 470Ω
  
  Frequency = 1.44 / [(470 + 940) × 1×10⁻⁶] ≈ 1020 Hz ✓
  Duty Cycle ≈ (0.693 × 940) / (1.44 / 1000) ≈ 45% (acceptable)
  
  For exactly 50%: Add bypass diode across R2:
  [D1: 1N4148] ─┐
                ├─ Parallel with R2
                ┘
  Diode conducts during discharge only → reduces t_L
```

**5V Adjustment (optional - for sensitivity)**:
```
  CV Pin (Pin 5) normally floats
  Add: 100nF cap to GND ← RF filtering
  Optional: 10kΩ pot to GND for fine-tuning
```

**Output: Pin 3**
```
  Delivers: 1 kHz square wave (0V to 12V, logic-level)
  Current: ~200mA max (sufficient for ZVS driver)
```

**Component List (555 Timer Section)**:
- IC: NE555 or LM555 (8-pin DIP)
- R1: 470Ω, 1/4W resistor
- R2: 470Ω, 1/4W resistor
- C1: 1μF capacitor (film or electrolytic, 16V minimum)
- D1: 1N4148 diode (optional, for 50% duty adjustment)
- C2: 100nF ceramic (CV pin filter)
- Socket: 8-pin DIP (optional but recommended)

**Tuning Notes**:
- Change C1 to adjust frequency (larger C = lower f)
- Change R1 or R2 to adjust duty cycle
- Voltage at pin 2 (TRIG) should oscillate around 4V

---

### 2C. ZVS (Zero Voltage Switching) Driver

```
From 555 Output (1 kHz, 12V square wave)
        │
        ▼
    ┌────────────┐
    │   MOSFET   │
    │  Channel 1 │
    │ (Q1: FQP   │
    │ 30N06L)    │
    │           │
    │ Gate ◄─────┼────── 1 kHz signal from 555
    │ Source─────┴─────── +12V
    │ Drain ──────────┬─ High voltage pulse to transformer primary
    │                 │
    └─────────────────┘
         
    ┌────────────────────────────────┐
    │ Driver IC (Optional, for speed)│
    │ IR2104 High-Speed Driver       │
    │                                │
    │ Input: 1 kHz from 555 (PIN 3)  │
    │ Output: Gate driver for MOSFET │
    │ Isolated output (floating GND) │
    └────────────────────────────────┘
         
    ┌──────────────────────────────────────────┐
    │ High Frequency Transformer               │
    │ (Step-up to arc ignition voltage)        │
    │                                          │
    │ Primary: MOSFET Drain (12V pulsed)      │
    │ Turns Ratio: 1:10 (approx)              │
    │ Secondary: 120V peak output             │
    │                                          │
    │ Transformer: Ferrite core, ~50 kHz BW  │
    └────────────┬─────────────────────┬──────┘
                 │                     │
                 ▼                     ▼
            W+ Electrode          W- Electrode
       (Tungsten electrode +)  (Tungsten electrode -)
                 │                     │
                 └─────┬───────────────┘
                       │
                   3-4mm GAP
                  (Water in between)
                       │
                       ▼
                    ARC DISCHARGE
              (Ionization → H₂O → H + O)
```

**Simplified One-MOSFET ZVS Circuit**:

```
                +12V
                 │
         ┌───[L1: 10μH]──┐
         │                │
         ├────[D1]────────┤
    P1 ──┤                │ (Primary winding)
         │   ┌────────┐   │ (Ferrite toroid)
         │ Q │MOSFET  │   │
         │ 1 │        │───┴─ P2 (to secondary)
         │   │        │
         │   └────────┘
         │       │
         │      GND
         │
         ├──[2N7000]──────┐ (Gate driver MOSFET)
         │ (small signal)  │
         │ Gate ◄──────────┴──── 1 kHz from 555
         ▼ Source
        GND

        S (Secondary, 1:10 step-up)
         │
         ├─[High Voltage Capacitor 100nF/500V]──┐
         │                                        │
         ├─ High Voltage Rectifier [HVDC]        │
         │                                        │
         ├──[1MΩ bleeder resistor]───────........├─ to Tungsten Electrodes
         │                                        │
         │                                        ▼
        GND ───────────────────────────────── Ground reference
```

**Full ZVS Driver Circuit (Production-Ready)**:

```
     +12V
      │
      ├──[R-Gate: 47Ω]──┐
      │                 │ Gate limiting resistor
      │      ┌──────────┘
      │      │
      │   ┌──┴──┐
      │   │Gate │
      │   │(G)  │
   L1 ├───┤     ├───┐ Drain (D)
      │   │     │   │
      │   └──┬──┘   ├──┘ Source (S)
      │      │      │
     D1 ────┴──────GND
      │            (Body diode of MOSFET
     ─┴─           provides return path)
    │ Q1 │
    │FQP │
    │30  │
    │N06 │
    │ L- │
    └────┘

    From 555 Timer (Pin 3) ──[100Ω current limiting]──► Gate
    
    ┌─ Transformer Primary Inductance ──┐
    │  L (approx 10-20μH from primary)   │
    │  Creates resonance with gate cap   │
    └─────────────────────────────────────┘
    
    Drain output → High Voltage Transformer
    Secondary → Rectified to ~150V DC → Electrodes
```

**Component List (ZVS Section)**:
- Q1: FQP30N06L N-channel MOSFET (30A, 60V, low R_ds)
- D1: 1N4007 (freewheeling diode, optional with MOSFET body diode)
- L1: 10μH ferrite inductor (or calculate from transformer primary)
- C_gate: Not needed (MOSFET has internal cap)
- R_gate: 47Ω current limiting resistor
- Gate driver: 2N7000 small-signal MOSFET or dedicated IC (IR2104)
- Transformer: Ferrite core, 1:10 step-up, 500V secondary rating
- D_hv: High voltage rectifier (1N4007 × 4 in bridge, or 1N4007 × 2 in doubly-rectified)
- C_hv: 100nF ceramic, 500V rating (output filter)
- R_bleed: 1MΩ, 1W (safety discharge)

**Output**: 
- ~150V peak AC at electrodes
- ~100-200V DC after rectification
- Frequency: 1 kHz (same as 555 timer)
- Peak current: 50-100mA (limited by transformer impedance)

---

### 2D. Sensor Interface Circuits

#### 2D-i. Thermocouple (K-Type) → Analog Input

```
Thermocouple leads (red/yellow)
    │
    ├─[K-type TC wire, ~50ft max]──┐
    │                               │
    │                          ┌────┴─────┐
    │                          │ Ref Block │
    │                          │ (Ice bath)│
    │                          └────┬─────┘
    │                               │
    ├─────────────────────────────┬─┘
    │      Cold junction            │
    │                              ▼
    ├──[100nF ceramic]────────┬─ OPA input (-)
    │  ││                      │
    │  ││                    ┌─┴──────┐
    │  GND                   │ OPA2134 │
    │                        │ Op-Amp  │
    │                    ┌───┤+Vcc 5V  │
    │                    │   │         │
    │                    │   │  Gain   │ ← 100x gain
    │                    │   │  Amp    │    (1mV / division)
    │                    │   │ Vout    │
    │                    │   └────┬────┘
    │                    │        │
    │                  ┌─┴─────────┴──┐
    │                  │ Potentiometer │
    │                  │ 1kΩ (for      │
    │                  │ offset cal)   │
    │                  └────────┬──────┘
    │                           │
    │                      ┌────▼───────┐
    │                      │ Analog Out  │
    │                      │ to DAQ      │
    │                      │ (0-5V range)│
    │                      └─────────────┘

Temperature formula:
  V_out (mV) / 100 = Temp (°C)
  
  Example: 400mV input → 4°C
           2000mV input → 200°C (limit)
```

**Component List (Thermocouple)**:
- K-type thermocouple wire (50ft spool, ~$15)
- Cold reference block (optional; room temp acceptable ±1°C)
- OPA2134 dual op-amp (or LM358)
- R_gain: calibrate for 100x amplification
- R_offset: 1kΩ potentiometer (nulling)
- C_filter: 100nF ceramic
- Positive supply: +5V, Negative: GND (single supply)

#### 2D-ii. Photodiode (UV Sensitive) → Analog Input

```
Light from arc
    │
    ▼
┌─────────────────┐
│ Photodiode      │
│ S8254-UL        │ ← responds to UV/visible light
│ (photodiode)    │
│ Anode (+)       │────────┬────┐
│ Cathode (-) ────┴────────┤    │
│                          │    │
│                      ┌───┤Bias│ (~10V reverse bias for speed)
│                      │   │Vcc │
│                      │   └─┬──┘
│                      │     │
│    ┌─────────────────┘     │
│    │  ┌──────────┐         │
│    ├──┤I→V Amp   │─────────┤ Output 0-5V
│    │  │(Transim) │         │ (0-10 nanoamps → 0-5V)
│    │  └──────────┘         │
│    │                       │
│   GND [1GΩ feedback resistor]
│
└───────────── to GND

Transimpedance Configuration:
    ┌──────────────────┐
    │                  │
    ├──◄  Photodiode   │
    │                  │
    │   ┌─────────┐    │
    ├───┤OPA2134  ├────┤ V_out = I_photo × R_f
    │   │ I→V     │    │ (I in nA → V in V)
    │   └─────────┘    │
    │      │           │
    └──────┴──────────┬─┘
                      │
                  ┌───▼────┐
                  │ Output  │
                  │ 0-5V    │
                  │ Filter  │
                  │ 100nF   │
                  └────┬────┘
                       │
                       ▼
                  To Data Logging
```

**Component List (Photodiode)**:
- Photodiode: S8254-UL or equivalent (UV/Visible)
- Op-amp: OPA2134 (low input bias current, high gain)
- R_f: 1GΩ (feedback resistor - adjustable via 10MΩ pot in series)
- Bias supply: 10V (optional, improves speed)
- C_filter: 100nF ceramic (output filter)
- Cable shielding recommended (long cable to arc chamber)

#### 2D-iii. Hall Effect Sensor (Piston Position) → Analog Input

```
Magnetic field from magnet on piston rod
        │
        ▼
    ┌────────────────┐
    │ Hall Sensor    │ ← Output varies with B-field
    │ (eg. A1301)    │   0V @ no field
    │                │   +5V @ max field
    │ Vcc: +5V       │   ~2.5V @ neutral
    │ Ground: GND    │
    │ Output ─────────┬──► Analog In (already 0-5V)
    │ Eq: V = Vcc/2   │
    └────────────────┘
             │
             ├── [100nF filter cap]
             │   ││
             │  GND
             │
             ▼
        Oscilloscope / DAQ
        Channel 2
        
Position Interpretation:
  2.5V = Hall sensor centered (piston at rest)
  0-2.5V = Moving backward (spring pulls piston)
  2.5-5V = Moving forward (pressure expands piston)
```

**Component List (Hall Sensor)**:
- Sensor: A1301 or A1302 (ratiometric, 0-5V output)
- Magnet: Small neodymium disk (5mm × 2mm) on piston rod
- C_filter: 100nF ceramic
- Supply: +5V (from separate regulated output or 7805)
- Mounting: Sensor fixed ~2cm from rod, perpendicular to motion

---

## 3. DATA ACQUISITION & MONITORING

```
                    ┌──────────────────────────────┐
                    │    Computer / Oscilloscope   │
                    │    USB or Serial Interface   │
                    └──────┬───────────────────────┘
                           │
                    ┌──────┴────────┐
                    │               │
                    ▼               ▼
            ┌──────────────┐  ┌──────────────┐
            │ Analog Input │  │ Frequency    │
            │ Multiplexer  │  │ Counter      │
            │ (3 channels) │  │ (555 clock)  │
            └──────┬───────┘  └──────────────┘
                   │
    ┌──────────┬───┼───┬──────────┐
    │          │   │   │          │
    ▼          ▼   ▼   ▼          ▼
   Temp      Light Pos  GND    Reference
   
Measurement Program (Python / LabVIEW):
  - Sample all 3 channels at 10 Hz
  - Display temperature, light intensity, position
  - Log to CSV
  - FFT of light signal (detect arcing frequency)
  - Monitor for oscillations
```

---

## 4. MECHANICAL-ELECTRICAL INTEGRATION

### 4A. Arc Chamber to Piston Interface

```
┌────────────────────────────────────────┐
│  Borosilicate Glass Tube (10mL)        │
│  ┌────────────────────────────────────┐│
│  │  Top Cap (PTFE or aluminum)        ││
│  │  ├─ W+ Electrode (tungsten)        ││ ← 150V+ from ZVS secondary
│  │  └─ W- Electrode (tungsten)        ││ ← Ground reference
│  │                                     ││
│  │  Water seal (silicone grease)      ││
│  │  ┌─────────────────────────────────┼┼──┐
│  │  │  10 mL distilled water          │║  │
│  │  │  ┌────────────────────────────┐ │║  │
│  │  │  │ 3-4mm electrode gap      ███ │║  │
│  │  │  │ {Arc ionizes H₂O}       ═══════ │ ← Light photons
│  │  │  │                            │ │║  │
│  │  │  │  H₂O → H⁺ + O²⁻ + e⁻     │ │║  │ UV/visible spectrum
│  │  │  │  Temperature rise        │ │║  │ detected by photodiode
│  │  │  └────────────────────────────┘ │║  │
│  │  │                                   ││  │
│  │  └─────────────────────────────────┬┼┼──┘
│  │                                     ││
│  │  Piston bottom cap (PTFE)          ││
│  │  ├─ Thermocouple wire (K-type)    ││ ← Temperature monitoring
│  │  │  (tip immersed in water)        ││
│  │  └─ Piston rod (8mm PTFE)          ││ ← Goes to mechanical section
│  │     with magnet embedded           ││ ← Hall sensor detects motion
│  └─────────────────────────────────────┘│
│                                          │
│  ┌──────────────────────────────────────┴──┐
│  │  Piston Block (Aluminum or PTFE)        │
│  │  ┌────────────────────────────────────┐ │
│  │  │ Piston disk (18mm diameter)        │ │ ← PTFE, 2mm thick
│  │  │ Sits snugly in glass tube end     │ │ ← Self-sealing
│  │  └────────────────────────────────────┘ │
│  │         │                                 │
│  │         ▼ (movement transmitted to rod)  │
│  │  ┌────────────────────────────────────┐ │
│  │  │ Piston Rod (8mm diameter, 50mm)   │ │ ← Slides on 20mm rails
│  │  │ M6 thread at end (for adjustment) │ │ ← For calibration
│  │  │ Small neodymium magnet (2mm)      │ │ ← For Hall sensor
│  │  └────────────────────────────────────┘ │
│  └──────────────────────────────────────────┘
└────────────────────────────────────────────┘
         │
         ├─ Pressure pushes piston out
         │  (arc + hot gas from combustion)
         │
         ├─ Spring pulls piston back
         │  (k=300 N/m, precompressed 5mm)
         │
         └─ Cycle repeats at 1 kHz oscillation frequency
```

### 4B. Electrical Connections Through Chamber

```
┌─────────────────────────────────┐
│ Top Cap (Feedthrough Panel)     │
├─────────────────────────────────┤
│  Tungsten leads (insulated)     │
│  ├─ Lead 1: W+ → ZVS secondary+ │
│  └─ Lead 2: W- → ZVS secondary- │
│                                 │
│  Thermocouple leads (small)     │
│  ├─ Red: to Op-amp input        │
│  └─ Yellow: to GND ref          │
│                                 │
│  Photodiode leads (shielded)    │
│  ├─ Signal: to I→V amplifier    │
│  └─ Ground: return              │
│                                 │
│  Hall sensor leads              │
│  ├─ +5V supply                  │
│  ├─ GND return                  │
│  └─ Signal: to multiplexer      │
└─────────────────────────────────┘
```

---

## 5. COMPLETE WIRING CHECKLIST

### Phase 1: Power
- [ ] 12V supply → Fuse 2A → Main bus
- [ ] Main bus → 555 timer Vcc (pin 8)
- [ ] Main bus → ZVS MOSFET drain
- [ ] All GND lines → Common return (star point at battery -)

### Phase 2: 555 Timer Clock
- [ ] Pin 1 (GND) → Common GND
- [ ] Pin 8 (Vcc) → +12V
- [ ] Pin 4 (Reset) → +12V (pulled high)
- [ ] Pin 5 (CV) → 100nF cap → GND
- [ ] Pin 2 (Trig) → Pin 6 (Thresh) → tied together
- [ ] Pin 2/6 → C1 (1μF) and to junction of R1, R2
- [ ] Pin 3 (Out) → 100Ω resistor → ZVS gate input
- [ ] R1 (470Ω) → +12V to junction
- [ ] R2 (470Ω) → junction to GND (with optional D1 bypass)

### Phase 3: ZVS Driver
- [ ] Pin 3 of 555 (1 kHz) → 100Ω → MOSFET gate
- [ ] MOSFET source → GND
- [ ] MOSFET drain → L1 (10μH inductor)
- [ ] L1 other end → Transformer primary positive
- [ ] Transformer primary negative → +12V (through optional D1)
- [ ] Transformer secondary → rectifier bridge
- [ ] Rectifier output → 100nF cap → 1MΩ bleed resistor
- [ ] Rectifier output (±) → Tungsten electrode leads

### Phase 4: Sensors
- [ ] Thermocouple K-type → Op-amp inverting input (through 1kΩ)
- [ ] Thermocouple ref → Op-amp non-inverting (with gain resistor)
- [ ] Op-amp output → DAQ channel 0 (Analog In)
- [ ] Photodiode anode → I→V transimpedance op-amp
- [ ] Photodiode cathode → GND (through 1GΩ feedback)
- [ ] I→V output → DAQ channel 1
- [ ] Hall sensor +5V → +5V (separate regulated supply)
- [ ] Hall sensor GND → GND
- [ ] Hall sensor output → 100nF cap → DAQ channel 2

### Phase 5: Data Logging
- [ ] DAQ USB → Computer
- [ ] Computer running logging software (Python + PySerial + matplotlib)
- [ ] Oscilloscope channel 1 → 555 output (for reference)
- [ ] Oscilloscope channel 2 → Photodiode output (light pulses)
- [ ] Oscilloscope channel 3 → Hall sensor output (position)

---

## 6. ASSEMBLY SEQUENCE

1. **Build power supply** (transformer, rectifier, 7812)
   - Test: Measure 12V ± 0.5V at main bus

2. **Build 555 timer circuit** on breadboard
   - Test: Measure 1 kHz square wave at pin 3
   - Duty cycle should be 40-60%

3. **Build ZVS driver** (MOSFET + transformer + rectifier)
   - ⚠️ HIGH VOLTAGE CAUTION before connecting secondary!
   - Test: Measure ~150V DC across output (no load, high impedance)

4. **Assemble chamber** (glass tube + electrodes + piston cap)
   - Test: Mechanical motion of piston rod (no power)
   - Lubricate rails with silicone grease

5. **Install sensors**
   - Thermocouple: immerse tip in water (or water-filled tube)
   - Photodiode: point at arc chamber (cover excess light with paper tube)
   - Hall sensor: mount ~2cm from magnet, perpendicular to motion

6. **Wire electrodes** to ZVS secondary
   - ⚠️ Insulate all high-voltage connections!
   - Use shrink tube over wire connections

7. **Connect sensor leads** to data acquisition
   - Use shielded cable for photodiode (minimize noise)
   - Keep thermocouple wires away from power cables (EMI)

8. **Final checks**
   - No shorts (megohmmeter on HV side and inputs)
   - All grounds connected to common return
   - Power supply smoothly energizes (slowly turn on if available)

---

## 7. SAFETY & TESTING PROCEDURE

### ⚠️ HAZARDS
- **High voltage** (~150V DC at electrodes) — lethal if touched
- **Arc plasma** — UV radiation + RF noise
- **Hydrogen production** — explosive in certain concentration ranges
- **Heat generation** — chamber adjacent components can reach 100°C+

### TESTING SEQUENCE
1. **Dry test** (no water, no HV)
   - Verify piston mechanical motion
   - Check 555 frequency
   
2. **Low water test** (2mL water, no HV)
   - Verify temperature sensor response (ambient increase)
   - Verify piston motion with added mass
   
3. **Arcing test** (5mL water, HV enabled, 30-second runs)
   - Start with 555 timer ONLY (no ZVS driver)
   - Activate ZVS driver, observe light emission
   - Monitor temperature (should rise quickly)
   - Run max 30 seconds, then cool
   
4. **Extended test** (10mL water, multiple 1-minute cycles)
   - Monitor for stable oscillations
   - Record temperature rise rate
   - Record light intensity variations
   - Look for pressure relief (piston feedback)

### SAFETY SHUTDOWN
- Instant power cut: **large red button** on power supply
- Discharge cap: **1MΩ resistor** left on HV side (bleeds in <10 seconds)
- Cool chamber: **Ice bath or water spray** (use insulated tongs)

---

## 8. EXPECTED MEASUREMENTS

### Temperature Response
```
Initial: 20°C (room temp)
At 30sec: 35-45°C (gentle heating)
At 60sec: 60-80°C (moderate heating possible)
At arc start: +50°C jump in seconds (arc thermal load)
```

### Light Detection
```
No arc: photodiode ≈ 0.2V (background)
Arc init: photodiode jumps to 2-3V
Stable arc: photodiode ≈ 2-5V (flickering at KHz rate)
```

### Piston Position
```
At rest: Hall sensor ≈ 2.5V (neutral)
Pressure pulse: 3.0-3.5V (0-50ms after arc)
Return: 2.0-2.5V (50-500ms, spring pulls back)
Period: ~1000ms (matches 1 kHz clock frequency)
```

---

## 9. SCHEMATIC SUMMARY & BOM

**Total Bill of Materials**:
- Power: Transformer, rectifier, 7812 regulator, caps, fuse
- 555 Timer: IC, resistors, capacitor, socket
- ZVS: MOSFET, diode, inductor, transformer, high-voltage rectifier, cap
- Sensors: Thermocouple (with reference), photodiode, Hall sensor, op-amps
- Passive: Resistors (various), capacitors (various), interconnect wire
- Mechanical: Glass tube, PTFE, electrodes, piston, rod, rails, spring

**Total Cost Estimate**:
- Electrical: $65-85 (electronics new)
- Mechanical: $45-65 (materials + fabrication time)
- Sensors: $30-40 (thermocouple, photodiode, Hall sensor)
- **Total: ~$140-190** (using your existing equipment, avoiding external fabrication)

---

## 10. NEXT STEPS

1. **Breadboard the 555 timer** — verify 1 kHz oscillation
2. **Build power supply** — test 12V regulation
3. **Assemble ZVS driver** with safety precautions
4. **Fabricate chamber assembly** (your lathe/mill)
5. **Integrate all systems** on a tested PCB or proto board
6. **Initial arc test** in controlled environment
7. **Data logging** and analysis

---

**Ready to proceed to detailed mechanical integration, or questions on electrical setup?**

