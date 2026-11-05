#!/bin/bash
#SBATCH --job-name=mtrc-esm-scan
#SBATCH --array=0-5            # one task per checkpoint
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x-%A_%a.out

module load anaconda3 cudatoolkit
conda activate mtrc

python -m src.phase1_esm_scan \
    --config config/filter_v1.yaml \
    --checkpoint-index $SLURM_ARRAY_TASK_ID \
    --out data/interim/esm_scan_${SLURM_ARRAY_TASK_ID}.parquet
