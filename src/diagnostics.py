"""Phase 0: does ESM know this protein, and how deep is the family? (never skipped)

Outputs (-> reports/phase0.json):
  ppl_percentile : MtrC pseudo-perplexity percentile vs ~300 length-matched null proteins
  neff_per_l     : per homolog (MtrC, OmcA, MtrF); theta = 0.8 weights
  per-position perplexity -> data/interim/ppl_per_pos.parquet
Record the decision (ESM leads vs mask leads) in the report.

TODO:
  - jackhmmer on MATURE sequence only; check final profile length vs query (drift)
  - filter: coverage >= 0.70; columns > 0.30 gaps excluded from conservation (keep raw gap stats)
  - pseudo-perplexity with the identical pipeline used in phase 1
"""
from src import config


def main():
    cfg = config.load()
    raise NotImplementedError


if __name__ == "__main__":
    main()
