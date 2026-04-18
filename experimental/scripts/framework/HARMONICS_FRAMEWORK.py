"""
HARMONICS FRAMEWORK: Universal resonance/relationship system across all domains

Key insight: Harmonics aren't unique to audio. They appear everywhere:
  - AUDIO: Harmonic series, overtones, frequency ratios
  - VISUAL/MOLECULAR: Resonance structures, electron shell harmonics, symmetry harmonics
  - COMPUTE: CPU frequency harmonics, cache line resonance, network latency harmonics
  - AGENTS: Decision branching harmonics, consensus patterns
  - LEDGER: Transaction pattern harmonics, causality resonance

Harmonics = relationships where small parts resonate with the whole.
Harmonics = emergent patterns from entity interactions.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


# ============================================================================
# UNIVERSAL HARMONIC TYPES
# ============================================================================

class HarmonicType(Enum):
    """Types of harmonics across all domains."""
    # Audio domain
    FREQUENCY_HARMONIC = "frequency_harmonic"      # 1x, 2x, 3x fundamental frequency
    OVERTONE = "overtone"                          # Natural frequency partials
    INTERFERENCE = "interference"                  # Constructive/destructive wave patterns
    
    # Visual/Molecular domain
    RESONANCE_STRUCTURE = "resonance_structure"    # Electron delocalization patterns
    ELECTRON_SHELL_HARMONIC = "electron_shell_harmonic"  # Orbital symmetry patterns
    SYMMETRY_HARMONIC = "symmetry_harmonic"        # Molecular symmetry operations
    BONDING_HARMONIC = "bonding_harmonic"          # Resonance bonding patterns
    ORBITAL_HYBRID = "orbital_hybrid"              # sp/sp2/sp3 hybridization resonance
    
    # Compute domain
    FREQUENCY_RESONANCE = "frequency_resonance"    # CPU clock harmonics with processes
    CACHE_RESONANCE = "cache_resonance"            # Memory line coherency patterns
    NETWORK_HARMONIC = "network_harmonic"          # Latency period harmonics
    
    # Agent domain
    CONSENSUS_HARMONIC = "consensus_harmonic"      # Agreement patterns across agents
    DECISION_RESONANCE = "decision_resonance"      # Branching path harmonics
    
    # Ledger domain
    TRANSACTION_RHYTHM = "transaction_rhythm"      # Pattern in TX timing
    CAUSALITY_CHAIN = "causality_chain"            # Sequential resonance


@dataclass
class Harmonic:
    """Universal harmonic representation.
    
    Represents any resonant relationship in the system.
    Can be between frequencies, molecular orbitals, CPU cycles, agent decisions, etc.
    """
    harmonic_type: str
    fundamental: float                      # Base frequency/property (domain-specific)
    multiplier: float = 1.0                 # n-th harmonic (2x = octave, 3x = fifth, etc)
    amplitude: float = 1.0                  # Strength of this harmonic (0-1)
    phase_offset: float = 0.0               # Phase shift (0-2π or 0-1 normalized)
    entities_involved: List[str] = field(default_factory=list)  # Which entities participate
    properties: Dict = field(default_factory=dict)  # Domain-specific properties
    
    @property
    def frequency(self) -> float:
        """Compute actual frequency/value of this harmonic."""
        return self.fundamental * self.multiplier
    
    @property
    def wavelength(self) -> float:
        """If interpreted as wave, what's the wavelength?"""
        if self.frequency <= 0:
            return float('inf')
        return 1.0 / self.frequency
    
    @property
    def energy_contribution(self) -> float:
        """Energy contribution of this harmonic (proportional to amplitude squared)."""
        return (self.amplitude ** 2) * self.multiplier  # Higher harmonics weighted by multiplier
    
    def __repr__(self) -> str:
        freq = f"{self.frequency:.1f}" if self.frequency > 0 else "∞"
        return f"Harmonic({self.harmonic_type}, n={self.multiplier}, f={freq}, A={self.amplitude:.2f})"


# ============================================================================
# HARMONIC PATTERNS FOR EACH DOMAIN
# ============================================================================

class AudioHarmonics:
    """Harmonics patterns for audio domain."""
    
    @staticmethod
    def create_harmonic_series(fundamental_freq: float, num_harmonics: int = 8) -> List[Harmonic]:
        """Create natural harmonic series (1x, 2x, 3x, 4x, etc).
        
        E.g., A4 (440 Hz) → 440Hz, 880Hz, 1320Hz, 1760Hz, ...
        This is the overtone series.
        """
        harmonics = []
        for n in range(1, num_harmonics + 1):
            harmonic = Harmonic(
                harmonic_type=HarmonicType.FREQUENCY_HARMONIC.value,
                fundamental=fundamental_freq,
                multiplier=float(n),
                amplitude=1.0 / n,  # Higher harmonics weaker (natural timbre)
            )
            harmonics.append(harmonic)
        return harmonics
    
    @staticmethod
    def create_musical_interval(freq1: float, freq2: float) -> Harmonic:
        """Create harmonic representing musical interval between two frequencies.
        
        E.g., C (261Hz) to G (392Hz) is a perfect fifth (ratio 3:2)
        """
        ratio = freq2 / freq1
        multiplier = ratio if ratio > 1 else 1 / ratio
        
        return Harmonic(
            harmonic_type=HarmonicType.OVERTONE.value,
            fundamental=min(freq1, freq2),
            multiplier=multiplier,
            amplitude=0.8,
            properties={"interval_name": interval_name_from_ratio(ratio)}
        )
    
    @staticmethod
    def detect_interference(freqs: List[float]) -> List[Harmonic]:
        """Detect interference patterns between frequencies.
        
        When two frequencies close in value play, they create beat patterns.
        """
        interference_patterns = []
        for i in range(len(freqs)):
            for j in range(i + 1, len(freqs)):
                beat_freq = abs(freqs[i] - freqs[j])
                harmonic = Harmonic(
                    harmonic_type=HarmonicType.INTERFERENCE.value,
                    fundamental=beat_freq,
                    multiplier=1.0,
                    amplitude=0.5 * min(1.0, beat_freq / 50),  # Weaker if beat freq low
                    properties={"freq1": freqs[i], "freq2": freqs[j], "beat_frequency": beat_freq}
                )
                interference_patterns.append(harmonic)
        return interference_patterns


class VisualHarmonics:
    """Harmonics patterns for visual/molecular domain."""
    
    @staticmethod
    def create_resonance_structures(atom_id: str, num_structures: int = 3) -> List[Harmonic]:
        """Create resonance structure harmonics (electron delocalization patterns).
        
        In benzene, electrons resonate across 3 structure forms (Kekule structures).
        Each delocalization pattern is a "harmonic" of the molecular structure.
        """
        harmonics = []
        for n in range(1, num_structures + 1):
            harmonic = Harmonic(
                harmonic_type=HarmonicType.RESONANCE_STRUCTURE.value,
                fundamental=n,  # Structure index
                multiplier=float(n),
                amplitude=1.0 / n,  # Earlier structures more probable
                entities_involved=[atom_id],
                properties={"structure_index": n, "contribution": 1.0 / n}
            )
            harmonics.append(harmonic)
        return harmonics
    
    @staticmethod
    def create_electron_shell_harmonics(element: str, valence_electrons: int) -> List[Harmonic]:
        """Create electron shell harmonics based on orbital patterns.
        
        Electron shells have natural harmonic patterns (s, p, d, f orbitals).
        s orbital: 1 lobe (fundamental)
        p orbital: 2 lobes (1:1 resonance)
        d orbital: 4 lobes (1:1:1:1 resonance)
        f orbital: 6 lobes (complex resonance)
        """
        orbital_patterns = {
            "s": (1, 1.0),      # 1 node, fundamental freq
            "p": (2, 2.0),      # 2 nodes, octave harmonic
            "d": (4, 4.0),      # 4 nodes, double octave
            "f": (6, 6.0),      # 6 nodes, sixth harmonic
        }
        
        harmonics = []
        orbital_sequence = "sp" if valence_electrons <= 2 else "spd" if valence_electrons <= 10 else "spdf"
        
        for orbital_type in orbital_sequence:
            num_lobes, harmonic_mult = orbital_patterns[orbital_type]
            harmonic = Harmonic(
                harmonic_type=HarmonicType.ELECTRON_SHELL_HARMONIC.value,
                fundamental=valence_electrons,
                multiplier=harmonic_mult,
                amplitude=1.0 / harmonic_mult,
                properties={"orbital": orbital_type, "num_lobes": num_lobes, "electron_density": harmonic_mult}
            )
            harmonics.append(harmonic)
        
        return harmonics
    
    @staticmethod
    def create_symmetry_harmonics(symmetry_point_group: str) -> List[Harmonic]:
        """Create harmonics from molecular symmetry operations.
        
        Symmetry point groups have harmonic structure:
        C2v: 2-fold rotation (1:1 resonance)
        D3h: 3-fold rotation (1:1:1 resonance)
        Oh: octahedral (4-fold, 3-fold, 2-fold rotations)
        """
        symmetry_patterns = {
            "C2v": 2,
            "C3v": 3,
            "D3h": 3,
            "T": 4,
            "Oh": 8,
            "Ih": 12,
        }
        
        harmonics = []
        n_sym = symmetry_patterns.get(symmetry_point_group, 2)
        
        for harmonic_n in range(1, n_sym + 1):
            harmonic = Harmonic(
                harmonic_type=HarmonicType.SYMMETRY_HARMONIC.value,
                fundamental=n_sym,
                multiplier=float(harmonic_n),
                amplitude=1.0 / harmonic_n,
                properties={"point_group": symmetry_point_group, "symmetry_order": n_sym}
            )
            harmonics.append(harmonic)
        
        return harmonics
    
    @staticmethod
    def create_bonding_harmonics(bond_type: str, bond_order: int) -> List[Harmonic]:
        """Create harmonics from bonding patterns.
        
        Single bond: σ (1 harmonic)
        Double bond: σ + π (2 harmonics with interference)
        Triple bond: σ + 2π (3 harmonics)
        Aromatic: delocalized n-th harmonic resonance
        """
        if bond_type == "single":
            harmonic_count = 1
        elif bond_type == "double":
            harmonic_count = 2
        elif bond_type == "triple":
            harmonic_count = 3
        elif bond_type == "aromatic":
            harmonic_count = bond_order  # Multiple delocalized harmonics
        else:
            harmonic_count = 1
        
        harmonics = []
        for n in range(1, harmonic_count + 1):
            harmonic = Harmonic(
                harmonic_type=HarmonicType.BONDING_HARMONIC.value,
                fundamental=n,
                multiplier=float(n),
                amplitude=1.0 / n,
                properties={"bond_type": bond_type, "orbital_type": "sigma" if n == 1 else "pi"}
            )
            harmonics.append(harmonic)
        
        return harmonics


class ComputeHarmonics:
    """Harmonics patterns for compute domain."""
    
    @staticmethod
    def create_cpu_frequency_harmonics(base_clock_mhz: float, num_harmonics: int = 5) -> List[Harmonic]:
        """Create CPU frequency harmonics.
        
        Modern CPUs have base clock with harmonic relationships:
        Base clock, 2x, 3x, etc for different components.
        """
        harmonics = []
        for n in range(1, num_harmonics + 1):
            harmonic = Harmonic(
                harmonic_type=HarmonicType.FREQUENCY_RESONANCE.value,
                fundamental=base_clock_mhz,
                multiplier=float(n),
                amplitude=1.0 / n,
                properties={"component": f"tier_{n}", "mhz": base_clock_mhz * n}
            )
            harmonics.append(harmonic)
        return harmonics
    
    @staticmethod
    def create_cache_coherency_harmonics(cache_line_size_bytes: int) -> List[Harmonic]:
        """Create harmonics from cache coherency patterns.
        
        Cache lines create harmonic patterns in memory access.
        """
        harmonics = []
        for level in [1, 2, 3]:  # L1, L2, L3 cache levels
            harmonic = Harmonic(
                harmonic_type=HarmonicType.CACHE_RESONANCE.value,
                fundamental=cache_line_size_bytes,
                multiplier=float(level),
                amplitude=1.0 / (level + 1),  # L1 stronger than L2 stronger than L3
                properties={"cache_level": f"L{level}", "size": cache_line_size_bytes * level}
            )
            harmonics.append(harmonic)
        return harmonics


class AgentHarmonics:
    """Harmonics patterns for agent domain."""
    
    @staticmethod
    def create_consensus_harmonics(num_agents: int, agreement_strength: float = 0.8) -> List[Harmonic]:
        """Create harmonics from multi-agent consensus patterns.
        
        When N agents agree, they create harmonic resonance at frequency = 1/N.
        """
        harmonics = []
        
        # Fundamental: all agents in agreement
        harmonic = Harmonic(
            harmonic_type=HarmonicType.CONSENSUS_HARMONIC.value,
            fundamental=1.0,
            multiplier=1.0 / num_agents,
            amplitude=agreement_strength,
            properties={"num_agents": num_agents, "consensus_type": "full"}
        )
        harmonics.append(harmonic)
        
        # Subharmonics: partial agreements (quorum)
        for quorum_size in range(2, num_agents):
            harmonic = Harmonic(
                harmonic_type=HarmonicType.CONSENSUS_HARMONIC.value,
                fundamental=1.0,
                multiplier=1.0 / quorum_size,
                amplitude=agreement_strength * (quorum_size / num_agents),
                properties={"quorum_size": quorum_size, "consensus_type": "partial"}
            )
            harmonics.append(harmonic)
        
        return harmonics


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def interval_name_from_ratio(ratio: float) -> str:
    """Convert frequency ratio to musical interval name."""
    intervals = {
        1.0: "unison",
        1.067: "minor_second",
        1.125: "major_second",
        1.2: "minor_third",
        1.25: "major_third",
        1.333: "perfect_fourth",
        1.414: "tritone",
        1.5: "perfect_fifth",
        1.6: "minor_sixth",
        1.667: "major_sixth",
        1.8: "minor_seventh",
        1.875: "major_seventh",
        2.0: "octave",
    }
    
    # Find closest match
    closest_name = "unknown"
    closest_diff = 1.0
    for ratio_val, name in intervals.items():
        diff = abs(ratio - ratio_val)
        if diff < closest_diff:
            closest_diff = diff
            closest_name = name
    
    return closest_name


def compute_harmonic_blend(harmonics: List[Harmonic], time_point: float = 0.0) -> float:
    """Combine all harmonics into single value (for audio waveform or visual property).
    
    Used to synthesize audio or visual output from harmonic components.
    """
    result = 0.0
    for harmonic in harmonics:
        # Add sine wave component for this harmonic
        phase = 2 * math.pi * harmonic.frequency * time_point + harmonic.phase_offset
        result += harmonic.amplitude * math.sin(phase)
    return result


# ============================================================================
# EXAMPLE: Show harmonic relationships across domains
# ============================================================================

if __name__ == "__main__":
    print("""
HARMONICS FRAMEWORK: Universal resonance patterns
==================================================

Harmonics appear everywhere:

1. AUDIO: A4 (440 Hz)
   └─ Natural overtone series
      └─ 1x: 440Hz (fundamental)
      └─ 2x: 880Hz (octave)
      └─ 3x: 1320Hz (twelfth)
      └─ 4x: 1760Hz (double octave)

2. VISUAL: Benzene (C6H6)
   └─ Resonance structures
      └─ 1st Kekule form (1 contribution)
      └─ 2nd Kekule form (1 contribution)
      └─ 3rd Kekule form (1 contribution)
      └─ Combined: Aromatic delocalization

3. MOLECULAR: Carbon atom
   └─ Electron shell harmonics
      └─ s orbital (1 lobe) = fundamental
      └─ p orbital (2 lobes) = 1:1 resonance
      └─ d orbital (4 lobes) = 1:1:1:1 resonance

4. COMPUTE: 3.0 GHz CPU
   └─ Frequency harmonics
      └─ 1x: 3.0 GHz (base clock)
      └─ 2x: 6.0 GHz (cache level)
      └─ 3x: 9.0 GHz (ALU operations)

5. AGENTS: 5-agent consensus
   └─ Consensus harmonics
      └─ Full agreement (1/5 frequency)
      └─ 4-agent quorum (1/4 frequency)
      └─ 3-agent quorum (1/3 frequency)

ALL follow the same mathematical pattern:
  Fundamental × Multiplier × Amplitude × Phase = Contribution
    """)
    
    # Create examples
    print("\nGenerating harmonic examples...\n")
    
    # Audio: A4 harmonic series
    print("1. Audio: A4 (440 Hz) harmonic series:")
    audio_harmonics = AudioHarmonics.create_harmonic_series(440, 4)
    for h in audio_harmonics:
        print(f"   {h}")
    
    # Visual: Benzene resonance structures
    print("\n2. Visual: Benzene resonance structures:")
    benzene_harmonics = VisualHarmonics.create_resonance_structures("benzene", 2)
    for h in benzene_harmonics:
        print(f"   {h}")
    
    # Molecular: Carbon electron shells
    print("\n3. Molecular: Carbon electron shell harmonics:")
    carbon_harmonics = VisualHarmonics.create_electron_shell_harmonics("C", 4)
    for h in carbon_harmonics:
        print(f"   {h}")
    
    # Bonding: Double bond harmonics
    print("\n4. Bonding: Double bond (C=O) harmonics:")
    double_bond_harmonics = VisualHarmonics.create_bonding_harmonics("double", 2)
    for h in double_bond_harmonics:
        print(f"   {h}")
    
    # Compute: CPU harmonics
    print("\n5. Compute: 3.0 GHz CPU frequency harmonics:")
    cpu_harmonics = ComputeHarmonics.create_cpu_frequency_harmonics(3000, 3)
    for h in cpu_harmonics:
        print(f"   {h}")
    
    # Agents: Consensus
    print("\n6. Agents: 5-agent consensus harmonics:")
    agent_harmonics = AgentHarmonics.create_consensus_harmonics(5, 0.9)
    for h in agent_harmonics:
        print(f"   {h}")
    
    print("\nAll domains share identical harmonic mathematics.")
