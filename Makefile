.PHONY: test phase0 scan
test:
	pytest -q
phase0:
	python -m src.phase0_diagnostics
scan:
	sbatch slurm/esm_scan.sbatch
