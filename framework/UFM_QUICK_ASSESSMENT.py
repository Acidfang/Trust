"""
UFM Self-Sustaining Dissociation-Recombination Analysis
Quick verdict on whether system self-sustains
"""

import math

print("\n" + "="*80)
print("UFM SELF-SUSTAINING DISSOCIATION-RECOMBINATION ASSESSMENT")
print("="*80 + "\n")

# ============================================================================
# PATHWAY 1: THERMAL RECURSION
# ============================================================================

print("PATHWAY 1: THERMAL RECURSION")
print("-"*80)

# Constants
H2O_DISSOCIATION_ENERGY = 467e3  # J/mol
AVOGADRO = 6.022e23

# 1L of water ≈ 1000g = 55.5 moles
water_moles = 55.5
water_mass_kg = 1.0

# If 1% dissociates in first cycle
fraction_dissociated = 0.01
moles_reacted = water_moles * fraction_dissociated

# Energy released
energy_released = moles_reacted * H2O_DISSOCIATION_ENERGY
print(f"Moles dissociated per cycle: {moles_reacted:.2f} mol")
print(f"Energy released: {energy_released:.2e} J ({energy_released/1e3:.1f} kJ)")

# Water heat capacity: 4186 J/(kg·K)
water_heat_capacity = 4186  # J/(kg·K)
chamber_mass = 0.5  # kg (stainless steel)
chamber_heat_capacity = 500  # J/(kg·K)

total_heat_capacity = water_mass_kg * water_heat_capacity + chamber_mass * chamber_heat_capacity
temp_rise = energy_released / total_heat_capacity

print(f"Total heat capacity: {total_heat_capacity:.0f} J/K")
print(f"Temperature rise: {temp_rise:.1f} K")
print(f"Peak temperature: {298 + temp_rise:.1f} K (from 298K ambient)")

# Key question: Can this heat trigger another dissociation?
# Thermal dissociation of water requires ~1000s of K
# But assisted dissociation (with photons or ions) needs much less

thermal_threshold_unaided = 3500  # K (thermal dissociation alone)
thermal_threshold_assisted = 500  # K (with photon/ion assistance)

print(f"\nThermal dissociation threshold (unaided): {thermal_threshold_unaided} K")
print(f"Thermal dissociation threshold (with photon/ion help): {thermal_threshold_assisted} K")

temp_peak = 298 + temp_rise
thermal_sufficient = temp_peak > thermal_threshold_assisted

print(f"Temperature sufficient for ASSISTED dissociation: {thermal_sufficient}")
print(f"  → Thermal pathway: {'✓ VIABLE' if thermal_sufficient else '✗ TOO COOL'}\n")

# ============================================================================
# PATHWAY 2: PHOTON CASCADE
# ============================================================================

print("PATHWAY 2: PHOTON-TRIGGERED DISSOCIATION")
print("-"*80)

# Photon energy needed matches dissociation energy
energy_per_molecule = H2O_DISSOCIATION_ENERGY / AVOGADRO  # J
planck = 6.626e-34  # J·s
c = 3e8  # m/s

# λ = hc/E
wavelength_dissociation = planck * c / energy_per_molecule

print(f"Energy per H2O molecule: {energy_per_molecule:.2e} J")
print(f"Wavelength for dissociation photon: {wavelength_dissociation*1e9:.1f} nm (UV-C)")

# Recombination releases similar energy → photons in UV range
# ~80% of energy can go to photons
photon_energy_typical = 0.8 * energy_per_molecule
wavelength_typical = planck * c / photon_energy_typical

print(f"\nRecombination photon energy (typical): {photon_energy_typical:.2e} J")
print(f"Recombination photon wavelength: {wavelength_typical*1e9:.1f} nm")

# Can these photons break H-O bonds?
photon_strong_enough = photon_energy_typical > 0.5 * energy_per_molecule

print(f"Photons above 50% dissociation threshold: {photon_strong_enough}")

# How many photons from one dissociation?
moles_dissociated_per_event = water_moles * 0.01  # 1% per cycle
molecules_dissociated = moles_dissociated_per_event * AVOGADRO
photons_per_molecule_avg = 2.5  # rough estimate
photons_generated = molecules_dissociated * photons_per_molecule_avg

print(f"\nPhotons generated per dissociation cycle: {photons_generated:.2e}")

# Absorption probability - water absorbs UV photons
# Cross-section for water ~1e-20 m^2, path ~0.1m, density ~55 mol/L
absorption_prob = 0.15  # ~15% of photons get absorbed

print(f"Absorption probability in chamber: {absorption_prob:.1%}")

photons_absorbed = photons_generated * absorption_prob
new_dissociations = photons_absorbed / 2.5  # each set of ~2-3 photons triggers one

print(f"Photons absorbed: {photons_absorbed:.2e}")
print(f"NEW dissociations triggered: {new_dissociations:.2e}")

cascade_multiplier = new_dissociations / molecules_dissociated if molecules_dissociated > 0 else 0

print(f"\nCascade multiplier per generation: {cascade_multiplier:.2f}")

if cascade_multiplier > 1.0:
    print("  → Cascade EXPONENTIALLY GROWS")
    photon_verdict = True
elif cascade_multiplier > 0.5:
    print("  → Cascade SUSTAINS (slow)")
    photon_verdict = True
else:
    print("  → Cascade DIES OUT")
    photon_verdict = False

print(f"  → Photon pathway: {'✓ VIABLE' if photon_verdict else '✗ INSUFFICIENT'}\n")

# ============================================================================
# PATHWAY 3: ION CASCADE
# ============================================================================

print("PATHWAY 3: ION CASCADE PERSISTENCE")
print("-"*80)

# Ions created from excited species during recombination
initial_ion_fraction = 0.005  # 0.5% of dissociated atoms become ions
ions_created = molecules_dissociated * 2 * initial_ion_fraction  # ×2 for H and O atoms

print(f"Ion density after recombination: {ions_created:.2e} ions")

# Plasma frequency: f_p = sqrt(n*e^2/(m*eps_0))
# Quick formula: f_p (Hz) ≈ 9e9 * sqrt(n_m^-3)
# where n is electron density

electron_density_per_liter = ions_created  # roughly
electron_density_per_m3 = electron_density_per_liter * 1000  # convert

# Plasma frequency rough calculation
plasma_freq = 9e9 * math.sqrt(max(electron_density_per_m3, 1))

print(f"Electron density: {electron_density_per_m3:.2e} m^-3")
print(f"Plasma frequency: {plasma_freq:.2e} Hz ({plasma_freq/1e6:.1f} MHz)")

# Ion recombination lifetime
# α (recombination coeff) ~ 1e-12 m^3/s at 300K, scales as T^-0.5
# τ_rec ~ 1/(α*n_oppositie)

alpha_recomb = 1e-12  # m^3/s
T_plasma = 2000  # K (estimated after recombination)
alpha_at_T = alpha_recomb * math.sqrt(300/T_plasma)

ion_lifetime = 1.0 / (alpha_at_T * max(electron_density_per_m3/2, 1e10)) if electron_density_per_m3 > 0 else 100

print(f"Recombination coefficient at {T_plasma}K: {alpha_at_T:.2e} m^3/s")
print(f"Ion lifetime before recombination: {ion_lifetime:.2e} seconds ({ion_lifetime*1000:.3f} ms)")

# Can plasma persist long enough to interact with next cycle?
# Need ions to last at least 1 microsecond
ion_persistent = ion_lifetime > 1e-6

print(f"Ions persist >1μs: {ion_persistent}")

# Can plasma frequency support energy exchange?
# Need f_p > kHz (for reasonable heartbeat)
freq_sufficient = plasma_freq > 1e3

print(f"Plasma frequency sufficient: {freq_sufficient}")

ion_verdict = ion_persistent and freq_sufficient

print(f"  → Ion pathway: {'✓ VIABLE' if ion_verdict else '✗ INSUFFICIENT'}\n")

# ============================================================================
# SYNTHESIS
# ============================================================================

print("="*80)
print("SYNTHESIS: SELF-SUSTAINABILITY VERDICT")
print("="*80 + "\n")

viable_count = sum([thermal_sufficient, photon_verdict, ion_verdict])

print(f"Thermal recursion:        {'✓ VIABLE' if thermal_sufficient else '✗ Not viable'}")
print(f"Photon cascade:           {'✓ VIABLE' if photon_verdict else '✗ Not viable'}")
print(f"Ion persistence:          {'✓ VIABLE' if ion_verdict else '✗ Not viable'}")
print()
print(f"TOTAL VIABLE PATHWAYS: {viable_count}/3")
print()

if viable_count >= 2:
    verdict = "SELF-SUSTAINS WITH MARGIN"
    advice = """
System likely SELF-SUSTAINS after bootstrap.
  ✓ Multiple redundant mechanisms
  ✓ Failure of one pathway still allows continuation via others
  ✓ High probability of stable oscillation
  
Action: Bootstrap with single ZVS arc pulse. System should continue indefinitely.
The heat harvested can power the 555 timer or maintain thermal conditions.
"""
elif viable_count == 1:
    verdict = "SELF-SUSTAINS (FRAGILE)"
    advice = """
System marginally SELF-SUSTAINS via single pathway.
  ⚠ No redundancy—any failure stops system
  ⚠ Conditions must be precisely maintained
  
Action: Bootstrap, then monitor. Keep 555 timer ready as fallback trigger.
"""
else:
    verdict = "REQUIRES EXTERNAL TRIGGER"
    advice = """
No self-sustaining mechanism is sufficient.
  ✗ System needs continuous power to maintain heartbeat
  
Action: Use 555 timer oscillator at 1 kHz.
Byproducts (heat, light, ions) still harvestable as power source.
No dissociation-recombination is wasted—all energy captured.
"""

print(f"VERDICT: {verdict}")
print("\n" + advice)

print("\n" + "="*80)
print("END ASSESSMENT")
print("="*80 + "\n")
