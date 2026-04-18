"""
ELECTRON EVOLUTIONARY TREE GENERATOR
Visualize how electrons fill orbitals across the periodic table
Shows genealogy of orbital occupation (aufbau principle)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import matplotlib.animation as animation
from collections import OrderedDict

class ElectronTreeGenerator:
    """Generate electron orbital evolution trees"""
    
    def __init__(self):
        """Initialize with periodic table electron configurations"""
        # Electron configuration in aufbau order (how orbitals fill)
        self.orbital_order = [
            '1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', 
            '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p'
        ]
        
        # Element configurations (simplified - electrons in highest filled orbitals)
        self.elements = self._generate_elements()
        
        # Color map for orbital types
        self.orbital_colors = {
            's': '#FF6B6B',  # Red
            'p': '#4ECDC4',  # Teal
            'd': '#45B7D1',  # Blue
            'f': '#FFA07A'   # Light Salmon
        }
    
    def _generate_elements(self):
        """Generate electron configurations for periodic table"""
        configs = {}
        electron_count = 0
        
        for element_num in range(1, 119):  # Elements 1-118
            element_name = self._get_element_name(element_num)
            config = self._get_electron_config(element_num)
            configs[element_name] = {
                'z': element_num,
                'config': config,
                'electrons': element_num
            }
        
        return configs
    
    def _get_element_name(self, z):
        """Get element name from atomic number"""
        elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                   'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
                   'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                   'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
                   'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
                   'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
                   'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
                   'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
                   'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
                   'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
                   'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
                   'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        return elements[z-1] if z <= len(elements) else f"E{z}"
    
    def _get_electron_config(self, z):
        """Generate electron configuration for element"""
        # Simplified aufbau configuration
        config = {}
        orbitals = [
            ('1s', 2), ('2s', 2), ('2p', 6), ('3s', 2), ('3p', 6), 
            ('4s', 2), ('3d', 10), ('4p', 6), ('5s', 2), ('4d', 10),
            ('5p', 6), ('6s', 2), ('4f', 14), ('5d', 10), ('6p', 6),
            ('7s', 2), ('5f', 14), ('6d', 10), ('7p', 6)
        ]
        
        electrons_remaining = z
        for orbital, max_electrons in orbitals:
            if electrons_remaining <= 0:
                break
            electrons_in_orbital = min(electrons_remaining, max_electrons)
            config[orbital] = electrons_in_orbital
            electrons_remaining -= electrons_in_orbital
        
        return config
    
    def generate_orbital_tree_static(self, filename='electron_tree_static.png'):
        """
        Generate static orbital tree showing aufbau order
        
        Visualization: Tree showing how each orbital fills
        """
        fig, ax = plt.subplots(figsize=(16, 10), dpi=150)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        # Draw orbital filling tree
        # Each orbital is a node, arrows show filling order
        
        y_positions = {}
        x_positions = {}
        
        # Position orbitals in energy levels
        orbital_groups = {
            '1s': (1, 0),      # n=1
            '2s': (2, 0),      # n=2
            '2p': (2, 1),
            '3s': (3, 0),      # n=3
            '3p': (3, 1),
            '4s': (4, 0),      # n=4
            '3d': (3, 2),
            '4p': (4, 1),
            '5s': (5, 0),      # n=5
            '4d': (4, 2),
            '5p': (5, 1),
            '6s': (6, 0),      # n=6
            '4f': (4, 3),
            '5d': (5, 2),
            '6p': (6, 1),
            '7s': (7, 0),      # n=7
            '5f': (5, 3),
            '6d': (6, 2),
            '7p': (7, 1),
        }
        
        # Draw nodes
        node_size = 800
        for i, orbital in enumerate(self.orbital_order):
            if orbital in orbital_groups:
                n, subshell_idx = orbital_groups[orbital]
                
                # Spread orbitals horizontally by subshell type
                x = n * 2 + subshell_idx * 0.6
                y = 10 - i * 0.5  # Energy increases down
                
                x_positions[orbital] = x
                y_positions[orbital] = y
                
                # Get orbital type color
                orbital_type = orbital[-1]
                color = self.orbital_colors.get(orbital_type, '#888888')
                
                # Draw orbital node
                circle = Circle((x, y), 0.25, color=color, ec='white', 
                              linewidth=2, zorder=3)
                ax.add_patch(circle)
                
                # Add label
                max_electrons = {'s': 2, 'p': 6, 'd': 10, 'f': 14}[orbital_type]
                ax.text(x, y-0.5, f'{orbital}\n(0-{max_electrons}e⁻)', 
                       ha='center', va='top', fontsize=8, color='white',
                       weight='bold')
        
        # Draw filling order arrows (aufbau principle)
        for i in range(len(self.orbital_order) - 1):
            curr_orbital = self.orbital_order[i]
            next_orbital = self.orbital_order[i + 1]
            
            if curr_orbital in x_positions and next_orbital in x_positions:
                x1, y1 = x_positions[curr_orbital], y_positions[curr_orbital]
                x2, y2 = x_positions[next_orbital], y_positions[next_orbital]
                
                # Draw arrow showing filling order
                arrow = FancyArrowPatch((x1, y1-0.3), (x2, y2+0.3),
                                      connectionstyle='arc3,rad=0.3',
                                      arrowstyle='->', mutation_scale=20,
                                      color='#888888', alpha=0.5, linewidth=1,
                                      zorder=1)
                ax.add_patch(arrow)
        
        # Configure axes
        ax.set_xlim(-1, 15)
        ax.set_ylim(-8, 11)
        ax.axis('off')
        
        # Add title and legend
        ax.text(7.5, 10.5, 'ELECTRON ORBITAL GENEALOGY', 
               ha='center', fontsize=14, color='white', weight='bold')
        ax.text(7.5, 10, 'Aufbau Principle: How Electrons Fill Orbitals', 
               ha='center', fontsize=10, color='#888888', style='italic')
        
        # Legend for orbital types
        legend_y = -6.5
        for orbital_type, color in self.orbital_colors.items():
            circle = Circle((1, legend_y), 0.15, color=color, ec='white', linewidth=1)
            ax.add_patch(circle)
            ax.text(1.5, legend_y, f'{orbital_type}-orbital', va='center', 
                   fontsize=9, color='white')
            legend_y -= 0.7
        
        plt.tight_layout(pad=3.0, w_pad=0.8, h_pad=1.2)
        plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        print(f"✓ Saved {filename}")
    
    def generate_element_genealogy_tree(self, filename='electron_element_tree.png'):
        """
        Generate tree showing how electron configurations evolve
        across periodic table elements
        """
        fig, ax = plt.subplots(figsize=(18, 12), dpi=150)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        # Show first 36 elements (to Kr) with their orbital evolution
        elements_to_show = 36
        
        # Arrange elements in rows by period
        periods = {
            1: list(range(1, 3)),         # H, He
            2: list(range(3, 11)),        # Li-Ne
            3: list(range(11, 19)),       # Na-Ar
            4: list(range(19, 37))        # K-Kr (partial)
        }
        
        y_offset = 0
        for period, element_numbers in periods.items():
            x_offset = 0
            
            for z in element_numbers:
                element_name = self._get_element_name(z)
                config = self._get_electron_config(z)
                
                # Draw element box
                box = FancyBboxPatch((x_offset, y_offset), 1.2, 1.2,
                                    boxstyle="round,pad=0.05", 
                                    edgecolor='white', linewidth=1.5,
                                    facecolor='#1a3a52', alpha=0.7,
                                    zorder=2)
                ax.add_patch(box)
                
                # Element symbol
                ax.text(x_offset + 0.6, y_offset + 0.85, element_name,
                       ha='center', va='center', fontsize=9, color='white',
                       weight='bold')
                
                # Electron configuration abbreviated
                last_orbital = list(config.keys())[-1] if config else '?'
                electrons = z
                ax.text(x_offset + 0.6, y_offset + 0.45, f'[...] {last_orbital}',
                       ha='center', va='center', fontsize=7, color='#888888')
                
                # Atomic number
                ax.text(x_offset + 0.1, y_offset + 1.0, str(z),
                       ha='left', va='top', fontsize=6, color='#666666')
                
                x_offset += 1.4
            
            y_offset -= 2.0
        
        # Add title
        ax.text(18, 14, 'ELEMENT GENEALOGY: Electron Configurations (H → Kr)',
               ha='right', fontsize=12, color='white', weight='bold')
        
        # Configure axes
        ax.set_xlim(-1, 19)
        ax.set_ylim(-8, 15)
        ax.axis('off')
        
        plt.tight_layout(pad=3.0, w_pad=0.8, h_pad=1.2)
        plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        print(f"✓ Saved {filename}")
    
    def generate_electron_growth_animation(self, filename='electron_growth_animation.gif'):
        """
        Animated electron tree: Show electrons adding one-by-one
        through the periodic table, revealing orbital structure
        """
        fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        max_z = 37  # Show through Tc (element 37)
        center_x, center_y = 7, 5
        
        def draw_frame(z):
            """Draw a single frame for element z"""
            ax.clear()
            ax.set_facecolor('#0a0e27')
            
            element_name = self._get_element_name(z)
            config = self._get_electron_config(z)
            
            # Draw shells as concentric circles
            max_shell = max([int(o[0]) for o in config.keys()])
            for shell in range(1, max_shell + 1):
                shell_circle = plt.Circle((center_x, center_y), shell * 1.5,
                                        fill=False, edgecolor='#333333',
                                        linewidth=0.5, linestyle='--', alpha=0.15)
                ax.add_patch(shell_circle)
            
            # Draw electrons - grouped by orbital for clarity
            electron_count = 0
            
            for orbital, electrons_in_orbital in config.items():
                orbital_type = orbital[-1]
                shell_num = int(orbital[0])
                color = self.orbital_colors.get(orbital_type, '#888888')
                
                # Define CORRECT quadrant positions based on matplotlib coordinates
                # matplotlib: RIGHT=0°, TOP=90°, LEFT=180°, BOTTOM=270°
                orbital_quadrants = {
                    's': (np.pi/2, 0.4),     # TOP (90°) - FIXED
                    'p': (0, 0.4),           # RIGHT (0°) - correct
                    'd': (3*np.pi/2, 0.4),   # BOTTOM (270°) - FIXED
                    'f': (np.pi, 0.4)        # LEFT (180°) - correct
                }
                
                if orbital_type in orbital_quadrants:
                    quadrant_angle, quadrant_width = orbital_quadrants[orbital_type]
                else:
                    quadrant_angle, quadrant_width = (0, 0.4)
                
                max_per_orbital = {'s': 2, 'p': 6, 'd': 10, 'f': 14}.get(orbital_type, 2)
                
                # Spread electrons within their quadrant
                for e in range(electrons_in_orbital):
                    angle_in_quadrant = (e / max(1, max_per_orbital - 1)) * quadrant_width if max_per_orbital > 1 else 0
                    angle = quadrant_angle + angle_in_quadrant
                    
                    radius = shell_num * 1.5
                    x = center_x + radius * np.cos(angle)
                    y = center_y + radius * np.sin(angle)
                    
                    # Draw electron dot
                    electron = plt.Circle((x, y), 0.15, color=color, ec='white',
                                        linewidth=1.5, zorder=3)
                    ax.add_patch(electron)
                    
                    # Add orbital label on first electron
                    if e == 0:
                        ax.text(x, y - 0.33, orbital, fontsize=6, 
                               color=color, ha='center', va='top',
                               weight='bold', alpha=0.7)
                    
                    electron_count += 1
            
            # Add title and element info
            ax.text(center_x, center_y + 5, 'Electron Configuration Growth',
                   ha='center', fontsize=12, color='white', weight='bold')
            ax.text(center_x, center_y + 4.3, f'{element_name} (Z={z}, {z} electrons)',
                   ha='center', fontsize=11, color='#4ECDC4', weight='bold')
            
            # Show electron configuration string
            config_str = ''.join([f'{orbital}{count}' for orbital, count in config.items()])
            ax.text(center_x, center_y - 3.5, config_str, ha='center', fontsize=8,
                   color='#888888', family='monospace',
                   bbox=dict(boxstyle='round', facecolor='#1a1a1a', 
                            edgecolor='#888888', linewidth=0.5, alpha=0.8))
            
            # Legend
            legend_y = -4.2
            legend_x = 1
            for orbital_type, color in self.orbital_colors.items():
                circ = plt.Circle((legend_x, legend_y), 0.1, color=color, ec='white', linewidth=0.8)
                ax.add_patch(circ)
                ax.text(legend_x + 0.4, legend_y, f'{orbital_type}-orbital', 
                       va='center', fontsize=7, color='white')
                legend_y -= 0.4
            
            # Set view
            ax.set_xlim(0, 14)
            ax.set_ylim(-5, 10)
            ax.axis('off')
        
        # Create animation
        def animate(frame_num):
            draw_frame(frame_num + 1)
        
        anim = animation.FuncAnimation(fig, animate, frames=max_z,
                                     interval=300, repeat=True)
        
        anim.save(filename, writer='pillow', dpi=100)
        plt.close()
        print(f"✓ Saved {filename}")
    
    def generate_orbital_filling_order(self, filename='orbital_filling_order.png'):
        """
        Create diagonal rule diagram (aufbau principle)
        Shows the order in which orbitals fill
        """
        fig, ax = plt.subplots(figsize=(14, 10), dpi=150)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        # Draw n vs l grid showing filling order
        n_values = range(1, 8)  # n = 1 to 7
        l_values = range(0, 4)   # l = 0(s) to 3(f)
        l_names = ['s', 'p', 'd', 'f']
        
        # Filling order (approximate)
        filling_order = [
            (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2),
            (4, 1), (5, 0), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2),
            (6, 1), (7, 0), (5, 3), (6, 2), (7, 1)
        ]
        
        # Draw grid
        for n in n_values:
            for l in l_values:
                if l < n:  # Valid only if l < n
                    x = n
                    y = l
                    
                    # Color based on filling order
                    if (n, l) in filling_order:
                        order_idx = filling_order.index((n, l))
                        color_intensity = order_idx / len(filling_order)
                        color = plt.cm.RdYlGn_r(color_intensity)
                    else:
                        color = '#333333'
                    
                    box = FancyBboxPatch((x-0.35, y-0.35), 0.7, 0.7,
                                       boxstyle="round,pad=0.02",
                                       facecolor=color, edgecolor='white',
                                       linewidth=1.5, alpha=0.8)
                    ax.add_patch(box)
                    
                    # Orbital label
                    ax.text(x, y, f'{n}{l_names[l]}', ha='center',
                           va='center', fontsize=10, color='white',
                           weight='bold')
                    
                    # Filling order number
                    if (n, l) in filling_order:
                        order_num = filling_order.index((n, l)) + 1
                        ax.text(x+0.25, y+0.25, str(order_num), ha='center',
                               va='center', fontsize=7, color='white',
                               bbox=dict(boxstyle='circle', facecolor='black',
                                       edgecolor='white', linewidth=0.5))
        
        # Draw aufbau diagonal
        for i, (n, l) in enumerate(filling_order):
            if i < len(filling_order) - 1:
                n_next, l_next = filling_order[i + 1]
                ax.arrow(n, l, n_next-n-0.15, l_next-l-0.15,
                        head_width=0.1, head_length=0.05,
                        fc='#FFD700', ec='#FFD700', alpha=0.5,
                        linewidth=1, length_includes_head=True)
        
        # Labels
        ax.set_xlabel('Principle Quantum Number (n)', fontsize=11,
                     color='white', weight='bold')
        ax.set_ylabel('Angular Momentum (l)', fontsize=11,
                     color='white', weight='bold')
        ax.set_title('AUFBAU PRINCIPLE: Orbital Filling Order',
                    fontsize=13, color='white', weight='bold', pad=20)
        
        ax.set_xticks(n_values)
        ax.set_yticks(l_values)
        ax.set_xticklabels(n_values, color='white')
        ax.set_yticklabels([l_names[l] for l in l_values], color='white')
        ax.tick_params(colors='white', labelsize=10)
        
        ax.set_xlim(0.3, 7.7)
        ax.set_ylim(-0.7, 3.7)
        ax.grid(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout(pad=3.0, w_pad=0.8, h_pad=1.2)
        plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        print(f"✓ Saved {filename}")


class CompositionHierarchyGenerator:
    """Generate compositional emergence tree - how elements combine into containers"""
    
    def __init__(self):
        """Initialize hierarchy levels"""
        self.hierarchy_levels = [
            {
                'name': 'ELECTRONS',
                'color': '#FF6B6B',
                'examples': ['e⁻', 'e⁻', 'e⁻'],
                'description': 'Fundamental particles',
                'capacity': '∞ per orbital'
            },
            {
                'name': 'ATOMS',
                'color': '#4ECDC4',
                'examples': ['H', 'C', 'O', 'N'],
                'description': 'Electron containers',
                'capacity': '1-118 electrons'
            },
            {
                'name': 'MOLECULES',
                'color': '#45B7D1',
                'examples': ['H₂O', 'CO₂', 'C₆H₁₂O₆', 'DNA'],
                'description': 'Atom containers',
                'capacity': 'Many atoms'
            },
            {
                'name': 'MATERIALS',
                'color': '#FFA07A',
                'examples': ['Ice', 'Diamond', 'Metal', 'Polymer'],
                'description': 'Molecule containers (crystals/polymers)',
                'capacity': 'Moles of molecules'
            },
            {
                'name': 'BIOMOLECULES',
                'color': '#FFD700',
                'examples': ['Proteins', 'RNA', 'Lipids', 'Carbs'],
                'description': 'Functional material containers',
                'capacity': 'Molecular machines'
            },
            {
                'name': 'ORGANELLES',
                'color': '#98D8C8',
                'examples': ['Mitochondria', 'Nucleus', 'Ribosome'],
                'description': 'Biomolecule containers',
                'capacity': 'Thousands of proteins'
            },
            {
                'name': 'CELLS',
                'color': '#6BCB77',
                'examples': ['Prokaryote', 'Eukaryote', 'Neuron', 'Muscle'],
                'description': 'Organelle containers',
                'capacity': '10,000+ organelles'
            },
            {
                'name': 'TISSUES',
                'color': '#4D96FF',
                'examples': ['Muscle', 'Nerve', 'Epithelial', 'Connective'],
                'description': 'Cell containers',
                'capacity': 'Billions of cells'
            },
            {
                'name': 'ORGANS',
                'color': '#9D84B7',
                'examples': ['Brain', 'Heart', 'Liver', 'Lung'],
                'description': 'Tissue containers',
                'capacity': 'Multiple tissues'
            },
            {
                'name': 'ORGANISMS',
                'color': '#FF6B9D',
                'examples': ['Human', 'Plant', 'Animal', 'Microbe'],
                'description': 'Organ containers',
                'capacity': '37+ trillion cells'
            }
        ]
    
    def generate_composition_tree(self, filename='composition_hierarchy_tree.png'):
        """Generate vertical tree showing compositional emergence"""
        fig, ax = plt.subplots(figsize=(16, 20), dpi=150)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        num_levels = len(self.hierarchy_levels)
        level_height = 1.8
        
        # Draw levels from bottom-up
        for idx, level in enumerate(self.hierarchy_levels):
            y = idx * level_height
            
            # Draw main container box
            box_height = 1.4
            box = FancyBboxPatch((2, y), 12, box_height,
                               boxstyle="round,pad=0.1",
                               facecolor=level['color'], edgecolor='white',
                               linewidth=2.5, alpha=0.7, zorder=2)
            ax.add_patch(box)
            
            # Level name (left)
            ax.text(2.5, y + box_height/2, level['name'],
                   ha='left', va='center', fontsize=13, color='white',
                   weight='bold', family='monospace')
            
            # Description (center-left)
            ax.text(6, y + box_height/2 + 0.3, level['description'],
                   ha='left', va='center', fontsize=9, color='white',
                   style='italic', alpha=0.9)
            
            # Capacity (center-right)
            ax.text(6, y + box_height/2 - 0.3, f"Capacity: {level['capacity']}",
                   ha='left', va='center', fontsize=8, color='#CCCCCC',
                   alpha=0.8)
            
            # Examples (right) - visual bubbles
            examples = level['examples']
            ex_x = 10.5
            for ex_idx, example in enumerate(examples):
                ex_circle = Circle((ex_x + ex_idx * 1.2, y + box_height/2),
                                  0.35, color=level['color'], ec='white',
                                  linewidth=1.5, alpha=0.9, zorder=3)
                ax.add_patch(ex_circle)
                ax.text(ex_x + ex_idx * 1.2, y + box_height/2, example,
                       ha='center', va='center', fontsize=7, color='white',
                       weight='bold')
            
            # Draw arrow to next level
            if idx < num_levels - 1:
                arrow = FancyArrowPatch((8, y + box_height), (8, y + level_height),
                                      arrowstyle='->', mutation_scale=25,
                                      color='#FFD700', linewidth=2.5,
                                      alpha=0.8, zorder=1)
                ax.add_patch(arrow)
                
                # Emergence label
                ax.text(8.5, y + box_height + level_height/2, 
                       'combines &\nEMERGES',
                       ha='left', va='center', fontsize=8, color='#FFD700',
                       weight='bold', style='italic')
        
        # Title and overall context
        ax.text(8, num_levels * level_height + 0.8, 
               'COMPOSITIONAL GENEALOGY TREE',
               ha='center', fontsize=15, color='white', weight='bold')
        ax.text(8, num_levels * level_height + 0.2,
               'How Elementary Particles Compose into Complex Containers',
               ha='center', fontsize=11, color='#888888', style='italic')
        
        # Key insight box
        insight_text = (
            "COMPLEXITY RULE:\n"
            "Each level = container for previous level\n"
            "New properties emerge at each composition"
        )
        ax.text(1, -1.2, insight_text,
               ha='left', va='top', fontsize=9, color='#FFD700',
               bbox=dict(boxstyle='round', facecolor='#1a3a1a',
                        edgecolor='#FFD700', linewidth=1.5, pad=0.7))
        
        # Configure axes
        ax.set_xlim(0, 15)
        ax.set_ylim(-1.5, num_levels * level_height + 1.5)
        ax.axis('off')
        
        plt.tight_layout(pad=3.0, w_pad=0.8, h_pad=1.2)
        plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        print(f"✓ Saved {filename}")
    
    def generate_branching_genealogy(self, filename='branching_genealogy.png'):
        """
        Generate tree showing how different combinations create diversity
        e.g., H+C → CₙHₙ → many different molecules → many materials
        """
        fig, ax = plt.subplots(figsize=(18, 12), dpi=150)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        # Root: electrons
        root_y = 10
        root_x = 9
        
        root_circle = Circle((root_x, root_y), 0.4, color='#FF6B6B',
                           ec='white', linewidth=2, zorder=3)
        ax.add_patch(root_circle)
        ax.text(root_x, root_y, 'e⁻', ha='center', va='center',
               fontsize=11, color='white', weight='bold')
        
        # Level 1: Atoms (branching)
        atoms = ['H', 'C', 'O', 'N', 'S']
        atom_y = 8
        atom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#FFD700']
        
        for i, (atom, color) in enumerate(zip(atoms, atom_colors)):
            atom_x = 3 + i * 3
            
            # Draw branch
            ax.plot([root_x, atom_x], [root_y - 0.4, atom_y + 0.3],
                   color='#666666', linewidth=1.5, alpha=0.6, zorder=1)
            
            # Draw atom node
            atom_circle = Circle((atom_x, atom_y), 0.35, color=color,
                               ec='white', linewidth=1.5, zorder=3)
            ax.add_patch(atom_circle)
            ax.text(atom_x, atom_y, atom, ha='center', va='center',
                   fontsize=10, color='white', weight='bold')
        
        # Level 2: Molecules (further branching)
        molecules_data = [
            (1.5, 'H₂', '#4ECDC4'),
            (3, 'H₂O', '#4ECDC4'),
            (4.5, 'CO₂', '#4ECDC4'),
            (6, 'NH₃', '#45B7D1'),
            (7.5, 'CH₄', '#45B7D1'),
            (9, 'C₆H₁₂O₆', '#FFD700'),
            (10.5, 'C₈H₁₀N₄O₂', '#FFD700'),
            (12, 'H₂S', '#666666'),
            (13.5, 'SO₂', '#FF6B6B'),
            (15, 'DNA', '#4ECDC4'),
        ]
        
        mol_y = 5.5
        atom_xs_list = [3, 6, 9, 12, 15]
        for mol_x, mol_name, mol_color in molecules_data:
            # Branch from atoms (closest atom)
            closest_atom_x = min(atom_xs_list,
                               key=lambda x: abs(x - mol_x))
            
            ax.plot([closest_atom_x, mol_x], [atom_y - 0.35, mol_y + 0.25],
                   color='#666666', linewidth=1, alpha=0.4, zorder=1)
            
            # Draw molecule node (smaller)
            mol_circle = Circle((mol_x, mol_y), 0.25, color=mol_color,
                              ec='white', linewidth=1, zorder=3)
            ax.add_patch(mol_circle)
            ax.text(mol_x, mol_y - 0.55, mol_name, ha='center', va='top',
                   fontsize=7, color='white')
        
        # Level 3: Materials (crown)
        materials_data = [
            (2, 'Ice', '#45B7D1'),
            (5, 'Proteins', '#6BCB77'),
            (8, 'RNA', '#98D8C8'),
            (11, 'Lipids', '#FFD700'),
            (14, 'Cellulose', '#FF6B6B'),
        ]
        
        mat_y = 2.5
        for mat_x, mat_name, mat_color in materials_data:
            # Branch from nearby molecules
            nearby_mol_x = min([mx for mx, _, _ in molecules_data],
                             key=lambda x: abs(x - mat_x))
            
            ax.plot([nearby_mol_x, mat_x], [mol_y - 0.25, mat_y + 0.3],
                   color='#666666', linewidth=1.5, alpha=0.4, zorder=1)
            
            # Draw material node
            mat_circle = Circle((mat_x, mat_y), 0.3, color=mat_color,
                              ec='white', linewidth=1.5, zorder=3)
            ax.add_patch(mat_circle)
            ax.text(mat_x, mat_y - 0.65, mat_name, ha='center', va='top',
                   fontsize=8, color='white', weight='bold')
        
        # Title
        ax.text(9, 10.8, 'BRANCHING GENEALOGY: Combinatorial Emergence',
               ha='center', fontsize=13, color='white', weight='bold')
        ax.text(9, 10.4, 'One electron type + different combinations = infinite diversity',
               ha='center', fontsize=10, color='#888888', style='italic')
        
        # Configure axes
        ax.set_xlim(0, 16)
        ax.set_ylim(1, 11.5)
        ax.axis('off')
        
        plt.tight_layout(pad=3.0, w_pad=0.8, h_pad=1.2)
        plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        print(f"✓ Saved {filename}")


class BinaryCompositionTracer:
    """Binary encoding of compositional hierarchy - genealogy at binary level"""
    
    def __init__(self):
        """Initialize binary tracing system"""
        self.composition_map = {
            'H': {'electrons': [1], 'binary': '1'},
            'C': {'electrons': [1, 1, 1, 1, 1, 1], 'binary': '111111'},
            'O': {'electrons': [1, 1, 1, 1, 1, 1, 1, 1], 'binary': '11111111'},
            'N': {'electrons': [1, 1, 1, 1, 1, 1, 1], 'binary': '1111111'},
        }
    
    def trace_hydrogen_binary(self):
        """H: 1 electron = binary 1"""
        return {
            'element': 'H',
            'electrons': 1,
            'binary': '1',
            'description': 'Single electron in 1s orbital'
        }
    
    def trace_carbon_binary(self):
        """C: 6 electrons = binary 111111"""
        return {
            'element': 'C',
            'electrons': 6,
            'binary': '111111',
            'orbitals': '1s² 2s² 2p²',
            'description': 'Carbon: foundation of organic molecules'
        }
    
    def trace_water_binary(self):
        """H₂O: combines H(1) + H(1) + O(11111111)"""
        h_binary = '1'
        o_binary = '11111111'
        
        # Molecular binary: encoding which atoms are present
        # H: bit position 1, H: bit position 2, O: bit position 3
        molecule_binary = '110'  # HHO present in molecule
        
        return {
            'molecule': 'H₂O',
            'components': ['H', 'H', 'O'],
            'electron_total': 1 + 1 + 8,
            'binary_components': [h_binary, h_binary, o_binary],
            'binary_molecular': molecule_binary,
            'electron_binary_full': h_binary + h_binary + o_binary,
            'description': 'Water: H₂O combines atoms via covalent bonds'
        }
    
    def trace_methane_binary(self):
        """CH₄: C(111111) + 4×H(1)"""
        c_binary = '111111'
        h_binary = '1'
        
        molecules_present = '10001'  # C present, 4 H present
        
        return {
            'molecule': 'CH₄',
            'components': ['C', 'H', 'H', 'H', 'H'],
            'electron_total': 6 + 4,
            'binary_components': [c_binary] + [h_binary] * 4,
            'binary_molecular': molecules_present,
            'electron_binary_full': c_binary + h_binary * 4,
            'description': 'Methane: Carbon bonded to 4 hydrogens'
        }
    
    def trace_glucose_binary(self):
        """C₆H₁₂O₆: 6 carbons, 12 hydrogens, 6 oxygens"""
        # Simplified: track atom counts as binary
        atom_counts = {
            'C': 6,
            'H': 12,
            'O': 6
        }
        
        # Binary presence: which atom types are in this molecule?
        binary_types = '111'  # C, H, O all present
        
        # Count encoding: how many of each?
        c_count_binary = bin(6)[2:].zfill(4)  # '0110'
        h_count_binary = bin(12)[2:].zfill(4)  # '1100'
        o_count_binary = bin(6)[2:].zfill(4)   # '0110'
        
        total_electrons = (6 * 6) + (12 * 1) + (6 * 8)  # 132 electrons
        
        return {
            'molecule': 'C₆H₁₂O₆',
            'atom_counts': atom_counts,
            'electron_total': total_electrons,
            'binary_presence': binary_types,
            'binary_counts': f"C:{c_count_binary} H:{h_count_binary} O:{o_count_binary}",
            'description': 'Glucose: Complex sugar (6-carbon backbone)'
        }
    
    def generate_binary_genealogy_tree(self, filename='binary_genealogy_tree.png'):
        """Generate tree showing binary genealogy of compositions"""
        fig, ax = plt.subplots(figsize=(18, 14), dpi=150)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        
        # Title
        ax.text(9, 13.5, 'BINARY GENEALOGY TREE',
               ha='center', fontsize=14, color='white', weight='bold')
        ax.text(9, 13, 'How Composition creates Binary Signatures',
               ha='center', fontsize=11, color='#FFD700', style='italic')
        
        # Level 1: Electrons (fundamental)
        ax.text(1, 12, 'LEVEL 1: ELECTRONS',
               ha='left', fontsize=11, color='#FF6B6B', weight='bold')
        
        electron_box = FancyBboxPatch((1, 11), 3, 0.7,
                                     boxstyle="round,pad=0.05",
                                     facecolor='#FF6B6B', edgecolor='white',
                                     linewidth=2, alpha=0.7)
        ax.add_patch(electron_box)
        ax.text(2.5, 11.35, 'Electron: 1', ha='center', va='center',
               fontsize=9, color='white', weight='bold', family='monospace')
        
        # Level 2: Atoms (H, C, O)
        ax.text(1, 10, 'LEVEL 2: ATOMS',
               ha='left', fontsize=11, color='#4ECDC4', weight='bold')
        
        atoms_data = [
            (1, 'H = 1 electron', '1', '#FF6B6B'),
            (3, 'C = 6 electrons', '111111', '#4ECDC4'),
            (5, 'O = 8 electrons', '11111111', '#45B7D1'),
        ]
        
        for x, label, binary, color in atoms_data:
            atom_box = FancyBboxPatch((x, 8.8), 1.8, 0.8,
                                     boxstyle="round,pad=0.05",
                                     facecolor=color, edgecolor='white',
                                     linewidth=1.5, alpha=0.7)
            ax.add_patch(atom_box)
            ax.text(x + 0.9, 9.4, label, ha='center', va='center',
                   fontsize=8, color='white')
            ax.text(x + 0.9, 9, binary, ha='center', va='center',
                   fontsize=7, color='white', family='monospace',
                   bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
            
            # Arrow from electron
            ax.annotate('', xy=(x + 0.9, 8.8), xytext=(2.5, 11),
                       arrowprops=dict(arrowstyle='->', color='#666666',
                                     lw=1, alpha=0.5))
        
        # Level 3: Molecules
        ax.text(1, 8, 'LEVEL 3: MOLECULES',
               ha='left', fontsize=11, color='#45B7D1', weight='bold')
        
        h2o_trace = self.trace_water_binary()
        ch4_trace = self.trace_methane_binary()
        
        # H₂O
        h2o_box = FancyBboxPatch((0.8, 6.2), 2.5, 1.2,
                               boxstyle="round,pad=0.05",
                               facecolor='#4ECDC4', edgecolor='white',
                               linewidth=1.5, alpha=0.7)
        ax.add_patch(h2o_box)
        ax.text(2.05, 7, 'H₂O (Water)', ha='center', fontsize=9,
               color='white', weight='bold')
        ax.text(2.05, 6.6, f"10 electrons total", ha='center', fontsize=7,
               color='#CCCCCC')
        ax.text(2.05, 6.35, '1+1+11111111', ha='center', fontsize=6,
               color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.4))
        
        # CH₄
        ch4_box = FancyBboxPatch((3.8, 6.2), 2.5, 1.2,
                               boxstyle="round,pad=0.05",
                               facecolor='#45B7D1', edgecolor='white',
                               linewidth=1.5, alpha=0.7)
        ax.add_patch(ch4_box)
        ax.text(5.05, 7, 'CH₄ (Methane)', ha='center', fontsize=9,
               color='white', weight='bold')
        ax.text(5.05, 6.6, f"10 electrons total", ha='center', fontsize=7,
               color='#CCCCCC')
        ax.text(5.05, 6.35, '111111+1+1+1+1', ha='center', fontsize=6,
               color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.4))
        
        # Level 4: Biopolymers (combine molecules)
        ax.text(1, 5.5, 'LEVEL 4: BIOPOLYMERS',
               ha='left', fontsize=11, color='#FFD700', weight='bold')
        
        # Glucose
        glucose_trace = self.trace_glucose_binary()
        
        glucose_box = FancyBboxPatch((0.8, 3.2), 5.5, 2,
                                    boxstyle="round,pad=0.05",
                                    facecolor='#FFD700', edgecolor='white',
                                    linewidth=1.5, alpha=0.7)
        ax.add_patch(glucose_box)
        ax.text(3.55, 4.8, 'C₆H₁₂O₆ (Glucose)', ha='center', fontsize=10,
               color='white', weight='bold')
        ax.text(3.55, 4.4, '6 Carbons + 12 Hydrogens + 6 Oxygens',
               ha='center', fontsize=8, color='#CCCCCC')
        ax.text(3.55, 3.95, f"Binary Presence: {glucose_trace['binary_presence']}",
               ha='center', fontsize=7, color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
        ax.text(3.55, 3.5, f"Atom Counts: C:6, H:12, O:6",
               ha='center', fontsize=7, color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
        
        # Arrows showing composition
        ax.annotate('combines', xy=(2.05, 6.2), xytext=(2, 5.5),
                   fontsize=7, color='#FFD700', ha='center',
                   arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1))
        ax.annotate('combines', xy=(5.05, 6.2), xytext=(5, 5.5),
                   fontsize=7, color='#FFD700', ha='center',
                   arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1))
        
        # Level 5: Biomolecules (functional)
        ax.text(1, 2.7, 'LEVEL 5: FUNCTIONAL COMPONENTS',
               ha='left', fontsize=11, color='#6BCB77', weight='bold')
        
        protein_box = FancyBboxPatch((0.8, 0.8), 2.2, 1.6,
                                    boxstyle="round,pad=0.05",
                                    facecolor='#6BCB77', edgecolor='white',
                                    linewidth=1.5, alpha=0.7)
        ax.add_patch(protein_box)
        ax.text(1.9, 2, 'PROTEINS', ha='center', fontsize=9,
               color='white', weight='bold')
        ax.text(1.9, 1.6, 'Amino acids\n(100+ types)', ha='center',
               fontsize=7, color='#CCCCCC')
        ax.text(1.9, 1, 'Binary: Presence\nof functional groups',
               ha='center', fontsize=6, color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
        
        dna_box = FancyBboxPatch((3.5, 0.8), 2.2, 1.6,
                               boxstyle="round,pad=0.05",
                               facecolor='#4ECDC4', edgecolor='white',
                               linewidth=1.5, alpha=0.7)
        ax.add_patch(dna_box)
        ax.text(4.6, 2, 'DNA/RNA', ha='center', fontsize=9,
               color='white', weight='bold')
        ax.text(4.6, 1.6, 'Nucleotides\n(4 types: ACGT)',
               ha='center', fontsize=7, color='#CCCCCC')
        ax.text(4.6, 1, 'Binary: Base pairs\n(4-bit code)',
               ha='center', fontsize=6, color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
        
        lipids_box = FancyBboxPatch((6.2, 0.8), 2.2, 1.6,
                                   boxstyle="round,pad=0.05",
                                   facecolor='#FFD700', edgecolor='white',
                                   linewidth=1.5, alpha=0.7)
        ax.add_patch(lipids_box)
        ax.text(7.3, 2, 'LIPIDS', ha='center', fontsize=9,
               color='white', weight='bold')
        ax.text(7.3, 1.6, 'Fatty acids\n& chains',
               ha='center', fontsize=7, color='#CCCCCC')
        ax.text(7.3, 1, 'Binary: Saturation\npattern',
               ha='center', fontsize=6, color='white', family='monospace',
               bbox=dict(boxstyle='round', facecolor='black', alpha=0.3))
        
        # Final insight
        ax.text(9, 0.2, 'KEY: Each level encodes previous levels in binary. Composition = Binary pattern combination.',
               ha='center', fontsize=9, color='#FFD700', style='italic',
               bbox=dict(boxstyle='round', facecolor='#1a3a1a',
                        edgecolor='#FFD700', linewidth=1.5, pad=0.5))
        
        # Configure axes
        ax.set_xlim(0, 16)
        ax.set_ylim(-0.5, 14)
        ax.axis('off')
        
        plt.tight_layout(pad=3.0, w_pad=0.8, h_pad=1.2)
        plt.savefig(filename, bbox_inches='tight', dpi=150, facecolor='#1a1a1a')
        plt.close()
        print(f"✓ Saved {filename}")


def generate_all_electron_trees():
    """Generate all electron tree visualizations"""
    generator = ElectronTreeGenerator()
    composition_gen = CompositionHierarchyGenerator()
    binary_gen = BinaryCompositionTracer()
    
    print("\nGenerating Electron Evolutionary Tree Visualizations...\n")
    
    generator.generate_orbital_tree_static()
    generator.generate_element_genealogy_tree()
    generator.generate_orbital_filling_order()
    generator.generate_electron_growth_animation()
    
    print("\nGenerating Compositional Hierarchy Visualizations...\n")
    
    composition_gen.generate_composition_tree()
    composition_gen.generate_branching_genealogy()
    
    print("\nGenerating Binary Genealogy Tree...\n")
    
    binary_gen.generate_binary_genealogy_tree()
    
    print("\n✓ All evolutionary trees generated successfully!")


if __name__ == '__main__':
    generate_all_electron_trees()
