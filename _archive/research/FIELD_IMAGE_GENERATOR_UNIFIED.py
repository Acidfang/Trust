#!/usr/bin/env python3
"""
FIELD IMAGE GENERATOR — UNIFIED VERSION

Core principle: Different scales require different visualization approaches

INVISIBLE SCALES (Electron, Atom):
  Show the FIELD ITSELF - mathematical expressions, field behavior, probability clouds
  What you see: equations, field lines, potential landscapes, orbital visualizations
  
VISIBLE SCALES (Water Molecule, Cell, etc.):
  Show the VISUAL MANIFESTATION - how the field appears when we can observe it
  What you see: molecular structure, cellular organization, actual observable patterns

UNIFICATION: Consolidates all versions (V-V6) into single unified implementation.
This is the only field image generator needed for entire project.
"""

import math
from pathlib import Path
from typing import Dict, Tuple, List


class FieldExpressionVisualizer:
    """Visualize FIELD EXPRESSIONS and BEHAVIOR for invisible scales."""
    
    # MEASURED CONSTANTS
    BOHR_RADIUS = 0.529  # Ångströms
    RYDBERG_ENERGY = 13.6  # eV
    FINE_STRUCTURE = 1/137.036  # alpha
    
    def __init__(self):
        pass
    
    def generate_electron_field_expression(self) -> str:
        """
        Show the ELECTRON as a FIELD, not a particle.
        
        Express the electron field mathematically and visually.
        The electron is an excitation of the omnipresent electron field φ_e(x,t)
        """
        svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="1200" viewBox="0 0 1000 1200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="fieldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#001a4d;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#003d7a;stop-opacity:1" />
        </linearGradient>
        <radialGradient id="probabilityCloud" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#ff00ff;stop-opacity:0.8" />
            <stop offset="70%" style="stop-color:#ff00ff;stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:#ff00ff;stop-opacity:0" />
        </radialGradient>
    </defs>
    
    <rect width="1000" height="1200" fill="url(#fieldGradient)"/>
    
    <!-- TITLE -->
    <text x="500" y="40" text-anchor="middle" fill="#00ff88" font-size="24" font-weight="bold" font-family="monospace">
        ELECTRON FIELD EXPRESSION
    </text>
    
    <!-- FIELD EQUATION 1: Dirac Equation -->
    <g id="dirac-section">
        <text x="50" y="100" fill="#ffff00" font-size="14" font-weight="bold" font-family="monospace">
            1. DIRAC EQUATION (Relativistic Field):
        </text>
        <text x="70" y="130" fill="#00ff88" font-size="12" font-family="monospace">
            (iγ·∂ - m)ψ(x,t) = 0
        </text>
        <text x="70" y="160" fill="#00ff88" font-size="11" font-family="monospace">
            ψ(x,t) = electron field amplitude at position x, time t
        </text>
        <text x="70" y="185" fill="#00ff88" font-size="11" font-family="monospace">
            γ = Dirac matrices | m = electron rest mass (9.109×10⁻³¹ kg)
        </text>
        <text x="70" y="210" fill="#00ff88" font-size="11" font-family="monospace">
            Spin: ½ (clockwise or counterclockwise) = TWO states
        </text>
    </g>
    
    <!-- FIELD PROBABILITY CLOUD VISUALIZATION -->
    <g id="probability-cloud">
        <text x="50" y="270" fill="#ffff00" font-size="14" font-weight="bold" font-family="monospace">
            2. PROBABILITY CLOUD IN 1s ORBITAL:
        </text>
        
        <!-- Nucleus at center -->
        <circle cx="500" cy="450" r="5" fill="#ff0000" opacity="0.8"/>
        <text x="510" y="455" fill="#ff0000" font-size="11" font-family="monospace">nucleus</text>
        
        <!-- Probability density cloud -->
        <circle cx="500" cy="450" r="80" fill="url(#probabilityCloud)" opacity="0.9"/>
        <circle cx="500" cy="450" r="120" stroke="#ff00ff" stroke-width="1" fill="none" stroke-dasharray="5,5" opacity="0.5"/>
        <circle cx="500" cy="450" r="160" stroke="#ff00ff" stroke-width="1" fill="none" stroke-dasharray="5,5" opacity="0.3"/>
        
        <!-- Bohr radius reference -->
        <line x1="500" y1="450" x2="580" y2="450" stroke="#00ff00" stroke-width="2"/>
        <text x="590" y="455" fill="#00ff00" font-size="11" font-family="monospace">
            a₀ = 0.529 Å (Bohr radius)
        </text>
        
        <!-- Field strength annotation -->
        <text x="420" y="450" fill="#ff00ff" font-size="10" font-family="monospace">|ψ|² = high</text>
        <text x="350" y="480" fill="#ff00ff" font-size="10" font-family="monospace">|ψ|² = medium</text>
        <text x="300" y="560" fill="#ff00ff" font-size="10" font-family="monospace">|ψ|² = low</text>
    </g>
    
    <!-- ENERGY LEVELS -->
    <g id="energy-levels">
        <text x="50" y="700" fill="#ffff00" font-size="14" font-weight="bold" font-family="monospace">
            3. ENERGY LEVELS (from Rydberg Formula):
        </text>
        <text x="70" y="730" fill="#00ff88" font-size="12" font-family="monospace">
            E_n = -13.6 eV / n²
        </text>
        
        <!-- Ground state -->
        <line x1="100" y1="780" x2="300" y2="780" stroke="#ff00ff" stroke-width="3"/>
        <text x="310" y="785" fill="#ff00ff" font-size="11" font-family="monospace">
            n=1: E₁ = -13.6 eV (ground state)
        </text>
        
        <!-- First excited -->
        <line x1="100" y1="730" x2="300" y2="730" stroke="#ff0088" stroke-width="2" stroke-dasharray="5,5"/>
        <text x="310" y="735" fill="#ff0088" font-size="11" font-family="monospace">
            n=2: E₂ = -3.4 eV (first excited)
        </text>
        
        <!-- Second excited -->
        <line x1="100" y1="710" x2="300" y2="710" stroke="#ff0044" stroke-width="2" stroke-dasharray="5,5"/>
        <text x="310" y="715" fill="#ff0044" font-size="11" font-family="monospace">
            n=3: E₃ = -1.51 eV
        </text>
        
        <!-- Continuum -->
        <line x1="100" y1="680" x2="300" y2="680" stroke="#ff0000" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="310" y="685" fill="#ff0000" font-size="11" font-family="monospace">
            E > 0: Free electron (ionized)
        </text>
    </g>
    
    <!-- QUANTUM SUPERPOSITION -->
    <g id="superposition">
        <text x="50" y="850" fill="#ffff00" font-size="14" font-weight="bold" font-family="monospace">
            4. QUANTUM SUPERPOSITION (What makes electron "real"):
        </text>
        <text x="70" y="880" fill="#00ff88" font-size="11" font-family="monospace">
            ψ_measured = α·ψ(spin up) + β·ψ(spin down)
        </text>
        <text x="70" y="910" fill="#00ff88" font-size="11" font-family="monospace">
            Position: UNDEFINED until measurement (in superposition everywhere)
        </text>
        <text x="70" y="940" fill="#00ff88" font-size="11" font-family="monospace">
            Measurement: Collapses wave function → reveals specific state
        </text>
        <text x="70" y="970" fill="#ff00ff" font-size="11" font-family="monospace">
            The electron IS the field. We see probability, not position.
        </text>
    </g>
    
    <!-- VIRTUAL PARTICLES -->
    <g id="virtual">
        <text x="50" y="1040" fill="#ffff00" font-size="14" font-weight="bold" font-family="monospace">
            5. VIRTUAL PARTICLE EXCHANGES (Field Self-Interaction):
        </text>
        <text x="70" y="1070" fill="#00ff88" font-size="11" font-family="monospace">
            Electron constantly exchanges virtual photons with itself
        </text>
        <text x="70" y="1100" fill="#00ff88" font-size="11" font-family="monospace">
            This self-energy correction: Δm = α·m/(2π) ≈ 0.1% of electron mass
        </text>
        <text x="70" y="1130" fill="#00ff88" font-size="11" font-family="monospace">
            MEASURED with 12 decimal place accuracy (fine structure constant)
        </text>
    </g>
    
    <text x="500" y="1180" text-anchor="middle" fill="#00ff00" font-size="10" font-family="monospace">
        This is NOT a particle. This is a FIELD EXCITATION expressed mathematically.
    </text>
</svg>'''
        return svg
    
    def generate_atom_field_expression(self, element: str, z: int) -> str:
        """
        Show the ATOM FIELD - electron orbitals, field potentials, shell structure.
        
        Express how electron fields organize around a nucleus.
        """
        
        # Build electron configuration
        config = self.generate_electron_configuration(z)
        config_str = ""
        electrons = 0
        for shell, count, orbital in config:
            config_str += f"{orbital}^{count} "
            electrons += count
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="1200" viewBox="0 0 1000 1200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="nuclearField" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#ffff00;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#ff8800;stop-opacity:0.3" />
        </radialGradient>
    </defs>
    
    <rect width="1000" height="1200" fill="#001a00"/>
    
    <!-- TITLE -->
    <text x="500" y="40" text-anchor="middle" fill="#00ff88" font-size="24" font-weight="bold" font-family="monospace">
        {element.upper()} (Z={z}) — ATOMIC FIELD STRUCTURE
    </text>
    
    <!-- ELECTRON CONFIGURATION -->
    <g id="config">
        <text x="50" y="90" fill="#ffff00" font-size="13" font-weight="bold" font-family="monospace">
            Electron Configuration:
        </text>
        <text x="70" y="120" fill="#00ff88" font-size="12" font-family="monospace">
            {config_str}
        </text>
    </g>
    
    <!-- NUCLEAR POTENTIAL AT CENTER -->
    <g id="nucleus">
        <text x="50" y="180" fill="#ffff00" font-size="13" font-weight="bold" font-family="monospace">
            1. NUCLEAR COULOMB POTENTIAL:
        </text>
        <text x="70" y="210" fill="#00ff88" font-size="11" font-family="monospace">
            V(r) = -Z·e²/(4πε₀r) = -Z·13.6 eV / (r/a₀)
        </text>
        <text x="70" y="240" fill="#00ff88" font-size="11" font-family="monospace">
            Z = {z} (nuclear charge)
        </text>
        
        <!-- Visual nucleus -->
        <circle cx="500" cy="450" r="8" fill="url(#nuclearField)"/>
        <text x="515" y="455" fill="#ffff00" font-size="11" font-family="monospace">nucleus (Z={z})</text>
    </g>
    
    <!-- ORBITAL SHELLS -->
    <g id="orbitals">
        <text x="50" y="310" fill="#ffff00" font-size="13" font-weight="bold" font-family="monospace">
            2. ELECTRON ORBITAL CLOUDS (Probability Density |ψ|²):
        </text>
        
        <!-- 1s orbital -->
        <circle cx="500" cy="450" r="60" fill="none" stroke="#ff00ff" stroke-width="2" opacity="0.8"/>
        <circle cx="500" cy="450" r="90" fill="none" stroke="#ff00ff" stroke-width="1" opacity="0.3" stroke-dasharray="5,5"/>
        <text x="610" y="450" fill="#ff00ff" font-size="11" font-family="monospace">1s orbital</text>
        
        <!-- If there are more shells -->
        '''
        
        if z > 2:
            # 2s/2p shell
            svg += f'''        <circle cx="500" cy="450" r="140" fill="none" stroke="#00ff88" stroke-width="2" opacity="0.6"/>
        <circle cx="500" cy="450" r="180" fill="none" stroke="#00ff88" stroke-width="1" opacity="0.2" stroke-dasharray="5,5"/>
        <text x="650" y="450" fill="#00ff88" font-size="11" font-family="monospace">n=2 shell (2s, 2p)</text>
        '''
        
        if z > 10:
            # 3s/3p/3d shell
            svg += f'''        <circle cx="500" cy="450" r="280" fill="none" stroke="#0088ff" stroke-width="2" opacity="0.4"/>
        <text x="790" y="450" fill="#0088ff" font-size="11" font-family="monospace">n=3</text>
        '''
        
        svg += '''    </g>
    
    <!-- FIELD STRENGTH PATTERN -->
    <g id="field-strength">
        <text x="50" y="600" fill="#ffff00" font-size="13" font-weight="bold" font-family="monospace">
            3. FIELD STRENGTH BY DISTANCE (Measured from Spectroscopy):
        </text>
        
        <!-- Field strength graph -->
        <line x1="100" y1="750" x2="800" y2="750" stroke="#666666" stroke-width="1"/>
        <line x1="100" y1="650" x2="100" y2="750" stroke="#666666" stroke-width="1"/>
        
        <text x="90" y="770" text-anchor="end" fill="#888888" font-size="9">0</text>
        <text x="90" y="660" text-anchor="end" fill="#888888" font-size="9">max</text>
        <text x="810" y="770" fill="#888888" font-size="9">r</text>
        
        <!-- 1s field strength curve -->
        <path d="M 100 720 Q 200 670 300 700 Q 400 730 500 745 Q 600 750 800 750" 
              stroke="#ff00ff" stroke-width="2" fill="none"/>
        <text x="150" y="740" fill="#ff00ff" font-size="10" font-family="monospace">1s density</text>
    </g>
    
    <!-- EFFECTIVE NUCLEAR CHARGE -->
    <g id="zeff">
        <text x="50" y="830" fill="#ffff00" font-size="13" font-weight="bold" font-family="monospace">
            4. SHIELDING EFFECT (Effective Nuclear Charge Z_eff):
        </text>
        <text x="70" y="860" fill="#00ff88" font-size="11" font-family="monospace">
            Inner electrons shield outer electrons from full nuclear charge
        </text>
        <text x="70" y="890" fill="#00ff88" font-size="11" font-family="monospace">
            Z_eff (valence) = Z - (inner electrons) ≈ smaller attraction
        </text>
        <text x="70" y="920" fill="#00ff88" font-size="11" font-family="monospace">
            Result: Outer electrons in larger orbitals despite high Z
        </text>
    </g>
    
    <!-- IONIZATION ENERGIES -->
    <g id="ionization">
        <text x="50" y="990" fill="#ffff00" font-size="13" font-weight="bold" font-family="monospace">
            5. IONIZATION ENERGIES (Energy to Remove Each Electron):
        </text>
        '''
        
        # Calculate and show ionization energies for each shell
        svg += f'''        <text x="70" y="1020" fill="#00ff88" font-size="10" font-family="monospace">
            1st ionization: {self.calculate_ionization_energy(z, 1):.1f} eV (outermost)
        </text>
        '''
        
        svg += '''    </g>
    
    <text x="500" y="1170" text-anchor="middle" fill="#00ff00" font-size="10" font-family="monospace">
        The atom is FIELDS AROUND NUCLEUS. We see probability clouds, not solid structure.
    </text>
</svg>'''
        return svg
    
    def generate_electron_configuration(self, z: int) -> List[Tuple[int, int, str]]:
        """Generate electron configuration for element with atomic number z."""
        order = [
            (1, 1, '1s'), (1, 2, '2s'), (1, 6, '2p'),
            (2, 2, '3s'), (2, 6, '3p'), (2, 10, '3d'),
            (3, 2, '4s'), (3, 6, '4p'), (3, 10, '4d'), (3, 14, '4f'),
        ]
        
        config = []
        electrons_placed = 0
        
        for shell, max_electrons, orbital in order:
            if electrons_placed >= z:
                break
            electrons_to_place = min(max_electrons, z - electrons_placed)
            config.append((shell, electrons_to_place, orbital))
            electrons_placed += electrons_to_place
        
        return config
    
    def calculate_ionization_energy(self, z: int, n: int = 1) -> float:
        """Calculate ionization energy using Rydberg formula."""
        RYDBERG_ENERGY = 13.6
        return RYDBERG_ENERGY * (z * z) / (n * n)


class VisualFieldRepresentation:
    """Visualize ACTUAL FIELDS as they appear for visible scales."""
    
    def generate_water_molecule_field_visual(self) -> str:
        """Show water molecule as we actually see it - electron clouds + nuclear positions."""
        svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="800" viewBox="0 0 1000 800" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="nucleusGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#ffff00;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#ff8800;stop-opacity:0" />
        </radialGradient>
        <radialGradient id="electronCloud" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#00ff88;stop-opacity:0.7" />
            <stop offset="100%" style="stop-color:#00ff88;stop-opacity:0" />
        </radialGradient>
    </defs>
    
    <rect width="1000" height="800" fill="#001a1a"/>
    
    <text x="500" y="50" text-anchor="middle" fill="#00ff88" font-size="24" font-weight="bold" font-family="monospace">
        WATER MOLECULE (H₂O) — AS OBSERVED
    </text>
    
    <!-- O nucleus -->
    <circle cx="500" cy="400" r="4" fill="url(#nucleusGrad)"/>
    <text x="510" y="405" fill="#ffff00" font-size="11" font-family="monospace">O (Z=8)</text>
    
    <!-- O electron cloud -->
    <circle cx="500" cy="400" r="70" fill="url(#electronCloud)" opacity="0.6"/>
    
    <!-- H1 nucleus -->
    <circle cx="420" cy="300" r="3" fill="#ffff00"/>
    <text x="425" y="305" fill="#ffff00" font-size="11" font-family="monospace">H</text>
    
    <!-- H1 electron cloud -->
    <circle cx="420" cy="300" r="30" fill="#00ff88" opacity="0.4"/>
    
    <!-- H2 nucleus -->
    <circle cx="580" cy="300" r="3" fill="#ffff00"/>
    <text x="585" y="305" fill="#ffff00" font-size="11" font-family="monospace">H</text>
    
    <!-- H2 electron cloud -->
    <circle cx="580" cy="300" r="30" fill="#00ff88" opacity="0.4"/>
    
    <!-- O-H bonds (lines show field overlap) -->
    <line x1="500" y1="400" x2="420" y2="300" stroke="#00ff88" stroke-width="2" opacity="0.8"/>
    <line x1="500" y1="400" x2="580" y2="300" stroke="#00ff88" stroke-width="2" opacity="0.8"/>
    
    <!-- Bond angle annotation -->
    <path d="M 450 340 Q 480 370 520 365" stroke="#ff0088" stroke-width="1" fill="none" stroke-dasharray="3,3"/>
    <text x="480" y="390" fill="#ff0088" font-size="11" font-family="monospace">104.5°</text>
    
    <text x="500" y="700" text-anchor="middle" fill="#00ff00" font-size="12" font-family="monospace">
        VSEPR geometry: Bent shape due to electron pair repulsion
    </text>
    <text x="500" y="730" text-anchor="middle" fill="#00ff00" font-size="11" font-family="monospace">
        Electron clouds (blue) show field density. Bonds form where fields overlap.
    </text>
</svg>'''
        return svg
