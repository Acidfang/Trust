# Scene entries for ATOM_COMPLEX and MOLECULE_BONDED
# Add these to your scenes.json file

## For scenes.json:

[
  {
    "id": "ILL_ATOM_COMPLEX",
    "lighting_mode": "self_luminous",
    "aspect_ratio": "1:1",
    "seed": 4847,
    "elements": [
      {
        "type": "nucleus",
        "motif": "primitive_point",
        "material": "emissive_point",
        "x": 1024,
        "y": 1024,
        "brightness": 0.95,
        "size": 12
      },
      {
        "type": "inner_shell",
        "motif": "coherence_spiral",
        "material": "emissive_soft",
        "center_x": 1024,
        "center_y": 1024,
        "radius": 120,
        "brightness": 0.70,
        "spiral_direction": "inward",
        "electrons": 3
      },
      {
        "type": "middle_shell",
        "motif": "coherence_spiral",
        "material": "emissive_soft",
        "center_x": 1024,
        "center_y": 1024,
        "radius": 220,
        "brightness": 0.50,
        "spiral_direction": "inward",
        "electrons": 8
      },
      {
        "type": "outer_shell",
        "motif": "time_trace",
        "material": "transparent_grid",
        "center_x": 1024,
        "center_y": 1024,
        "radius": 340,
        "brightness": 0.30,
        "trace_states": 4,
        "electrons": 8
      },
      {
        "type": "field_background",
        "motif": "field_wave_grid",
        "material": "transparent_grid",
        "brightness": 0.05,
        "grid_density": 0.15
      }
    ],
    "constraints": [
      "no_text",
      "background_absolute_black:10",
      "center_element_dominant:true",
      "field_grid_max_weight:0.05",
      "glow_radius_max_pct:8",
      "light_fill_min_pct:15",
      "darkness_max_pct:70"
    ],
    "description": "Complex atom with multiple electron shells. Brightness encodes coherence/binding energy. Nucleus at 0.95 (maximum), inner shells brighter than outer shells."
  },
  {
    "id": "ILL_MOLECULE_BONDED",
    "lighting_mode": "self_luminous",
    "aspect_ratio": "1:1",
    "seed": 5921,
    "elements": [
      {
        "type": "nucleus_left",
        "motif": "primitive_point",
        "material": "emissive_point",
        "x": 750,
        "y": 1024,
        "brightness": 0.80,
        "size": 10
      },
      {
        "type": "nucleus_right",
        "motif": "primitive_point",
        "material": "emissive_point",
        "x": 1300,
        "y": 1024,
        "brightness": 0.80,
        "size": 10
      },
      {
        "type": "shared_electrons",
        "motif": "coherence_spiral",
        "material": "emissive_soft",
        "center_x": 1025,
        "center_y": 1024,
        "radius": 140,
        "brightness": 0.75,
        "spiral_direction": "inward",
        "orbit_path": "figure_eight",
        "electrons": 2
      },
      {
        "type": "left_atomic_shell",
        "motif": "time_trace",
        "material": "transparent_grid",
        "center_x": 750,
        "center_y": 1024,
        "radius": 180,
        "brightness": 0.50,
        "trace_states": 3
      },
      {
        "type": "right_atomic_shell",
        "motif": "time_trace",
        "material": "transparent_grid",
        "center_x": 1300,
        "center_y": 1024,
        "radius": 180,
        "brightness": 0.50,
        "trace_states": 3
      },
      {
        "type": "bonding_field",
        "motif": "water_flow",
        "material": "transparent_grid",
        "center_x": 1025,
        "center_y": 1024,
        "radius": 200,
        "brightness": 0.30,
        "flow_direction": "bidirectional",
        "flow_wavelength": 0.8
      },
      {
        "type": "field_background",
        "motif": "field_wave_grid",
        "material": "transparent_grid",
        "brightness": 0.05,
        "grid_density": 0.15
      }
    ],
    "constraints": [
      "no_text",
      "background_absolute_black:10",
      "center_two_elements_balanced:true",
      "field_grid_max_weight:0.05",
      "glow_radius_max_pct:8",
      "light_fill_min_pct:20",
      "darkness_max_pct:60"
    ],
    "description": "Homonuclear diatomic molecule showing covalent bond. Two nuclei at 0.80 (equal strength). Shared electrons at 0.75 (bond region has high coherence). Individual shells dim at 0.50 because electrons migrated to bonding. Bidirectional flow field shows symmetric molecular coherence."
  }
]
