# Research status and claim boundaries

Snapshot date: 2026-11-04.

## Problem

Protein binder pipelines can produce plausible structures with high confidence while retaining errors in chain identity, geometry, biological context or prediction conditions. The project makes those distinctions explicit before selecting candidates for experimental evaluation.

## Research contexts

1. **NK2R nanobody design:** investigate VHH candidates for ligand-independent receptor activation. The internal final candidate record contains computational hypotheses, not demonstrated agonists. Neither receptor contact nor an active-state template proves activation.
2. **Nanobody/minibinder target selection:** evaluate the fit between available design methods, target constructs, experimental objectives and competition screening. Target recommendations remain conditional on actual candidate quality and experimental context.
3. **Evaluation methodology:** retain input provenance, separate prediction profiles and inspect binder pose independently of binder fold.

## What is verifiable here

The public audit functions can be read, executed and tested. Extracted modules are accompanied by byte-level hashes. Synthetic examples illustrate their intended behavior without publishing confidential candidates.

The public snapshot does not include the private run archive. Historical GPU execution, unpublished candidate performance or full-pipeline reproducibility cannot be independently verified from this repository alone.

## Planned work

- Adapt ESMFold2 structural outputs and PAE to a versioned ipSAE evaluation profile.
- Record target-only MSA inputs and exact model/scoring parameters for competition-specific comparison.
- Add independently reviewed adapters and biological-context checks before expanding candidate generation.
- Connect selected computational hypotheses to appropriate binding and functional experiments when available.

These items describe a research roadmap. They are not completed capabilities of this release.

## Validation levels

| Level | What it supports |
| --- | --- |
| Script runs | Engineering execution |
| Synthetic test passes | Behavior for a specified fixture |
| Structure/geometry supports a hypothesis | Computational evidence under stated conditions |
| Binding experiment | Interaction under the measured assay conditions |
| Functional experiment | Activity in the tested biological system |

No level is automatically equivalent to the next. This repository claims the first two levels for its included demonstration and tests only.
