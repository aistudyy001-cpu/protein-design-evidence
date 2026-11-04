# Workflow and module contracts

## Generation and evaluation

Candidate generation and prediction run in separately managed model environments. The project uses model-specific evidence rather than treating all confidence scores as interchangeable.

In the intended Changjiang Cup evaluation branch, ESMFold2 and ipSAE follow the organizer's specified conditions. In the NK2R competition context, AF3 interface screening and experimental agonism are separate stages. Parameters and rules must be checked against current official documentation before a run.

This public repository implements neither official screening branch. It publishes the audit layer described below.

## Included audit modules

### `pdp.metrics.prediction_blocks`

Inputs: a residue PAE matrix in angstroms, pLDDT values normalized to [0, 1], target length and binder length. The chain blocks must be contiguous, target first. This is a ColabDesign-oriented helper rather than a model-agnostic parser.

Outputs: binder mean confidence, both directional cross-chain PAE means and their symmetric mean. PAE remains directional in the individual outputs. No acceptance threshold is assigned.

### `pdp.interface_robustness.scoped_pose_metrics`

Inputs: reference and prediction CA coordinates indexed by chain, plus explicit target fitting positions. Positions are one-based. All selected coordinates must exist and be finite.

Outputs include:

- target CA RMSD after fitting the selected target core;
- binder CA RMSD after that same target fit (pose change);
- binder CA RMSD after fitting the binder to itself (shape change);
- global complex CA RMSD and optional regional diagnostics.

The metrics describe geometry, not affinity, function or conformational free energy. Chain/residue correspondence must be established before using them.

## Candidate portfolio

For future research, candidates should be selected with attention to sequence family, scaffold, epitope and shared failure modes. Additional prediction seeds can diagnose sensitivity, but must not be cherry-picked or pooled across incompatible conditions.

## Public data boundary

The demonstration uses generated coordinate fixtures and synthetic confidence values only. No submitted research sequence, private structure, model weight, access token or machine configuration is required.
