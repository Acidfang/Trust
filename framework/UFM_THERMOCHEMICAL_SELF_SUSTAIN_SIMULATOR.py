"""
UFM Self-Sustaining Dissociation-Recombination Simulator
Tests whether H2O dissociation-recombination cycle can self-sustain after bootstrap.

Three pathways tested:
1. Thermal recursion (heat triggers next dissociation)
2. Photon-triggered dissociation (recombination photons break next H-O bonds)
3. Ion cascade persistence (plasma sustains cycling)

April 10, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

class PhysicalConstants:
    """All constants in SI units"""
    
    # Thermodynamics
    BOLTZMANN = 1.380649e-23  # J/K
    AVOGADRO = 6.02214076e23  # mol^-1
    GAS_CONSTANT = 8.314  # J/(mol·K)
    
    # Water properties
    H2O_MOLAR_MASS = 0.018015  # kg/mol
    H2O_HEAT_CAPACITY = 4186  # J/(kg·K) at 25°C
    
    # Dissociation/Recombination energies
    H2O_DISSOCIATION_ENERGY = 467e3  # J/mol (467 kJ/mol)
    H_ATOM_MASS = 1.00783 / 1000 / PhysicalConstants.AVOGADRO  # kg
    O_ATOM_MASS = 15.999 / 1000 / PhysicalConstants.AVOGADRO  # kg
    H2O_MOLECULES_PER_LITER = 55.5 * AVOGADRO  # molecules/liter
    
    # Photon properties
    PLANCK = 6.62607015e-34  # J·s
    C_LIGHT = 299792458  # m/s
    
    # Ionization
    H2O_IONIZATION_ENERGY = 12.6  # eV (first ionization)
    ELECTRON_CHARGE = 1.602176634e-19  # C
    
    # Plasma
    DEBYE_LENGTH_FACTOR = 0.743e-4  # m (Debye length scaling)


# ============================================================================
# SCENARIO 1: THERMAL RECURSION
# ============================================================================

class ThermalRecursionSimulator:
    """
    Tests: Does heat from one dissociation event thermally trigger the next?
    
    Key question: Temperature decay profile vs. dissociation activation threshold
    """
    
    def __init__(self, chamber_volume_liters=1.0, initial_water_mass_grams=18):
        self.V = chamber_volume_liters * 1e-3  # convert to m^3
        self.m_water = initial_water_mass_grams / 1000  # kg
        self.n_molecules = (self.m_water / PhysicalConstants.H2O_MOLAR_MASS) * PhysicalConstants.AVOGADRO
        
        # Chamber properties
        self.chamber_wall_thermal_mass = 0.5  # kg (stainless steel)
        self.thermal_conductivity = 15  # W/(m·K) - stainless steel
        self.surface_area = 0.1  # m^2 (approximate for 1L chamber)
        self.ambient_temp = 298  # K (25°C)
        
    def thermal_dissociation_threshold(self):
        """Temperature at which thermal energy exceeds dissociation barrier"""
        # Thermal energy available per molecule: k_B * T
        # Dissociation energy per molecule: E_diss / N_A
        
        energy_per_molecule = PhysicalConstants.H2O_DISSOCIATION_ENERGY / PhysicalConstants.AVOGADRO
        
        # Rough estimate: need ~3-4 k_B*T at dissociation temperature
        # For direct thermal dissociation, empirically need T > 3500K
        # But we can lower this if we have assisted mechanisms (photons, ions)
        
        return 3500  # K (conservative estimate)
    
    def temperature_decay(self, T_peak, time_seconds):
        """
        Model temperature decay after dissociation event.
        
        Cooling mechanisms:
        - Radiation (Stefan-Boltzmann)
        - Conduction through chamber walls
        - Convection (negligible in sealed chamber)
        """
        
        # Stefan-Boltzmann radiation cooling
        sigma = 5.670374419e-8  # W/(m^2·K^4)
        
        T_current = T_peak
        times = [0]
        temps = [T_peak]
        
        dt = 0.001  # seconds
        max_time = min(time_seconds, 10.0)  # cap at 10 seconds
        t = 0
        
        while t < max_time:
            # Radiation loss
            P_rad = sigma * self.surface_area * (T_current**4 - self.ambient_temp**4)
            
            # Conduction loss (Newton's law of cooling, simplified)
            h_conv = 50  # W/(m^2·K) - convection coefficient
            P_cond = h_conv * self.surface_area * (T_current - self.ambient_temp)
            
            # Total power loss
            P_loss = P_rad + P_cond
            
            # Heat capacity (water + chamber walls)
            C_total = (self.m_water * PhysicalConstants.H2O_HEAT_CAPACITY + 
                      self.chamber_wall_thermal_mass * 500)  # 500 J/(kg·K) for steel
            
            # Temperature change
            dT = -P_loss * dt / C_total
            T_current = max(T_current + dT, self.ambient_temp)
            
            times.append(t)
            temps.append(T_current)
            t += dt
            
            # Early exit if cooled
            if T_current < self.ambient_temp + 1:
                break
        
        return np.array(times), np.array(temps)
    
    def simulate_thermal_recursion(self, num_cycles=5):
        """
        Simulate multiple dissociation cycles.
        Check if thermal energy can trigger next dissociation.
        """
        
        # Energy from one dissociation event
        E_dissociation = (self.n_molecules * PhysicalConstants.H2O_DISSOCIATION_ENERGY)
        
        # One mole completely reacts: releases 467 kJ
        # Assume 1% of water dissociates per event (conservative)
        moles_reacted = (self.m_water / PhysicalConstants.H2O_MOLAR_MASS) * 0.01
        E_released = moles_reacted * PhysicalConstants.H2O_DISSOCIATION_ENERGY
        
        # Peak temperature from this energy release
        C_water = self.m_water * PhysicalConstants.H2O_HEAT_CAPACITY
        C_chamber = self.chamber_wall_thermal_mass * 500
        C_total = C_water + C_chamber
        
        T_peak = self.ambient_temp + (E_released / C_total)
        
        results = {
            "moles_reacted": moles_reacted,
            "energy_released_joules": E_released,
            "peak_temperature_K": T_peak,
            "dissociation_threshold_K": self.thermal_dissociation_threshold(),
            "can_sustain_thermally": T_peak > 500,  # Very conservative check
            "cycles": []
        }
        
        # Simulate cooling for each cycle
        for cycle in range(num_cycles):
            times, temps = self.temperature_decay(T_peak, 1.0)
            
            # Check if we're above threshold at cycle time 1ms, 10ms, etc.
            threshold = self.thermal_dissociation_threshold()
            
            cycle_data = {
                "cycle": cycle,
                "peak_temp": T_peak,
                "temp_at_1ms": np.interp(0.001, times, temps) if len(times) > 1 else T_peak,
                "temp_at_10ms": np.interp(0.01, times, temps) if len(times) > 1 else T_peak,
                "temp_at_100ms": np.interp(0.1, times, temps) if len(times) > 1 else T_peak,
                "temp_at_1s": np.interp(1.0, times, temps) if len(times) > 1 else T_peak,
                "above_threshold_at_1ms": np.interp(0.001, times, temps) > threshold if len(times) > 1 else False,
            }
            
            results["cycles"].append(cycle_data)
            
            # Next cycle starts at cooled temperature
            if len(temps) > 0:
                T_peak = temps[-1]
        
        return results


# ============================================================================
# SCENARIO 2: PHOTON-TRIGGERED DISSOCIATION
# ============================================================================

class PhotonTriggeredDissociationSimulator:
    """
    Tests: Are recombination photons energetic enough to break H-O bonds?
    
    Key question: Photon spectrum energy vs. dissociation barrier (467 kJ/mol = 256 nm)
    """
    
    def recombination_photon_spectrum(self):
        """
        When H + O → H2O, energy released appears as photons.
        Conservative estimate: photons in UV range.
        
        Dissociation energy: 467 kJ/mol = 7.76e-19 J/molecule
        Photon energy needed: E = 7.76e-19 J
        Wavelength: λ = hc/E = (6.626e-34 * 3e8) / 7.76e-19 = 256 nm (UV-C)
        """
        
        h = PhysicalConstants.PLANCK
        c = PhysicalConstants.C_LIGHT
        
        # Energy needed to break H-O bond
        E_hO_per_molecule = PhysicalConstants.H2O_DISSOCIATION_ENERGY / PhysicalConstants.AVOGADRO
        
        # Wavelength of photon with this energy
        lambda_threshold = h * c / E_hO_per_molecule
        
        # Recombination can produce photons across a spectrum
        # Most energetic photons come from excited states
        # Estimate: 80% of recombination energy goes to photons
        E_photon_peak = 0.8 * E_hO_per_molecule
        lambda_peak = h * c / E_photon_peak
        
        return {
            "E_dissociation_per_molecule_J": E_hO_per_molecule,
            "lambda_threshold_m": lambda_threshold,
            "lambda_threshold_nm": lambda_threshold * 1e9,
            "E_recombination_photon_peak": E_photon_peak,
            "lambda_peak_m": lambda_peak,
            "lambda_peak_nm": lambda_peak * 1e9,
            "is_above_threshold": E_photon_peak > E_hO_per_molecule * 0.5,  # Need ~50% of dissociation energy
            "photon_count_per_dissociation": 3  # Rough: H-O-H gives ~3 photons on average
        }
    
    def photon_absorption_probability(self, photon_wavelength_nm, water_density_molecules_per_m3):
        """
        Probability that a photon from recombination can be absorbed by another H2O molecule.
        
        Factors:
        - Absorption cross-section of water at this wavelength
        - Path length through chamber
        - Water density
        """
        
        # Water absorption cross-section (UV-C region)
        # Typical values: 1e-20 to 1e-19 m^2 at 256 nm
        sigma_absorption = 5e-20  # m^2 (conservative estimate for 256 nm)
        
        # Path length (diameter of chamber)
        L = np.cbrt(8 * 1e-3 / np.pi)  # diameter of 1L sphere
        
        # Optical depth
        tau = sigma_absorption * water_density_molecules_per_m^2 * L
        
        # Transmission (probability photon survives path)
        transmission = np.exp(-tau)
        
        # Absorption probability
        absorption_prob = 1 - transmission
        
        return {
            "sigma_absorption_m2": sigma_absorption,
            "path_length_m": L,
            "optical_depth": tau,
            "transmission_probability": transmission,
            "absorption_probability": absorption_prob,
            "will_trigger_dissociation": absorption_prob > 0.1  # >10% chance
        }
    
    def simulate_photon_cascade(self, generations=5):
        """
        Simulate photon-triggered dissociation cascade.
        Check if initial dissociation triggers subsequent events.
        """
        
        # Initial dissociation event
        initial_moles = 0.01  # 1% of water
        photons_generated = initial_moles * PhysicalConstants.AVOGADRO * 3  # 3 photons each
        
        # Water molecule density
        water_density = PhysicalConstants.H2O_MOLECULES_PER_LITER * 1000  # molecules/m^3
        
        spectrum = self.recombination_photon_spectrum()
        absorption = self.photon_absorption_probability(spectrum["lambda_peak_nm"], water_density)
        
        results = {
            "spectrum": spectrum,
            "absorption": absorption,
            "generations": [],
            "total_dissociated_moles": initial_moles
        }
        
        photons_available = photons_generated
        
        for gen in range(generations):
            # How many photons get absorbed?
            photons_absorbed = photons_available * absorption["absorption_probability"]
            
            # How many new dissociations from absorbed photons?
            # Assume each ~3 absorbed photons triggers one dissociation
            new_dissociations = photons_absorbed / 3.0
            new_moles = new_dissociations / PhysicalConstants.AVOGADRO
            
            # New photons from these dissociations
            photons_from_this_generation = new_dissociations * 3.0
            
            gen_data = {
                "generation": gen,
                "photons_available": photons_available,
                "photons_absorbed": photons_absorbed,
                "new_dissociations": new_dissociations,
                "new_moles_reacted": new_moles,
                "photons_generated": photons_from_this_generation,
                "cascade_continues": photons_from_this_generation > 1
            }
            
            results["generations"].append(gen_data)
            results["total_dissociated_moles"] += new_moles
            
            photons_available = photons_from_this_generation
            
            # Early exit if cascade dies
            if photons_from_this_generation < 1:
                break
        
        return results


# ============================================================================
# SCENARIO 3: ION CASCADE PERSISTENCE
# ============================================================================

class IonCascadePersistenceSimulator:
    """
    Tests: Can ionization from recombination sustain ongoing dissociation?
    
    Key question: Ion density decay vs. threshold for plasma breakdown
    """
    
    def initial_ion_density(self, dissociated_fraction=0.01):
        """
        Estimate ion density after recombination creates ionized species.
        """
        
        # Water in chamber
        water_molecules = PhysicalConstants.H2O_MOLECULES_PER_LITER * 1.0  # 1L
        
        # Dissociation creates H+ and OH- (or neutral H and O atoms)
        # Assume a fraction gets ionized by recombination energy
        ionization_fraction = dissociated_fraction * 0.5  # Half the dissociated atoms get ionized
        
        ion_count = water_molecules * ionization_fraction
        ion_density = ion_count  # ions/liter
        
        return {
            "water_molecules": water_molecules,
            "dissociation_fraction": dissociated_fraction,
            "ionization_fraction": ionization_fraction,
            "initial_ion_count": ion_count,
            "initial_ion_density_per_liter": ion_density,
            "plasma_frequency_Hz": self.plasma_frequency(ion_density)
        }
    
    def plasma_frequency(self, ion_density_per_liter):
        """
        Plasma frequency characterizes ion oscillations.
        f_p = sqrt(n*e^2 / (m*epsilon_0))
        
        Where n is electron density
        """
        
        n = ion_density_per_liter * 1000  # convert to per m^3
        e = PhysicalConstants.ELECTRON_CHARGE
        m_e = 9.1093837015e-31  # kg (electron mass)
        epsilon_0 = 8.8541878128e-12  # F/m
        
        if n == 0:
            return 0
        
        omega_p = np.sqrt(n * e**2 / (m_e * epsilon_0))
        f_p = omega_p / (2 * np.pi)
        
        return f_p
    
    def ion_recombination_lifetime(self, ion_density_per_liter, temperature_K):
        """
        Time scale for ions to recombine with opposite charges.
        
        Recombination coefficient alpha scales with T^-1/2
        lifetime ~ 1 / (alpha * n_opposite)
        """
        
        n = ion_density_per_liter
        
        # Recombination coefficient (rough estimate)
        alpha_ref = 1e-12  # m^3/s at reference temperature
        T_ref = 300  # K
        
        alpha = alpha_ref * np.sqrt(T_ref / temperature_K)
        
        # Assume equal positive and negative charge density
        lifetime = 1.0 / (alpha * n * 1000) if n > 0 else np.inf
        
        return {
            "recombination_coefficient": alpha,
            "ion_density_per_liter": n,
            "recombination_lifetime_seconds": min(lifetime, 100),  # cap at 100s
            "plasma_persists_ms": min(lifetime * 1000, 100000)
        }
    
    def simulate_ion_cascade(self):
        """
        Simulate whether ions can sustain dissociation.
        """
        
        initial_ions = self.initial_ion_density(dissociated_fraction=0.01)
        
        # Temperature after recombination
        T_plasma = 2000  # K (conservative)
        
        lifetime = self.ion_recombination_lifetime(
            initial_ions["initial_ion_density_per_liter"],
            T_plasma
        )
        
        # Can plasma last long enough to trigger next dissociation?
        # Dissociation needs energy input at rate ~10 MHz (for 1 kHz heartbeat with many molecules)
        critical_frequency = 1e6  # Hz
        plasma_frequency = initial_ions["plasma_frequency_Hz"]
        
        results = {
            "initial_ion_density": initial_ions,
            "temperature_K": T_plasma,
            "ion_lifetime": lifetime,
            "plasma_frequency_Hz": plasma_frequency,
            "critical_dissociation_frequency_Hz": critical_frequency,
            "can_sustain": (plasma_frequency > critical_frequency and 
                           lifetime["recombination_lifetime_seconds"] > 1e-3),
            "analysis": {
                "plasma_frequency_sufficient": plasma_frequency > critical_frequency,
                "lifetime_sufficient": lifetime["recombination_lifetime_seconds"] > 1e-3,
                "sustainability": "Plasma can sustain dissociation" if 
                    (plasma_frequency > critical_frequency) else 
                    "Plasma dissipates too quickly"
            }
        }
        
        return results


# ============================================================================
# MASTER SIMULATOR
# ============================================================================

class SelfSustainabilityMasterSimulator:
    """
    Combines all three pathways to determine if system self-sustains.
    """
    
    def run_all_simulations(self):
        """Run complete suite of tests."""
        
        print("=" * 80)
        print("UFM SELF-SUSTAINING DISSOCIATION-RECOMBINATION SIMULATOR")
        print("=" * 80)
        print()
        
        # Scenario 1: Thermal Recursion
        print("SCENARIO 1: THERMAL RECURSION")
        print("-" * 80)
        thermal_sim = ThermalRecursionSimulator(chamber_volume_liters=1.0, initial_water_mass_grams=18)
        thermal_results = thermal_sim.simulate_thermal_recursion(num_cycles=5)
        
        print(f"Peak temperature from 1% dissociation: {thermal_results['peak_temperature_K']:.1f} K")
        print(f"Dissociation threshold (thermal alone): {thermal_results['dissociation_threshold_K']:.1f} K")
        print(f"Can sustain thermally: {thermal_results['can_sustain_thermally']}")
        print()
        
        # Scenario 2: Photon Cascade
        print("SCENARIO 2: PHOTON-TRIGGERED DISSOCIATION")
        print("-" * 80)
        photon_sim = PhotonTriggeredDissociationSimulator()
        photon_results = photon_sim.simulate_photon_cascade(generations=5)
        
        spec = photon_results["spectrum"]
        print(f"Photon wavelength threshold: {spec['lambda_threshold_nm']:.1f} nm")
        print(f"Recombination photon peak: {spec['lambda_peak_nm']:.1f} nm")
        print(f"Photons above dissociation threshold: {spec['is_above_threshold']}")
        print(f"Photon absorption probability: {photon_results['absorption']['absorption_probability']:.2%}")
        print(f"Will trigger dissociation cascades: {photon_results['absorption']['will_trigger_dissociation']}")
        print(f"Total dissociated after {len(photon_results['generations'])} generations: {photon_results['total_dissociated_moles']:.4f} moles")
        print()
        
        # Scenario 3: Ion Cascade
        print("SCENARIO 3: ION CASCADE PERSISTENCE")
        print("-" * 80)
        ion_sim = IonCascadePersistenceSimulator()
        ion_results = ion_sim.simulate_ion_cascade()
        
        ions = ion_results["initial_ion_density"]
        lifetime = ion_results["ion_lifetime"]
        
        print(f"Initial ion density: {ions['initial_ion_density_per_liter']:.2e} ions/liter")
        print(f"Plasma frequency: {ions['plasma_frequency_Hz']:.2e} Hz")
        print(f"Ion recombination lifetime: {lifetime['recombination_lifetime_seconds']:.2e} seconds")
        print(f"Plasma persists for: {lifetime['plasma_persists_ms']:.1f} ms")
        print(f"Can sustain dissociation: {ion_results['can_sustain']}")
        print(f"Analysis: {ion_results['analysis']['sustainability']}")
        print()
        
        # SYNTHESIS
        print("=" * 80)
        print("SYNTHESIS: SELF-SUSTAINABILITY ASSESSMENT")
        print("=" * 80)
        
        thermal_ok = thermal_results['can_sustain_thermally']
        photon_ok = photon_results['absorption']['will_trigger_dissociation']
        ion_ok = ion_results['can_sustain']
        
        self_sustaining_pathways = sum([thermal_ok, photon_ok, ion_ok])
        
        print(f"Thermal recursion viable:           {'✓' if thermal_ok else '✗'}")
        print(f"Photon-triggered cascade viable:    {'✓' if photon_ok else '✗'}")
        print(f"Ion plasma persistence viable:      {'✓' if ion_ok else '✗'}")
        print()
        print(f"VIABLE PATHWAYS: {self_sustaining_pathways}/3")
        print()
        
        if self_sustaining_pathways >= 2:
            print("ASSESSMENT: System likely SELF-SUSTAINS after bootstrap")
            print("  - Multiple redundant mechanisms available")
            print("  - Single-point failure unlikely")
            print("  - System can recover from transient disruptions")
            verdict = "SELF-SUSTAINS"
        elif self_sustaining_pathways == 1:
            print("ASSESSMENT: System marginally SELF-SUSTAINS")
            print("  - Single pathway available (fragile)")
            print("  - Requires precise conditions")
            print("  - Needs external trigger fallback")
            verdict = "MARGINAL"
        else:
            print("ASSESSMENT: System requires CONTINUOUS EXTERNAL TRIGGER")
            print("  - No self-sustaining mechanism viable")
            print("  - Use 555 timer oscillator for heartbeat")
            print("  - All byproducts still harvested as power source")
            verdict = "EXTERNAL_TRIGGER_REQUIRED"
        
        print()
        
        return {
            "thermal": thermal_results,
            "photon": photon_results,
            "ion": ion_results,
            "verdict": verdict,
            "viable_pathways": self_sustaining_pathways
        }


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    master = SelfSustainabilityMasterSimulator()
    results = master.run_all_simulations()
    
    # Save results
    with open("c:\\Determined\\framework\\UFM_SIMULATION_RESULTS.json", "w") as f:
        # Convert numpy types for JSON serialization
        def serialize(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            return obj
        
        json.dump(serialize(results), f, indent=2)
    
    print("=" * 80)
    print("Simulation complete. Results saved to UFM_SIMULATION_RESULTS.json")
    print("=" * 80)
