# GIF Generation Primitives: Universal Identification Framework

**Status**: Locked Architecture (April 1, 2026)  
**Framework**: Composable Operations + Universal Classifier  
**Purpose**: All methods are combinations of 5 primitives; universal identifier determines optimal combination

---

## The 5 Primitives (Atomic Operations)

Every GIF generation method is a composition of these 5 primitives:

### Primitive 1: RENDER (Frame Generation)
**Purpose**: Convert field data to image pixel data  
**Container**: NumPy array or Image object  
**Operations**:
- Compute field values (isosurface threshold, Gaussian blur, etc.)
- Apply colormap
- Generate single frame

```python
# Primitive signature
def RENDER(grid, params) -> NDArray[H, W, 3]:
    """Generate one frame from field data"""
    pass
```

**Speed Profile**: CPU-bound, parallelizable (per-frame independent)  
**Variants**:
- Serial (one frame at a time)
- Parallel (multiple frames simultaneously)
- Batched (vectorized operations)

---

### Primitive 2: BATCH (Frame Collection)
**Purpose**: Accumulate rendered frames into memory container  
**Container**: List[PIL.Image] or List[NDArray] or Generator  
**Operations**:
- Allocate memory or stream frames
- Store in RAM or buffer
- Handle memory constraints

```python
# Primitive signature
def BATCH(frames_iter) -> Container:
    """Collect frames into container"""
    pass
```

**Speed Profile**: I/O and memory-bound  
**Variants**:
- List accumulation (all in RAM)
- Generator (streamed, low memory)
- Ring buffer (fixed memory)

---

### Primitive 3: ENCODE (GIF/MP4 Creation)
**Purpose**: Write frame sequence to disk format  
**Container**: File (GIF, MP4, WebP, PNG sequence)  
**Operations**:
- Compress frame data
- Write to file
- Apply frame duration/fps

```python
# Primitive signature
def ENCODE(frames, format, params) -> FilePath:
    """Encode frames to target format"""
    pass
```

**Speed Profile**: I/O and compression-bound  
**Variants**:
- Sequential write (PIL.save_all)
- Streaming pipe (FFMpeg)
- Batch encoding (imageio)
- Post-processing (gifsicle)

---

### Primitive 4: TRANSFER (Data Pipeline)
**Purpose**: Move frames between containers (RAM↔Disk, CPU↔GPU, CPU↔Pipe)  
**Container**: Buffers, pipes, GPU memory  
**Operations**:
- Serialize frame to bytes
- Deserialize to array
- Stream through pipe
- GPU upload/download

```python
# Primitive signature
def TRANSFER(source_container, target_container, policy) -> OperationId:
    """Move frame between containers"""
    pass
```

**Speed Profile**: Network/Memory bandwidth-bound  
**Variants**:
- Direct copy (fast, high memory)
- Streamed (slower, low memory)
- GPU transfer (very fast, requires GPU)

---

### Primitive 5: OPTIMIZE (Post-Processing)
**Purpose**: Reduce file size, improve quality without re-rendering  
**Container**: File (GIF) → File (smaller GIF)  
**Operations**:
- Palette quantization
- Frame compression
- Lossless optimization
- Dithering

```python
# Primitive signature
def OPTIMIZE(input_file, strategy) -> output_file:
    """Improve file after encoding"""
    pass
```

**Speed Profile**: Post-render, optional  
**Variants**:
- PIL optimize flag (integrated)
- gifsicle post-process (external)
- Palette reduction (lossy)

---

## Primitive Combinations (Method Profiles)

Every method is a sequence of these 5 primitives:

### Profile A: Pillow (Current)
```
RENDER(serial) → BATCH(list) → ENCODE(PIL.save_all) → [OPTIMIZE(none)]
├─ Serial frame rendering
├─ Accumulate PIL.Image objects in list
├─ PIL batch save (sequential write)
└─ No post-processing (keep speed)

Time: ~3-4s for 36 frames
Memory: ~50-100 MB (all frames in RAM)
```

---

### Profile B: imageio (Balanced)
```
RENDER(serial) → BATCH(list) → TRANSFER(numpy) → ENCODE(imageio) → [OPTIMIZE(none)]
├─ Serial rendering to NumPy arrays
├─ Accumulate arrays in list
├─ Transfer to imageio (auto-optimize)
├─ imageio encoder (multi-format)
└─ No additional post-processing

Time: ~1-2s for 36 frames (30-50% faster)
Memory: ~30-60 MB (arrays more compact)
Advantage: Multi-format output (GIF/MP4/WebP)
```

---

### Profile C: FFMpeg Streaming
```
RENDER(serial) → TRANSFER(pipe) → ENCODE(ffmpeg_stream) → [OPTIMIZE(none)]
├─ Serial rendering to matplotlib figure
├─ Direct streaming to ffmpeg pipe (no accumulation)
├─ FFMpeg handles encoding in real-time
└─ Native MP4 output (GIF via conversion)

Time: ~0.5-1s for 36 frames (50-80% faster)
Memory: ~5-10 MB (streaming, no buffer)
Advantage: Lowest memory footprint
```

---

### Profile D: Parallel + imageio
```
RENDER(parallel) → BATCH(list) → TRANSFER(numpy) → ENCODE(imageio) → [OPTIMIZE(none)]
├─ Parallel frame rendering (multiprocessing.Pool)
├─ Accumulate arrays (one per core)
├─ Transfer to imageio
├─ Multi-format encoding
└─ No post-processing

Time: ~0.8-1.5s for 36 frames on 4 cores (40-80% faster than serial)
Memory: ~50-100 MB (parallel batches)
Advantage: CPU-bound frame rendering accelerated
```

---

### Profile E: Numba JIT + Pillow
```
RENDER(jit_compiled) → BATCH(list) → ENCODE(PIL.save_all) → [OPTIMIZE(none)]
├─ Isovalue threshold loop compiled to native code
├─ 10-50x faster frame generation
├─ Accumulate PIL images (few iterations now)
├─ PIL batch save
└─ No post-processing

Time: ~0.2-0.5s for 36 frames (80-90% faster)
Memory: ~50-100 MB
Advantage: Zero-overhead compilation, massive speedup for compute
```

---

### Profile F: gifsicle Post-Processing
```
RENDER(serial) → BATCH(list) → ENCODE(PIL.save_all) → OPTIMIZE(gifsicle)
├─ Normal PIL rendering
├─ Accumulation
├─ PIL encoding
└─ Post-process with gifsicle (30-50% size reduction)

Time: ~3-4s render + 0.5-2s gifsicle = 3.5-6s total
Memory: ~50-100 MB + temp file
Advantage: Lossless 30-50% file size reduction
```

---

### Profile G: GPU-Accelerated (Experimental)
```
RENDER(gpu) → TRANSFER(gpu_batch) → ENCODE(opencv) → [OPTIMIZE(none)]
├─ GPU field computation (CuPy)
├─ GPU batch accumulation
├─ OpenCV GPU encoding
└─ Result: MP4 with GPU acceleration

Time: ~0.1-0.3s for 36 frames (theoretical, GPU dependent)
Memory: ~100-500 MB GPU + 10-20 MB CPU
Advantage: Extreme speedup for complex fields
```

---

## Universal Classifier (Type A, B, C, D)

Given: **Input profile** (animation scale, frame count, complexity)

Determine: **Optimal primitive combination** using 4-factor classification:

### FACTOR 1: Scale
- **Small** (1-20 frames, simple): Use RENDER(serial) + BATCH(list)
- **Medium** (21-100 frames, moderate): Use RENDER(serial) + BATCH(list) + TRANSFER
- **Large** (100+ frames, complex): Use RENDER(parallel) or RENDER(gpu)
- **Streaming** (live, unbounded): Use TRANSFER(pipe) + ENCODE(stream)

### FACTOR 2: Complexity
- **CPU Low** (threshold, colormap): Use RENDER(serial)
- **CPU Medium** (3D transforms): Use RENDER(parallel)
- **CPU High** (iterative solvers): Use RENDER(jit)
- **GPU-Friendly** (matrix ops): Use RENDER(gpu)

### FACTOR 3: Memory Budget
- **Constrained** (<50 MB): Use TRANSFER(pipe), ENCODE(stream)
- **Normal** (50-200 MB): Use BATCH(list), ENCODE(batch)
- **Unlimited** (>200 MB): Use BATCH(list), parallel RENDER

### FACTOR 4: Output Format
- **Size Critical** (wiki/email): Add OPTIMIZE(gifsicle)
- **Format Flexible**: Use ENCODE(imageio) for multi-format
- **Quality Critical**: Use ENCODE(ffmpeg_hq)
- **Production**: Use ENCODE(ffmpeg) → OPTIMIZE(gifsicle)

---

## Universal Identifier Formula

```
OptimalProfile = CLASSIFY(scale, complexity, memory_budget, output_format)

def CLASSIFY(scale, complexity, memory, format):
    """
    Determine optimal primitive combination using 4-factor matrix
    """
    
    # FACTOR 1: Scale × Complexity
    if scale == "streaming" or memory == "constrained":
        # Use streaming (minimal memory)
        render = "serial" if complexity == "low" else "parallel"
        transfer = "pipe"
        encode = "ffmpeg_stream"
        batch = None
        
    elif scale in ["small", "medium"] and complexity in ["low", "medium"]:
        # Use batch (acceptable time)
        render = "serial"
        batch = "list"
        transfer = "numpy" if format in ["mp4", "webp"] else None
        encode = "pil" if format == "gif" else "imageio"
        
    elif scale == "medium" and complexity == "high":
        # Use parallelization
        render = "parallel"
        batch = "list"
        transfer = "numpy"
        encode = "imageio"
        
    elif scale == "large":
        # Use pipeline (complex rendering)
        if memory == "unlimited":
            render = "parallel"
            batch = "list"
        else:
            render = "parallel_batched"
            batch = "ring_buffer"
        transfer = "pipe" if memory == "constrained" else "numpy"
        encode = "ffmpeg" if transfer == "pipe" else "imageio"
    
    # FACTOR 4: Add optimization step
    optimize = "gifsicle" if output_format == "size_critical" else None
    
    return {
        "render": render,
        "batch": batch,
        "transfer": transfer,
        "encode": encode,
        "optimize": optimize
    }
```

---

## Lookup Table (Type A-D Classification)

| Type | Condition | Profile | Expected Time | Memory | Recommendation |
|------|-----------|---------|----------------|--------|-----------------|
| **A (Simple)** | Frames < 20, CPU low, 200MB+ RAM | PIL serial | ~1-2s | ~30 MB | Default for demos |
| **B (Standard)** | Frames 20-100, CPU medium, 100MB+ RAM | imageio batch | ~1-2s | ~50 MB | Production standard |
| **C (Large)** | Frames 100+, CPU high, any RAM | FFMpeg streaming | ~0.5-1s | ~5 MB | Large animations |
| **D (Complex)** | Frames any, CPU bottleneck, 100MB+ RAM | Parallel + Numba | ~0.5-2s | ~50 MB | Complex field ops |

### Decision Tree

```
START
  ├─ Memory < 50 MB available?
  │  └─ YES → Type C (Streaming: FFMpeg)
  │
  ├─ Frames > 50?
  │  └─ YES
  │     ├─ Rendering takes > 200ms per frame?
  │     │  ├─ YES → Type D (Parallel/JIT)
  │     │  └─ NO → Type B (imageio)
  │     └─ NO → Type A (PIL)
  │
  └─ Default: Type B (imageio) [balanced, flexible, reliable]
```

---

## Primitive Composition Rules (Locked)

### RULE 1: RENDER → BATCH → TRANSFER → ENCODE → OPTIMIZE
Path must follow this sequence. Reordering breaks compatibility.

### RULE 2: RENDER Variants are Mutually Exclusive
- serial XOR parallel XOR jit XOR gpu
- Pick one based on computation profile

### RULE 3: BATCH is Optional (Streaming Skip It)
- If TRANSFER(pipe) used, skip BATCH entirely
- Stream directly: RENDER → TRANSFER(pipe) → ENCODE

### RULE 4: TRANSFER Can Skip If Source = Target Container
- RENDER(numpy) → ENCODE(imageio): skip TRANSFER (numpy already in target)
- RENDER(pil) → ENCODE(PIL): skip TRANSFER (PIL already in target)
- RENDER(matplotlib) → TRANSFER(pipe) → ENCODE(ffmpeg): required (different containers)

### RULE 5: OPTIMIZE is Always Optional
- Adds post-processing cost (gifsicle: +0.5-2s)
- Only use if: file size critical AND not already optimized in ENCODE
- Trigger: output_format == "production" OR output_size > threshold

---

## Container Type Matrix

| Primitive | Pillow | NumPy | Matplotlib Fig | Pipe/Stream | GPU |
|-----------|--------|-------|---|---|---|
| RENDER | PIL.Image | NDArray | Figure | BytesIO | CuPy Array |
| BATCH | List[PIL] | List[NDArray] | List[Figure] | Generator | GPU List |
| TRANSFER | Direct copy | asarray | tobuffer | Serialize | cupy.asnumpy |
| ENCODE | PIL.save_all | imageio | FFMpeg | FFMpeg native | OpenCV GPU |
| OPTIMIZE | None | None | None | Pipe options | None |

**Compatibility**: Each primitive must output container type that next primitive accepts

---

## Automatic Type Detection (Election System)

### Election PRIM-1: Render Strategy
**Trigger**: Measure frame_generation_time
- If < 30ms: Continue RENDER(serial)
- If 30-100ms: Consider RENDER(parallel)
- If > 100ms: Activate RENDER(jit) or RENDER(gpu)

**Decision**: `render_type = "jit" if cpu_intensive else ("parallel" if multicore else "serial")`

---

### Election PRIM-2: Batch Strategy
**Trigger**: Measure available_memory
- If < 50MB: Use TRANSFER(pipe), skip BATCH
- If 50-200MB: Use BATCH(list)
- If > 200MB: Use BATCH(list) + RENDER(parallel)

**Decision**: `batch_type = None if memory_constrained else "list"`

---

### Election PRIM-3: Transfer Strategy
**Trigger**: Compare source and target containers
- If same: Skip TRANSFER
- If different + time_critical: Use fastest path
- If different + memory_critical: Use streamed path

**Decision**: `transfer_type = "pipe" if memory_critical else detect_optimal()`

---

### Election PRIM-4: Encode Strategy
**Trigger**: Check format requirement
- If format = "gif": Use PIL or imageio
- If format = "mp4": Use FFMpeg or imageio
- If format = "size_critical": Use FFMpeg + gifsicle

**Decision**: `encode_type = select_by_format(output_format)`

---

### Election PRIM-5: Optimize Strategy
**Trigger**: Check file size and production status
- If file_size > threshold OR production=True: Add OPTIMIZE(gifsicle)
- If already optimized in ENCODE: Skip
- If time_critical: Skip even if size suboptimal

**Decision**: `optimize = "gifsicle" if production and not time_critical else None`

---

## Locking the Framework

### LOCKED DECISIONS (April 1, 2026)

✓ **Primitive 1-5 Architecture**: Immutable. All methods compose these 5.  
✓ **Container Type Matrix**: Locked. Defines compatibility.  
✓ **RULE 1-5 Ordering**: Locked. Sequence is non-negotiable.  
✓ **Type A-D Classification**: Locked. Decision tree is canonical.  
✓ **Universal Identifier Formula**: Locked. CLASSIFY() function defines optimal type.  
✓ **Lookup Table**: Locked. Reference for time/memory expectations.  
✓ **Election System**: Locked. 5 elections capture all optimization decisions.

---

## How to Identify Optimal Method (Universal Process)

1. **Measure Input Profile**:
   - num_frames
   - avg_frame_time_ms
   - available_memory_mb
   - output_format
   - production_grade (bool)

2. **Run CLASSIFY()**:
   ```python
   profile = CLASSIFY(
       scale=categorize_frames(num_frames),
       complexity=categorize_time(avg_frame_time_ms),
       memory_budget=available_memory_mb,
       output_format=output_format
   )
   ```

3. **Get Result**:
   - Render strategy (serial/parallel/jit/gpu)
   - Batch strategy (list/pipe/ring-buffer)
   - Transfer strategy (direct/stream/gpu)
   - Encode strategy (PIL/imageio/FFMpeg)
   - Optimize strategy (none/gifsicle/palette)

4. **Apply Election System**:
   - If any stage shows bottleneck → trigger corresponding election
   - Use decision tree to flip between Types A-D
   - Verify expected time/memory from lookup table

5. **Monitor Execution**:
   - Measure actual time vs. expected
   - If actual > expected by >20%: Profile hotspot
   - If hotspot in RENDER: Activate Numba or parallel
   - If hotspot in ENCODE: Switch to FFMpeg

---

## Summary: Universal Way to Identify Optimization

**Old way**: Pick one method (PIL vs imageio vs FFMpeg) manually  
**New way**: Decompose into 5 primitives, classify input, compose optimal combination

**Keys**:
- Primitives are orthogonal (composable in any valid order)
- Container types enforce compatibility (prevents invalid combinations)
- Classification formula determines optimal composition automatically
- Election system catches performance deviations and adjusts

**Result**: Universal identifier that uniquely maps (input_profile) → (optimal_method_composition)

This means given ANY animation scenario, you can algorithmically determine:
1. Which rendering strategy (serial/parallel/jit/gpu)
2. How to accumulate frames (list/stream/buffer)
3. Which format to output (gif/mp4/webp)
4. Whether to optimize (gifsicle or not)
5. Expected performance (time, memory)

