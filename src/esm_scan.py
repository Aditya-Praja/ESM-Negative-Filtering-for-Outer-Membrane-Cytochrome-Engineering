"""Phase 1: L x 20 masked-marginal tolerance tensor, one parquet per checkpoint.

Usage: python -m src.phase1_esm_scan --config config/filter_v1.yaml \
           --checkpoint-index 0 --out data/interim/esm_scan_0.parquet

Contract:
  score = log p(mt | masked at i) - log p(wt | masked at i); negative = deleterious.
  model.eval() ALWAYS. Assert len(seq) <= max_len and that no wrapper clipped.
  Log the sequence length the model actually received.
  Index with src.numbering only; emit pos_uniprot.
"""
import argparse
from src import config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(config.DEFAULT))
    ap.add_argument("--checkpoint-index", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cfg = config.load(args.config)
    config.assert_config_committed(args.config)
    ckpt = cfg["esm"]["checkpoints"][args.checkpoint_index]
    # TODO: load ckpt, model.eval(), loop masked positions, write parquet
    raise NotImplementedError(f"scan with {ckpt}")


if __name__ == "__main__":
    main()
