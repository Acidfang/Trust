#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARIA — Single entry point for all ledger-driven operations.
RULE 1: Single Purpose Per File — This is THE Python runtime for ARIA.
RULE 5: Only runtime code that serves active functions.
Combines: core system + bootstrap + builder + input interface.
"""

import json
import sys
import time
import math
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from enum import Enum

# ============================================================================
# CORE STATE MACHINE — Cycle-based, ledger-driven
# ============================================================================

class AriaCoreSystem:
    """Deterministic state machine. Every change recorded to ledger."""

    def __init__(self, ledger_file='ledgers.json', spec_file='complete_app_ledger.json'):
        self.ledger_file = ledger_file
        self.spec_file = spec_file
        self.cycle = 0
        self.state = 0
        self.ledger_data = {}
        self.spec = {}

        self.load_files()
        self.init_from_ledger()

    def load_files(self):
        """Load ledger and spec"""
        try:
            with open(self.ledger_file, 'r') as f:
                self.ledger_data = json.load(f)
        except FileNotFoundError:
            self.ledger_data = {"aria": {}}

        try:
            with open(self.spec_file, 'r') as f:
                self.spec = json.load(f)
        except FileNotFoundError:
            self.spec = {}

        if 'aria' not in self.ledger_data:
            self.ledger_data['aria'] = {}

    def save_ledger(self):
        """Save ledger"""
        with open(self.ledger_file, 'w') as f:
            json.dump(self.ledger_data, f, indent=2, ensure_ascii=False)

    def init_from_ledger(self):
        """Restore state from ledger history"""
        core_log = self.ledger_data.get('aria', {}).get('core_log', [])
        if core_log:
            self.cycle = core_log[-1].get('cycle', 0)
            self.state = core_log[-1].get('state', 0)

    def clock_tick(self):
        """Increment cycle"""
        self.cycle += 1

    def encode_signal(self, signal: Optional[str]) -> int:
        """Encode signal to state (0-255)"""
        if signal is None:
            return self.state
        return sum(ord(c) for c in str(signal)) % 256

    def get_memory(self) -> Dict[Tuple[int, int], int]:
        """Get learned transitions from ledger"""
        memory_str = self.ledger_data.get('aria', {}).get('memory', {})
        memory = {}
        for key_str, count in memory_str.items():
            try:
                key = tuple(map(int, key_str.strip('()').split(', ')))
                memory[key] = count
            except:
                pass
        return memory

    def resolve_state_from_memory(self, base_state: int) -> int:
        """Use learned transitions or fall back to base state"""
        memory = self.get_memory()
        possible_next = {}
        for (prev, next_state), count in memory.items():
            if prev == self.state:
                possible_next[next_state] = count

        if possible_next:
            return max(possible_next.items(), key=lambda x: x[1])[0]
        return base_state

    def resolve_state(self, signal: Optional[str]) -> int:
        """Resolve state: encode signal, check memory, return most likely next state"""
        base_state = self.encode_signal(signal)
        return self.resolve_state_from_memory(base_state)

    def compute_delta(self, prev: int, current: int) -> int:
        """Delta = XOR"""
        return prev ^ current

    def learn_transition(self, prev: int, current: int):
        """Record transition to ledger memory"""
        memory = self.get_memory()
        key = (prev, current)
        memory[key] = memory.get(key, 0) + 1
        memory_str = {str(k): v for k, v in memory.items()}
        self.ledger_data['aria']['memory'] = memory_str

    def commit(self, signal: Optional[str] = None) -> Dict:
        """Core loop: tick, resolve, compute delta, record, learn"""
        self.clock_tick()
        new_state = self.resolve_state(signal)
        delta = self.compute_delta(self.state, new_state)

        entry = {
            "cycle": self.cycle,
            "timestamp": int(time.time()),
            "prev": self.state,
            "state": new_state,
            "delta": delta,
            "signal": signal
        }

        if 'core_log' not in self.ledger_data['aria']:
            self.ledger_data['aria']['core_log'] = []

        self.ledger_data['aria']['core_log'].append(entry)
        self.learn_transition(self.state, new_state)

        self.state = new_state
        self.save_ledger()

        return entry

    def format_output(self, entry: Dict) -> str:
        """Minimal output format"""
        coherence = self.ledger_data.get('aria', {}).get('tau', 0.95)
        entropy = bin(entry['delta']).count('1')
        return f"C:{entry['cycle']} | S:{entry['state']:03d} | D:{bin(entry['delta'])[2:].zfill(8)} | E:{entropy} | Co:{coherence:.2f}"

# ============================================================================
# BUILDER — Builds phases from spec
# ============================================================================

class AriaBuildSystem:
    """Elects and builds phases deterministically"""

    def __init__(self, spec: dict, ledger_data: dict):
        self.spec = spec
        self.ledger_data = ledger_data

    def get_pending_phases(self) -> list:
        """Get pending phases from spec"""
        phases = []
        galaxy_phases = self.spec.get('visualization_spec', {}).get('galaxy_phases', {})
        for phase_key, phase_data in galaxy_phases.items():
            if phase_data.get('enabled') is False and phase_data.get('status') == 'pending':
                phases.append({
                    'key': phase_key,
                    'name': phase_data.get('what_to_build', 'unknown'),
                    'particles': phase_data.get('parameters', {}).get('particle_count', 0),
                })
        return phases

    def generate_phase_3_disk(self, params: dict) -> list:
        """Generate Phase 3 disk particles with exponential falloff"""
        particles = []
        count = params.get('particle_count', 3000)
        inner_radius = params.get('inner_radius', 30)
        outer_radius = params.get('outer_radius', 300)
        thickness = params.get('disk_half_thickness', 5)

        for i in range(count):
            # Exponential falloff density
            u = (i + 1) / count  # Progressive 0 to 1
            r = inner_radius + (outer_radius - inner_radius) * (1 - math.exp(-u * 3)) / (1 - math.exp(-3))
            theta = (i * 2.4) % (2 * math.pi)  # Deterministic angle based on index
            z = ((i % 100) - 50) * thickness / 50  # Deterministic z distribution

            particles.append({
                'x': round(r * math.cos(theta), 2),
                'y': round(r * math.sin(theta), 2),
                'z': round(z, 2),
                'index': i
            })

        return particles

    def generate_phase_4_presence_field(self, params: dict) -> list:
        """
        Generate Phase 4 Presence Field: Multi-axis spherical spiral expansion.
        'Every axis' means we expand in (r, theta, phi) to create the presence field in full effect.
        Formula: r = a * e^(b * theta) mapped to spherical coordinates.
        """
        particles = []
        major_arms = params.get('major_arms', 4)
        minor_arms = params.get('minor_arms', 3)
        total_arms = major_arms + minor_arms
        
        a = params.get('a', 20)
        b = params.get('b', 0.3)
        
        major_arm_particles = params.get('major_arm_particles', 800)
        minor_arm_particles = params.get('minor_arm_particles', 400)
        
        # We distribute particles across the spiral arms, but on EVERY axis (spherical)
        for arm in range(total_arms):
            is_major = arm < major_arms
            arm_count = major_arm_particles if is_major else minor_arm_particles
            arm_offset = (arm * 2 * math.pi) / total_arms
            
            for i in range(arm_count):
                u = i / arm_count
                theta = u * 2 * math.pi * 2 # 2 full rotations
                r = a * math.exp(b * theta)
                
                # Multi-axis expansion: instead of just x,y, we use spherical angles
                # This creates 'the presence field in full effect' by occupying the volume
                # phi is the polar angle (0 to pi), theta is the azimuthal (0 to 2pi)
                # To simulate the 'field spiral', we introduce a slight pitch (phi) 
                # that also follows a harmonic or spiral path
                phi = (math.pi / 2) + (math.sin(theta * 0.5) * 0.2) # Slight oscillation around equator
                
                # Jitter for field density
                jitter = (i % 7 - 3) * 2
                r_j = r + jitter
                
                x = round(r_j * math.sin(phi) * math.cos(theta + arm_offset), 2)
                y = round(r_j * math.sin(phi) * math.sin(theta + arm_offset), 2)
                z = round(r_j * math.cos(phi), 2)
                
                particles.append({
                    'x': x, 'y': y, 'z': z,
                    'arm': arm,
                    'is_major': is_major,
                    'type': 'presence_field_node'
                })
        return particles

    def elect_and_build(self) -> bool:
        """Elect next phase and build it"""
        pending = self.get_pending_phases()
        if not pending:
            return False

        phase_key = pending[0]['key']
        galaxy_phases = self.spec.get('visualization_spec', {}).get('galaxy_phases', {})
        phase_data = galaxy_phases.get(phase_key, {})

        # Build
        params = phase_data.get('parameters', {})
        particle_count = params.get('particle_count', 0)

        # Generate particles for Phase 3
        particles = None
        if phase_key == 'phase_3_disk':
            particles = self.generate_phase_3_disk(params)

        # Record to ledger
        if 'build_log' not in self.ledger_data['aria']:
            self.ledger_data['aria']['build_log'] = []

        build_entry = {
            'phase': phase_key,
            'what': phase_data.get('what_to_build'),
            'particles': particle_count,
            'status': 'COMPLETE'
        }
        self.ledger_data['aria']['build_log'].append(build_entry)

        # Mark complete in spec
        galaxy_phases[phase_key]['enabled'] = True
        galaxy_phases[phase_key]['status'] = 'complete'

        # Save phases to ledger
        if 'phases' not in self.ledger_data['aria']:
            self.ledger_data['aria']['phases'] = {}

        phase_record = {
            'status': 'complete',
            'particle_count': particle_count
        }

        # Store actual particle data if generated
        if particles:
            phase_record['particles'] = particles

        self.ledger_data['aria']['phases'][phase_key] = phase_record

        return True

# ============================================================================
# INTERACTIVE LOOP
# ============================================================================

def main():
    """Single entry point: run ARIA"""
    system = AriaCoreSystem()
    builder = AriaBuildSystem(system.spec, system.ledger_data)

    print("ARIA — Ledger-driven state machine")
    print("Type 'status', 'build', or 'quit'.\n")

    # Auto-bootstrap on first run
    if not system.ledger_data.get('aria', {}).get('core_log'):
        system.commit("SYSTEM_START")

    while True:
        try:
            user_input = input().strip()
        except (KeyboardInterrupt, EOFError):
            system.commit("SHUTDOWN")
            break

        if user_input.lower() in ['quit', 'exit']:
            system.commit("SHUTDOWN")
            break

        if user_input.lower() == 'status':
            core_log = system.ledger_data.get('aria', {}).get('core_log', [])
            if core_log:
                last = core_log[-1]
                print(system.format_output(last))
            continue

        if user_input.lower() == 'build':
            if builder.elect_and_build():
                system.save_ledger()
                pending = builder.get_pending_phases()
                if pending:
                    print(f"BUILT: {pending[0]['name']}")
                    print(f"NEXT PENDING: {len(pending)-1} phases")
            else:
                print("All phases complete!")
            continue

        if user_input == "":
            continue

        # Process input
        entry = system.commit(user_input)
        print(system.format_output(entry))

if __name__ == '__main__':
    main()
