# Active Codebase - April 1, 2026

## Status: CLEAN ENVIRONMENT

Old prototype files archived to `_archive_*` directories.

---

## Core Active Files

### 1. **UNIVERSAL_CONTAINER_RENDERER.py** (Universal framework)
- **Purpose**: Abstract base classes for 7-stage causality pipeline
- **Exports**: 
  - `UniversalResult` - Result wrapper enforcing causality
  - `Stage1_InputValidator` - Abstract validator
  - `Stage2_MetricsCalculator` - Abstract metrics
  - `Stage3_StrategySelector` - Abstract strategy
  - `Stage4_Executor` - Abstract executor
  - `Stage5_Verifier` - Abstract verifier
  - `Stage6_Adapter` - Abstract adapter
  - `Stage7_OutputGenerator` - Abstract output
  - `UniversalContainerOrchestrator` - Orchestrator enforcing causality
- **Implementations included**:
  - ListValidator, ListMetrics, ListStrategy, ListExecutor, ListVerifier, ListAdapter, ListOutputGenerator (for lists)
  - TreeValidator, TreeMetrics, TreeStrategy, TreeExecutor, TreeVerifier, TreeAdapter, TreeOutputGenerator (for trees)
- **Status**: ✓ TESTED

### 2. **REAL_MOLECULAR_GIF_GENERATOR.py** (Molecule-specific implementation)
- **Purpose**: Apply universal 7-stage pipeline to molecular rendering
- **Exports**:
  - `Molecule` - Data class for molecular structure
  - `MoleculeRenderer` - Orchestrator for molecular rendering
  - `UniversalResult` - Inherited from universal framework
- **Stages**:
  - Stage1: InputValidator (validates atoms/bonds)
  - Stage2: MetricsCalculator (spread_factor, density, asymmetry)
  - Stage3: StrategySelector (chooses rotation based on metrics)
  - Stage4: RenderExecutor (generates 20 frames)
  - Stage5: QualityVerifier (checks frame validity)
  - Stage6: QualityAdapter (fixes if needed)
  - Stage7: GIFGenerator (saves to file)
- **Test molecules**: Water, Methane, Benzene, Ammonia, CO2, Ethane, Ethene, Acetylene, Formaldehyde
- **Status**: ✓ TESTED (9 molecules render successfully)

---

## The Universal Pattern

```
ANY CONTAINER (molecule, list, tree, graph, etc.)
  ↓
[VALIDATE] Stage 1: Check input safety
  ↓ (if fails, stop)
[METRICS] Stage 2: Analyze properties
  ↓ (if fails, stop)
[STRATEGY] Stage 3: Choose approach (depends on metrics)
  ↓ (if fails, stop)
[EXECUTE] Stage 4: Apply strategy
  ↓ (if fails, stop)
[VERIFY] Stage 5: Check quality
  ↓ (if fails, stop)
[ADAPT] Stage 6: Fix violations
  ↓ (if fails, stop)
[OUTPUT] Stage 7: Generate final result
  ↓
GUARANTEED QUALITY (through causality enforcement)
```

**Key feature**: Each stage receives previous stage's output as UniversalResult. Failure at any stage stops entire pipeline.

---

## How to Use

### For molecules:
```python
from REAL_MOLECULAR_GIF_GENERATOR import MoleculeRenderer, Molecule

renderer = MoleculeRenderer()
mol = Molecule(name="Water", atoms=[("O", 0,0,0), ("H", 1,0,0), ("H", -0.5, 0.866, 0)], bonds=[(0,1,1.0), (0,2,1.0)])
path, result = renderer.render_molecule_to_gif(mol, frames=20)
```

### For lists:
```python
from UNIVERSAL_CONTAINER_RENDERER import UniversalContainerOrchestrator, ListValidator, ListMetrics, ListStrategy, ListExecutor, ListVerifier, ListAdapter, ListOutputGenerator

orchestrator = UniversalContainerOrchestrator()
result = orchestrator.orchestrate(
    container=[1, 5, 3, 8, 2],
    validator=ListValidator(),
    metrics_calc=ListMetrics(),
    strategy_sel=ListStrategy(),
    executor=ListExecutor(),
    verifier=ListVerifier(),
    adapter=ListAdapter(),
    output_gen=ListOutputGenerator()
)
```

### For trees:
```python
from UNIVERSAL_CONTAINER_RENDERER import UniversalContainerOrchestrator, TreeNode, TreeValidator, TreeMetrics, TreeStrategy, TreeExecutor, TreeVerifier, TreeAdapter, TreeOutputGenerator

tree = TreeNode("A", children=[TreeNode("B"), TreeNode("C")])
orchestrator = UniversalContainerOrchestrator()
result = orchestrator.orchestrate(
    container=tree,
    validator=TreeValidator(),
    metrics_calc=TreeMetrics(),
    strategy_sel=TreeStrategy(),
    executor=TreeExecutor(),
    verifier=TreeVerifier(),
    adapter=TreeAdapter(),
    output_gen=TreeOutputGenerator()
)
```

### For NEW containers:
Just inherit from Stage1-7 abstract classes:
```python
from UNIVERSAL_CONTAINER_RENDERER import Stage1_InputValidator, Stage2_MetricsCalculator, ...

class MyContainerValidator(Stage1_InputValidator):
    def validate(self, container: MyContainer) -> UniversalResult:
        # Your validation logic
        
class MyContainerMetrics(Stage2_MetricsCalculator):
    def calculate_metrics(self, container: MyContainer) -> UniversalResult:
        # Your metrics logic

# ... repeat for all 7 stages ...

result = orchestrator.orchestrate(container, MyValidator(), MyMetrics(), MyStrategy(), ...)
```

---

## Verification

Run tests:
```bash
python UNIVERSAL_CONTAINER_RENDERER.py       # Tests lists and trees
python REAL_MOLECULAR_GIF_GENERATOR.py        # Tests molecules
```

Both should show 7 stages executing with causality enforcement.

---

## No Ambiguity

- Each file has one clear purpose
- Each stage has one clear responsibility
- Each implementation is separated from framework
- Quality guaranteed by architecture, not luck
- Zero second-guessing possible (causality enforced)

---

## Next: Extend to New Containers

Types to implement:
- Graphs (vertices + edges)
- Point clouds (points + distances)
- Networks (nodes + links)
- Collections (items + grouping)
- Time series (values + timestamps)
- Relational databases (tables + keys)

Each takes <50 lines of code (just implement 7 abstract methods).
