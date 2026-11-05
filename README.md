# Mtrc-Filter

**A calibrated ESM-based negative filter for engineering the outer-membrane decaheme cytochrome MtrC.**

*Shewanella oneidensis* MR-1 · UniProt [Q8EG34](https://www.uniprot.org/uniprotkb/Q8EG34) · PDB [4LM8](https://www.rcsb.org/structure/4LM8)

---

## Overview

MtrC is a 671-residue surface lipoprotein that carries electrons from the cell to minerals, flavins and
partner cytochromes through ten covalently bound hemes. Engineering it as a biosensor component requires
knowing which residues can be mutated. This project builds a per-residue filter that combines
protein language model scores, alignment-based conservation, and cofactor geometry from the crystal
structure, and reports its false-negative rate calibrated on surrogate deep mutational scanning datasets.

The output is a per-position allowed alphabet for MtrC, one mask per design mechanism, that can be passed
directly to a de novo design tool (LigandMPNN).

**Headline result** _(fill in once complete)_:

> At threshold τ, the filter excludes **__%** of positions with an estimated false-negative rate of
> **__%** (95% CI __–__%), calibrated on **__** surrogate datasets.

![Graphical abstract](reports/figures/graphical_abstract.png)
*Figure 0. Graphical abstract (placeholder).*

---

## Table of contents

1. [Background](#background)
2. [Methods](#methods)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Results](#results)
6. [Limitations](#limitations)
7. [Handwritten notes](#handwritten-notes)
8. [Repository structure](#repository-structure)
9. [References](#references)
10. [Citation, license, contact](#citation-license-contact)

---

## Background

### Extracellular electron transfer in *S. oneidensis*
_Short summary: the Mtr conduit, why MtrC is the terminal cytochrome, and why an electrode behaves like a mineral._

![Mtr pathway](reports/figures/f1_mtr_pathway.png)
*Figure 1. Mtr pathway from the quinol pool to the electrode.*

### c-type cytochrome chemistry
_CXXCH attachment, bis-His axial coordination, determinants of reduction potential, Marcus-theory limits on tuning._

### MtrC architecture
_Four domains, crossed heme chains, the conserved CX₈C disulfide, five Ca²⁺ sites, lipoprotein N-terminus._

![MtrC structure](reports/figures/f2_mtrc_structure.png)
*Figure 2. 4LM8 colored by domain, with hemes and Ca²⁺ shown.*

### Why a protein language model needs checking here
_Narrow family, heavy cofactor burden, conservation is not the same as engineerability, relevant cytochrome P450 precedent._

### Design mechanisms considered
_Loop grafting, second-shell redox tuning, interface engineering, allosteric gating. This project targets **second-shell redox tuning**._

---

## Methods

### Target and numbering
UniProt numbering is the canonical key throughout. The mature chain (26–671) is the primary scoring
target and the precursor (1–671) is a sensitivity check. All index conversion lives in `src/numbering.py`.

### Language model scoring
Masked-marginal scoring with an ensemble of the five ESM-1v checkpoints, plus ESM-2 650M as an
architecturally distinct second opinion. Per-site mean, standard deviation across seeds, and
cross-architecture disagreement are recorded. Negative scores mean deleterious.

### Is ESM reliable on this family?
Family depth (N_eff/L, θ = 0.8) from a jackhmmer alignment, and pseudo-perplexity of MtrC against a
length-matched null set of random bacterial proteins. These determine how much weight the language model
receives.

### Alignment-based baselines
Sequence-weighted column entropy, GEMME, a shuffled-sequence control, and an RSA-only predictor. Gap
frequency per column gives an insertion-tolerance signal that ESM cannot provide.

### Structure features and chemistry mask
From 4LM8: relative solvent accessibility with and without hemes, distances to heme Fe, porphyrin,
propionates and Ca²⁺, secondary structure, and domain. Axial ligands are extracted from Fe–N geometry,
not annotation. CXXCH cysteines and histidines, distal histidines, Ca²⁺ coordination shells, and the
signal peptide are hard-masked.

### Residual decomposition
ESM site tolerance is regressed on structural covariates only (OLS, with a GAM if residuals curve).
The residual separates structural constraint from functional constraint: large negative residuals mark
sites conserved beyond what burial and cofactor proximity explain.

### Calibration
The filter is treated as a binary screen and tuned against false negatives. The threshold is derived
from surrogate DMS datasets run through this exact pipeline, pooled by worst case, with site-level and
dataset-level bootstrap confidence intervals.

### Pre-registration
Thresholds, mask definitions and surrogate datasets are fixed in `config/filter_v1.yaml`, committed and
tagged before any candidate list is generated. Later changes go in a new tagged config and both are
reported.

| Date | Config tag | Commit | Notes |
|------|-----------|--------|-------|
|      | filter-v1 |        |       |

---

## Installation

```bash
git clone <repo-url> mtrc-filter && cd mtrc-filter

conda create -n mtrc python=3.11 -c conda-forge -y
conda activate mtrc

conda install -c conda-forge -c bioconda -y \
    numpy pandas pyarrow scipy statsmodels scikit-learn pygam \
    matplotlib seaborn tqdm pyyaml pytest biopython hmmer dssp

pip install torch --index-url https://download.pytorch.org/whl/cu121   # match your CUDA version
pip install fair-esm freesasa
```

Pre-download model weights once, to shared storage, so array jobs do not each download them:

```bash
export TORCH_HOME=/path/to/shared/torch_cache
python -c "import esm; [getattr(esm.pretrained, n)() for n in \
  ['esm1v_t33_650M_UR90S_1','esm1v_t33_650M_UR90S_2','esm1v_t33_650M_UR90S_3',\
   'esm1v_t33_650M_UR90S_4','esm1v_t33_650M_UR90S_5','esm2_t33_650M_UR50D']]"
```

**Data** (place in `data/raw/`): `4LM8.cif`, `Q8EG34.fasta`, `uniref90.fasta`, OmcA (Q8EG33, 4LMH) and
MtrF (3PMQ) files, the null-protein set, and the ProteinGym surrogate datasets.


**Verify:**
```bash
python -c "import torch, esm; print(torch.__version__)"
jackhmmer -h | head -2 && mkdssp --version
pytest -q
```

---

## Usage

```bash
# 1. Pre-register
git add config && git commit -m "pre-register filter v1" && git tag filter-v1

# 2. Tests first
pytest -q

# 3. Run the pipeline stages (see src/ for each entry point)
python -m src.phase0_diagnostics
sbatch slurm/esm_scan.sbatch
python -m src.phase3_chem_mask
python -m src.phase2_residual
python -m src.phase4_calibrate
python -m src.phase5_alphabet
```

**Output:** `data/processed/allowed_alphabet.parquet`

| Column | Meaning |
|--------|---------|
| `pos_uniprot` | Canonical position |
| `wt` | Wild-type residue |
| `allowed` | Substitutions surviving the filter |
| `class` | `hard_off` / `conditional` / `free` |
| `llr_mean`, `llr_sd` | ESM ensemble mean and spread |
| `residual` | Structural-regression residual (large negative = functional target) |
| `mask_reason` | Rule that excluded the site, if any |
| `gap_freq` | Insertion tolerance (loop grafting) |

A LigandMPNN per-position bias file is written alongside it.

---

## Results

### Is the language model reliable on this family?

| Protein | Length | N_eff | N_eff/L | Pseudo-perplexity | Percentile vs null |
|---------|--------|-------|---------|-------------------|--------------------|
| MtrC | | | | | |
| OmcA | | | | | |
| MtrF | | | | | |

![Perplexity vs null](reports/figures/f4_ppl_null.png)
*Figure 3. MtrC pseudo-perplexity against the null distribution.*

### Structural versus functional constraint

![Residual plot](reports/figures/f6_residual.png)
*Figure 4. Regression residual against residue position, colored by domain, with chemistry-mask
positions marked and known functional regions shaded.*

![Residual on structure](reports/figures/f7_residual_structure.png)
*Figure 5. Residual mapped onto 4LM8 (blue to red).*

### Recovery of the chemistry mask by ESM alone

| Mask class | n | Fraction recovered |
|------------|---|--------------------|
| CXXCH cysteines | | |
| CXXCH histidines | | |
| Distal histidines | | |
| Ca²⁺ coordination | | |

### Calibration

| Surrogate | Length | N_eff/L | FNR at τ | 95% CI |
|-----------|--------|---------|----------|--------|
|           |        |         |          |        |
| **Worst case** | | | | |

![Operating curve](reports/figures/f8_operating_curve.png)
*Figure 6. False-negative rate against fraction of positions excluded, per surrogate.*

### Comparison with baselines and controls

| Method | Result | Notes |
|--------|--------|-------|
| ESM ensemble | | |
| Column entropy | | |
| GEMME | | |
| RSA only | | |
| Shuffled-sequence ESM | | |
| Random sites | | |
| Cross-homolog (OmcA, MtrF) | | |
| Literature mutants (CX₈C) | | |

### Discussion
_What worked, what did not, and how the filter should be weighted when used._

---

## Limitations

- Scoring is single-site; any multi-mutant design must be rescored.
- ESM cannot score insertions. Gap frequency is used for loop grafting instead.
- Log-likelihoods are not millivolts. Candidate shifts need electrostatics calculations.
- Maturation (Ccm), lipidation and trafficking failures are invisible to the filter and look like misfolding at the electrode.
- Tuning one heme changes the driving force for two transfer steps, so neighbouring steps must be evaluated.
- Calibration transfers from surrogate proteins and assumes they resemble MtrC.

---

## Handwritten notes


---

## Repository structure

```
mtrc-filter/
  config/        pre-registered configs and surrogate list
  data/          raw, msa, interim, processed (gitignored)
  src/           numbering.py, config.py, pipeline modules
  tests/         numbering and known-mutant checks
  slurm/         batch scripts
  notes/         handwritten/
  reports/       figures/
  logs/
```

---

## References

1. Clarke et al. (2011). Structure of a bacterial cell surface decaheme electron conduit. *PNAS* 108:9384–9389.
2. Edwards et al. (2015). Redox linked flavin sites in extracellular decaheme proteins involved in microbe-mineral electron transfer. *Sci Rep* 5:11677.
3. Meier et al. (2021). Language models enable zero-shot prediction of the effects of mutations on protein function. *NeurIPS*.
4. Xu, Samori, Nayar & Altman (2026). Homology-based variant-effect predictors break down on cytochrome P450 pharmacogenes. *bioRxiv*.
5. Notin et al. (2023). ProteinGym. *NeurIPS*.
6. Tien et al. (2013). Maximum allowed solvent accessibilities of residues in proteins. *PLoS ONE*.
7. Marcus & Sutin (1985). Electron transfers in chemistry and biology. *BBA* 811:265.
8. ESM repository: github.com/facebookresearch/esm
9. HMMER user guide (jackhmmer).
