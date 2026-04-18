# UFM FLYWHEEL SYSTEM - CONFIGURABLE DESIGN
**Modular Piston-to-Rotation Conversion**  
**April 10, 2026**

---

## OVERVIEW

The flywheel converts linear piston oscillation → rotational energy → any output you want.

**Fully configurable:**
- Flywheel size (diameter: 50mm to 200mm)
- Flywheel mass (steel vs aluminum vs composite)
- Crank mechanism (simple eccentric, true crankshaft, or belt drive)
- Input frequency (1 kHz piston = variable RPM depending on mechanism)
- Output load (pump, generator, mechanical work, or just energy smoothing)

---

## DESIGN PARAMETERS (USER-CONFIGURABLE)

### Parameter 1: Piston Specifications (Fixed for this prototype)
```
Stroke Length: L_s = 30mm (0.03m)
Piston Mass: m_p = 0.05 kg (50g PTFE disk)
Input Frequency: f_in = 1 kHz (555 timer clock)
Piston Area: A_p = π × (18mm)² ≈ 1000 mm² = 0.001 m²
```

### Parameter 2: Crank Mechanism Selection
**Choose ONE:**

**Option A: Simple Eccentric Cam (Fastest to build)**
- Crank radius (eccentricity): r = 15mm
- Input: Linear piston motion (±15mm)
- Output: Rotating follower on eccentric
- Advantage: Single rod, low cost, easy assembly
- Disadvantage: Non-sinusoidal motion (bang-bang)

**Option B: True Crankshaft (Most balanced)**
- Crank arm length: L_c = 15mm (equivalent stroke = 30mm)
- Connecting rod length: L_rod = 60-100mm (adjustable)
- Input: Linear piston motion
- Output: Smooth sinusoidal rotation
- Advantage: Smooth energy transfer, optimizable
- Disadvantage: More fabrication (turning, drilling)

**Option C: Belt/Pulley Drive (Most flexible)**
- Input pulley: Small (20mm diameter) on piston rod
- Output pulley: Large (50-100mm diameter) on flywheel shaft
- Mechanical advantage: Output_RPM = Input_RPM × (Input_D / Output_D)
- Advantage: Decoupled, variable ratio
- Disadvantage: Belt tensioning, slip potential

### Parameter 3: Flywheel Size & Mass
Choose based on **intended use:**

**Lightweight (Energy Smoothing Only)**
```
Diameter: 80mm
Thickness: 10mm
Material: Aluminum (ρ = 2700 kg/m³)
Mass: ~0.17 kg

I (moment of inertia) = 0.5 × m × r² = 0.5 × 0.17 × (0.04)² ≈ 1.36e-4 kg·m²

Energy storage @ 1000 RPM:
  ω = 1000 × 2π/60 = 104.7 rad/s
  E = 0.5 × I × ω² = 0.5 × 1.36e-4 × (104.7)² ≈ 0.75 J
```

**Medium (Light Mechanical Load - pump, small generator)**
```
Diameter: 120mm
Thickness: 15mm
Material: Steel (ρ = 7850 kg/m³)
Mass: ~0.66 kg

I = 0.5 × 0.66 × (0.06)² ≈ 1.19e-3 kg·m²

Energy storage @ 1000 RPM:
  E = 0.5 × 1.19e-3 × (104.7)² ≈ 6.5 J
```

**Heavy (Significant Load - continuous pump, electricity generation)**
```
Diameter: 150mm
Thickness: 20mm
Material: Steel (ρ = 7850 kg/m³)
Mass: ~1.5 kg

I = 0.5 × 1.5 × (0.075)² ≈ 4.22e-3 kg·m²

Energy storage @ 1000 RPM:
  E = 0.5 × 4.22e-3 × (104.7)² ≈ 23 J
```

### Parameter 4: Output Application
Choose what the flywheel DOES:

**A) Smoothing Only** (no external load)
- Flywheel just stores energy between pulses
- Reduces vibration, improves efficiency
- No electrical or mechanical output
- Simplest assembly

**B) Pump Drive** (small water or gas pump)
- Flywheel powers peristaltic pump (water recirculation)
- Or air pump (pressurize chamber)
- Requires: 1-2 W mechanical power at 500-1500 RPM
- Flywheel size: Medium (see above)

**C) Electrical Generation** (charge battery, run LED)
- Flywheel drives small DC generator (toy motor, reversed)
- Output: 1-5 W electrical @ 12V
- Flywheel size: Medium to Heavy

**D) Secondary Water Dissociation** (cascade system)
- Flywheel drives SECOND chamber with its own electrodes
- Double the H₂/O₂ production from single 555 timer input
- Flywheel size: Heavy, geared up for torque

**E) Mechanical Work** (lift weight, compress spring)
- Flywheel stores energy over multiple cycles
- Then releases in one short burst
- Useful for mechanical amplification

---

## IMPLEMENTATION OPTIONS

### OPTION A: ECCENTRIC CAM (Simplest - 2 hours to build)

**Parts to Machine from Your Stock:**

```
From 55mm steel rod:
  ├─ Crank shaft: 50mm length, 6mm diameter
  │  Eccentric offset: 15mm from center (turn one end)
  │  Keyway: 2mm × 10mm for flywheel coupling
  │
  └─ Eccentric follower: 8mm bore, 8mm thick
     (slides on crank pin, transmits to piston rod via link)

Flywheel: 80-150mm diameter × 10-20mm thick
  ├─ Bore: 6mm (fits on crank shaft)
  ├─ Keyway: 2mm × 10mm (locks to shaft)
  └─ Material: Your aluminum or steel stock

Bearings: Two 6mm shaft bearings (deep groove ball)
  or DIY: Brass bushings you can turn from scrap

Connecting link: 30mm aluminum angle iron
  ├─ One end: pin joint to eccentric follower
  └─ Other end: pin joint to piston rod (M6 thread)
```

**Fabrication Steps:**
1. Turn 55mm steel rod down to 6mm diameter (50mm long) = crank shaft
2. Turn eccentric on one end: 15mm offset, smoothed radius
3. Drill 6mm hole in piston rod end, install M6 pin
4. Drill 8mm hole in connecting link, install joint pins
5. Machine flywheel from aluminum disk (80mm dia, 10mm thick)
6. Bore 6mm hole in flywheel center
7. Cut keyway (2mm × 10mm) in shaft and flywheel bore
8. Press flywheel onto shaft, pin with 3mm key
9. Install bearings in frame supports

**Motion Profile:**
```
As piston moves OUT (+15mm):
  Eccentric rotates 90° (¼ turn) → crank arm goes from horizontal to vertical
  Flywheel picks up speed: 0 → 500 RPM

As piston moves BACK (-15mm):
  Eccentric rotates another 90° → crank arm returns to horizontal
  Flywheel coasts: 500 → 250 RPM (resists piston return)

Cycle repeats, net speed oscillates 250-500 RPM at piston frequency
Average output: ~350 RPM continuous
```

---

### OPTION B: TRUE CRANKSHAFT (Most Balanced - 4 hours to build)

**Parts to Machine:**

```
Crankshaft (from 55mm steel rod):
  ├─ Main journal (6mm diameter) at each end
  │  Length: 60mm total
  │
  ├─ Crank pin (6mm diameter):
  │  Offset: 15mm from centerline
  │  Located 30mm from one end
  │  Width: 8mm (length of crank arm)
  │
  └─ Keyway: 2mm × 10mm for flywheel coupling

Connecting rod (from aluminum stock):
  ├─ Bore 1: 6mm (fits crank pin)
  ├─ Bore 2: 8mm (connects to piston rod with M6 thread)
  ├─ Length: 80-120mm (longer = smoother motion, requires more space)
  └─ Width: 20mm, thickness: 8mm (keep lightweight)

Piston rod modified:
  ├─ End threaded M6 (already done)
  ├─ Upper bore: 8mm (pin joint for connecting rod)
  └─ Alignment: must be colinear with crank pin

Flywheel: 80-150mm diameter × 10-20mm thick
  ├─ Bore: 6mm (fits main journal)
  ├─ Keyway: 2mm × 10mm
  └─ Mounted on crank shaft, toward bearing

Bearings: Two 6mm deep groove ball bearings
  ├─ One at each end of crankshaft
  └─ Mounted in adjustable frame blocks
```

**Fabrication Steps:**
1. Turn crankshaft from 55mm rod:
   - Main journal: 6mm diameter, 20mm length each end
   - Crank arm: 8mm thick, 15mm offset crank pin
   - Smooth all transitions with 1mm radius
2. Turn connecting rod from aluminum:
   - 6mm bore at crank end, 8mm bore at piston end
   - Drill cleanly perpendicular to rod axis
3. Modify piston rod upper end:
   - Drill 8mm hole for pin joint
   - Ensure colinear with piston motion axis
4. Machine flywheel:
   - Diameter: your choice (80-150mm)
   - Thickness: 10-20mm
   - Bore: 6mm, with keyway in bore
5. Assembly:
   - Press flywheel onto crankshaft main journal
   - Install crank pin (press-fit or set screw)
   - Parallel-mount two bearing blocks 60mm apart
   - Install crankshaft in bearings
   - Install connecting rod on crank pin
   - Link connecting rod to piston rod with M6 pin

**Motion Profile:**
```
Piston position as function of crank angle:
  x(θ) = L_c × cos(θ) + √(L_rod² - (L_c × sin(θ))²) - (L_c + L_rod)
  
  where:
    L_c = crank length (15mm)
    L_rod = connecting rod length (80-120mm)
    θ = crank angle (0-360°)

At θ=0°: x = 0 (piston neutral)
At θ=90°: x = L_c = 15mm (piston most extended)
At θ=180°: x = 0 (piston back at neutral)
At θ=270°: x = -L_c = -15mm (piston most retracted)

Smoother than eccentric, sinusoid-like motion
Output speed: Continuous @ ~330-500 RPM depending on load
```

---

### OPTION C: BELT DRIVE (Most Flexible - 1 hour setup)

**Parts Needed:**

```
Input pulley (on piston rod, or shaft from eccentric cam):
  ├─ Diameter: 20mm
  ├─ Bore: 8mm (fits piston rod or eccentric shaft)
  ├─ Groove: V-belt slot (for small V-belt)
  └─ Mounting: Slide onto rod, secure with set screws

Output pulley (on flywheel shaft):
  ├─ Diameter: 60-100mm (choose for desired output RPM)
  ├─ Bore: 6mm (fits flywheel shaft)
  ├─ Groove: V-belt slot
  └─ Mounting: Press onto shaft, pin with key

Flywheel:
  ├─ Can be same as above (80-150mm)
  ├─ Or smaller/lighter since drive is decoupled
  └─ Mounted coaxially with output pulley

Belt:
  ├─ Type: Small V-belt (3/8" width, typically A- or B-profile)
  ├─ Length: Determined by pulley spacing (see formula below)
  └─ Tensioner: Small spring-loaded roller (improvise or buy)

Shaft bearing supports (aluminum frame blocks):
  ├─ Adjustable for belt tension
  └─ Must align pulleys coaxially (or slight angle acceptable)
```

**Pulley Sizing Formula:**
```
Mechanical Advantage:
  RPM_output = RPM_input × (D_in / D_out)
  Torque_output = Torque_input × (D_out / D_in)

Example 1: Want same RPM as input
  D_in = 20mm → D_out = 20mm (1:1 ratio)
  Input: 1 kHz piston, eccentric → ~400 RPM
  Output: ~400 RPM (smooth steady state)

Example 2: Want to run slower, higher torque  
  D_in = 20mm → D_out = 80mm (4:1 reduction)
  Input: ~400 RPM
  Output: ~100 RPM, 4× torque

Example 3: Want to run faster
  D_in = 30mm → D_out = 20mm (1:1.5 overdrive)
  Input: ~400 RPM
  Output: ~600 RPM, less torque
```

**Belt Length Calculation:**
```
L = π(R_out + R_in) + 2 × C × sin(arccos((R_out - R_in) / C))

Where:
  R_out = output pulley radius (mm)
  R_in = input pulley radius (mm)
  C = center distance between pulleys (mm)

Example: D_out=80mm, D_in=20mm, C=100mm
  L = π(40+10) + 2×100×sin(arccos(30/100))
  L ≈ 157 + 200×sin(72.5°) ≈ 157 + 190 ≈ 347mm
  
  Buy V-belt with pitch length ~350mm
```

**Advantages Over Direct Drive:**
- Can change ratio by swapping pulleys (no remachining)
- Decouples vibrations (belt acts as damper)
- Can place flywheel far from piston (good for weight distribution)
- Simple to assemble/disassemble

**Disadvantages:**
- Belt wear (replace every 6-12 months depending on use)
- Slight power loss to friction (~5-10%)
- Requires tension adjustment

---

## BEARING OPTIONS (Choose Your Level)

### Option 1: Ball Bearings (Best, ~$5-10 each)
```
Size: 6mm bore (fits your crankshaft)
Type: Deep groove ball bearing (most common)
Part: 606 or 626 (small standard sizes)
Mount: In adjustable aluminum frame blocks
Preload: None needed for low-speed engine

Supply: McMaster-Carr, eBay, AliExpress (cheap)
```

### Option 2: Brass Bushings (DIY from your stock, ~$1)
```
Material: Brass or bronze (you have scrap?)
Bore: 6mm (match crankshaft diameter)
OD: 10-12mm to fit frame hole
Thickness: 8-10mm

Fabrication:
  ├─ Start with brass rod 10mm OD
  ├─ Drill 6mm hole through center (use drill press)
  ├─ Cut to 8-10mm length segments
  ├─ Ream 6mm hole to smooth finish (minimize runout)
  └─ Install in frame blocks with slight interference fit

Lubrication: Light machine oil, drip every 100 hours
```

### Option 3: Polymer Bushings (Cheap, ~$0.50, lowest friction)
```
Material: UHMWPE (ultra-high molecular weight polyethylene)
  or acetal (Delrin)
  
Source: 
  ├─ Buy: AliExpress/McMaster ($1-3 for pair)
  └─ Or: Drill PTFE rod (you have!) to 6mm bore
  
Advantages: 
  ├─ Self-lubricating (no oil needed)
  └─ Very low friction, silent

Disadvantages:
  ├─ Wears faster than metal (1-2 year lifespan)
  └─ Must align perfectly or will bind
```

---

## POWER & TORQUE ANALYSIS (Pick Your Scenario)

### Scenario 1: Smooth Energy Oscillation (No External Load)

```
Input power: From piston pressure pulses
  Peak pressure: 2-3 atm = 200-300 kPa
  Piston area: 1000 mm² = 0.001 m²
  Peak force: F = P × A = 300000 × 0.001 = 300 N
  Piston velocity (at resonance): v ≈ L_s × f = 0.03 × 1000 = 30 m/s
  
  Peak power input: P = F × v = 300 × 30 = 9000 W (9 kW)
  BUT: Piston does NOT reach 30 m/s in practice
  Realistic peak power: ~200-500 W
  Average power: ~50-100 W

Minimum flywheel mass to maintain steady oscillation:
  Inertia needed: I_min = 1e-4 kg·m² (aluminum 80mm flywheel)
  At 400 RPM average speed

Effect of heavier flywheel:
  ├─ 1e-4 I: Oscillates heavily (250-500 RPM swing)
  ├─ 1e-3 I: Smoother (350-450 RPM swing)
  └─ 4e-3 I: Very smooth (380-420 RPM constant)
```

### Scenario 2: Drive Small Pump (Water Recirculation)

```
Typical pump specs:
  Power needed: 1-3 W @ 500-1000 RPM
  Torque needed: 0.05-0.1 N·m at output shaft

Flywheel sizing:
  Input torque (at crank): ~2-5 N·m (from piston pressure)
  Crank radius: 15mm = 0.015m
  Torque transmission: T_in = F_piston × L_c = 300N × 0.015m ≈ 4.5 N·m
  
  This is PLENTY for a small pump
  
  Flywheel mass: Medium (0.66 kg steel, 120mm dia)
  Helps smooth oscillation while powering pump

Output speed (with eccentric cam or crankshaft):
  Base: 400 RPM piston frequency
  At steady state: ~400-800 RPM (varies with pump load)
  
Coupling to pump:
  ├─ Direct: couple pump shaft directly to crankshaft (1:1)
  ├─ Gear: use 20:40 gear pair (2:1 reduction for lower speed)
  └─ Belt: use pulleys for smooth ratio adjustment
```

### Scenario 3: Electrical Generation (Charge Battery)

```
Tiny DC generator specs:
  Available from: dead cordless tool batteries, toy motors (reversed)
  Power: 2-5 W @ 12V
  RPM: 1000-3000 RPM
  Torque: 0.01-0.05 N·m
  
  Cost: ~$2-5 (junkyard or eBay)

Gearing strategy:
  Piston input: 400 RPM
  Generator needs: 1500 RPM
  Gear ratio needed: 1500/400 = 3.75:1
  
  Use: 20T pinion on crankshaft, 75T gear on generator
  OR: Belt drive with D_out = 4× D_in

Power output:
  Input power (from piston): ~100 W
  Mechanical losses (belt, gears): ~20-30%
  Available to generator: ~70 W
  
  Electrical output: 70W × 0.85 efficiency ≈ 60 W
  At 12V: 60W / 12V = 5A current
  
  Charge 12V/5Ah battery in: 5Ah / 5A ≈ 1 hour continuous running

Schematic:
  Flywheel → Gearbox (3.75:1) → Generator → Rectifier → Battery
```

---

## ASSEMBLY DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPLETE FLYWHEEL SYSTEM                 │
└─────────────────────────────────────────────────────────────┘

From Arc Chamber:
    │
    ▼
Piston Rod (8mm, moving up/down @ 1 kHz)
    │
    ├─ Connection Link ──┐
    │  (aluminum angle)  │
    │                    │ (or eccentric follower, or belt pulley)
    │                    │
    ▼                    ▼
┌─────────────────────────────────┐
│      CRANK MECHANISM            │
│                                 │
│  ┌─────────────────────────────┐│
│  │ Crankshaft (your 55mm rod)  ││
│  │ ├─ Main journal: 6mm × 20mm ││
│  │ ├─ Crank pin: 6mm offset    ││
│  │ └─ Keyway: 2mm × 10mm       ││
│  │                              ││
│  └─────────────────────────────┘│
│         │        │               │
│         ▼        ▼               ▼
│    Bearing      Flywheel    Bearing
│  (Left side)    (120mm, 0.66kg)  (Right side)
│   6mm bore          6mm bore      6mm bore
│                                   │
│                                   ├─ Keyway for output coupling
│                                   │
│                                   ▼
│                              Optional:
│                              ├─ Pulley (belt drive)
│                              ├─ Gear (direct drive)
│                              └─ Pump shaft (direct couple)
└─────────────────────────────────────────────────────────────┘
```

---

## TUNING & CONFIGURATION WORKSHEET

**Copy this and fill in your choices:**

```
DESIGN CHOICES:
  Crank mechanism: [ ] Eccentric [ ] True crankshaft [ ] Belt drive
  
  Flywheel diameter: _____ mm
  Flywheel material: [ ] Aluminum [ ] Steel [ ] Other: _____
  Flywheel thickness: _____ mm
  Estimated flywheel mass: _____ kg
  
  Bearing type: [ ] Ball [ ] Brass bushing [ ] Polymer [ ] DIY
  
OUTPUT CONFIGURATION:
  [ ] Smoothing only (no external load)
  [ ] Pump drive (1-3W @ 500-1000 RPM)
  [ ] Electrical gen (1500+ RPM @ 2-5W)
  [ ] Secondary water dissociation
  [ ] Mechanical work / lifting load
  
  If using gears/belt:
    Input pulley/gear: _____mm / _____T
    Output pulley/gear: _____mm / _____T
    Ratio: 1:_____ (output slower/faster than input)

PERFORMANCE TARGETS:
  Steady-state RPM: _____ (goal)
  Oscillation range: ±_____ RPM (acceptable)
  Output power needed: _____ W
  Load torque: _____ N·m

FABRICATION TIME ESTIMATE:
  [ ] Eccentric cam: 2 hours
  [ ] Crankshaft: 4 hours
  [ ] Belt drive: 1 hour setup
  + 1 hour flywheel machine
  + 1 hour bearing/frame assembly
  
  TOTAL: _____ hours
```

---

## STARTING POINT RECOMMENDATION (If Unsure)

**Build THIS first (fastest, simplest):**

1. **Eccentric cam mechanism** (turns piston motion into rotation)
2. **Aluminum flywheel** (80mm diameter, 10mm thick, ~0.17 kg)
3. **Brass bushings** (DIY from scrap aluminum or bronze)
4. **Belt drive coupling** (to separate flywheel from piston if needed)
5. **Output**: Just smooth the oscillation; no external load yet

**Time**: 3-4 hours total machining
**Cost**: ~$20 (mostly the belt and small bearings)
**Result**: Stable rotating system you can test, then add load later

Once running, you can:
- Swap to heavier flywheel (add mass to existing bore)
- Add pump coupling (simple friction drive)
- Upgrade to crankshaft for smoother power if needed
- Add generator for power output

---

## NEXT STEPS

1. **Decide**: Eccentric, crankshaft, or belt drive?
2. **Dimension the flywheel**: Pick diameter and material
3. **Calculate moment of inertia**: Check I value matches your needs
4. **Plan bearing support**: DIY bracket or buy bearing blocks?
5. **Machine crankshaft** from your 55mm rod stock
6. **Turn flywheel** from aluminum or steel disk
7. **Assemble and test**: Spin by hand, then power up piston

What's your primary goal with the flywheel?
- Just smooth things out, OR
- Drive something external (pump, generator, other) ?

