"""
CONTAINER-AWARE FUNCTIONAL COMPOSITION DEMONSTRATION
=====================================================

Shows how variants (like FFMpeg) carry references to their container context.
Same primitive used in different domains = different performance profiles.
"""

import sys
sys.path.insert(0, r'c:\Determined')

from FUNCTIONAL_COMPOSITION_FRAMEWORK import (
    Primitive, Container, ComposedMethod, Composer, VariantRegistry, 
    HybridGenerator, registry, composer, hybrid_generator
)

if __name__ == "__main__":
    print("=" * 100)
    print("CONTAINER-AWARE FUNCTIONAL COMPOSITION")
    print("=" * 100)
    print()
    
    # Define containers (domains)
    gif_container = Container(
        name="gif",
        domain_properties={
            "output_format": "GIF",
            "typical_frames": 36,
            "max_palette": 256,
            "optimization_focus": "file_size"
        }
    )
    
    video_container = Container(
        name="video",
        domain_properties={
            "output_format": "MP4/WebM",
            "typical_frames": 1800,
            "framerate": 30,
            "optimization_focus": "quality_speed"
        }
    )
    
    molecular_container = Container(
        name="molecular_rendering",
        domain_properties={
            "output_format": "PNG/VTK",
            "typical_complexity": "high",
            "accuracy_critical": True,
            "optimization_focus": "precision"
        }
    )
    
    # Register containers
    composer.register_container(gif_container)
    composer.register_container(video_container)
    composer.register_container(molecular_container)
    
    print("0. CONTAINERS (Domains) DEFINED")
    print("-" * 100)
    for container_name, container in composer.container_registry.items():
        print(f"\n  {container.name}:")
        for prop, value in container.domain_properties.items():
            print(f"    - {prop}: {value}")
    print()
    
    # Example 1: FFMpeg in different containers
    print("\n1. FFMpeg REFERENCES ACROSS CONTAINERS")
    print("=" * 100)
    
    ffmpeg_gif_config = {
        Primitive.RENDER: "parallel",
        Primitive.BATCH: "ring_buffer",
        Primitive.TRANSFER: "pipe",
        Primitive.ENCODE: "ffmpeg",
        Primitive.OPTIMIZE: "gifsicle",
    }
    
    ffmpeg_video_config = {
        Primitive.RENDER: "gpu",
        Primitive.BATCH: "ring_buffer",
        Primitive.TRANSFER: "gpu_memory",
        Primitive.ENCODE: "ffmpeg",
        Primitive.OPTIMIZE: "none",
    }
    
    ffmpeg_molecular_config = {
        Primitive.RENDER: "jit",
        Primitive.BATCH: "generator",
        Primitive.TRANSFER: "streaming",
        Primitive.ENCODE: "ffmpeg",
        Primitive.OPTIMIZE: "palette",
    }
    
    method_gif = composer.compose("GIF_FFMpeg", ffmpeg_gif_config, container=gif_container)
    method_video = composer.compose("Video_FFMpeg", ffmpeg_video_config, container=video_container)
    method_mol = composer.compose("Molecular_FFMpeg", ffmpeg_molecular_config, container=molecular_container)
    
    print(f"\nFFMpeg appears in three domains with DIFFERENT context:\n")
    print(f"  GIF Domain:      {method_gif}")
    print(f"  Video Domain:    {method_video}")
    print(f"  Molecular Domain: {method_mol}")
    
    print(f"\nEach method shows FFMpeg but in a DIFFERENT CONTAINER context:")
    print(f"  - Same encode primitive (FFMpeg)")
    print(f"  - Different surrounding pipeline (render/batch/transfer/optimize)")
    print(f"  - Different container reference automatically attached")
    
    print()
    print("-" * 100)
    
    # Example 2: Container signatures
    print("\n2. CONTAINER AFFECTS SIGNATURES")
    print("=" * 100)
    
    sig_gif = method_gif.get_signature()
    sig_video = method_video.get_signature()
    sig_mol = method_mol.get_signature()
    
    print(f"\nSignatures (container-aware):")
    print(f"  GIF:      {sig_gif}    (includes 'gif' in hash)")
    print(f"  Video:    {sig_video}    (includes 'video' in hash)")
    print(f"  Molecular:{sig_mol}    (includes 'molecular_rendering' in hash)")
    
    print(f"\nSame variant combinations IN DIFFERENT CONTAINERS = DIFFERENT SIGNATURES")
    print(f"This prevents cross-domain confusion and enables domain-specific optimization")
    
    print()
    print("-" * 100)
    
    # Example 3: Which variants appear in each container
    print("\n3. CONTAINER-SPECIFIC VARIANT USAGE")
    print("=" * 100)
    
    all_hybrids = hybrid_generator.generate_all_combinations()
    
    # Analyze which variants appear where (if we had container tagging in generation)
    print(f"\nGenerated {len(all_hybrids)} hybrid combinations")
    print(f"(In real usage, these would be tagged with container context)")
    
    # Show FFMpeg's representation across containers
    print(f"\nFFMpeg encoding profile (metadata):")
    ffmpeg_meta = registry._metadata.get("encode:ffmpeg", {})
    for dimension, value in ffmpeg_meta.items():
        print(f"  - {dimension}: {value}")
    
    print(f"\nBut this profile behaves differently based on CONTAINER:")
    print(f"  GIF context:       FFMpeg {ffmpeg_meta} + gifsicle post-process (palette focus)")
    print(f"  Video context:     FFMpeg {ffmpeg_meta} alone (no extra optimization needed)")
    print(f"  Molecular context: FFMpeg {ffmpeg_meta} + palette (scientific color fidelity)")
    
    print()
    print("-" * 100)
    
    # Example 4: Container-aware optimization decisions
    print("\n4. CONTAINER DETERMINES OPTIMIZATION STRATEGY")
    print("=" * 100)
    
    weights_gif = {"speed": 0.2, "memory": 0.1, "quality": 0.3, "robustness": 0.4}
    weights_video = {"speed": 0.5, "memory": 0.2, "quality": 0.2, "robustness": 0.1}
    weights_molecular = {"speed": 0.1, "memory": 0.1, "quality": 0.7, "robustness": 0.1}
    
    print(f"\nOptimization priorities by container:")
    print(f"  GIF:           {weights_gif}     (prefer robustness)")
    print(f"  Video:         {weights_video}     (prefer speed)")
    print(f"  Molecular:     {weights_molecular}  (prefer quality)")
    
    print(f"\n=> Same variant gets different WEIGHT based on container context")
    print(f"=> FFMpeg scored 0.85 quality means different things in each domain")
    
    print()
    print("=" * 100)
    print("CONTAINERS COMPLETE: Variants are context-aware through their container")
    print("=" * 100)
    print()
    print("KEY INSIGHT:")
    print("  FFMpeg doesn't exist in a vacuum. It ALWAYS has a container reference.")
    print("  Same FFMpeg, different container => different pipeline, different weights")
    print("  The framework automatically routes through the right container context")
    print("=" * 100)
