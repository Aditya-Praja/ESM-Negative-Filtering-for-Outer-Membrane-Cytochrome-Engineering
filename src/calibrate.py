"""Phase 4: calibrate threshold on surrogate DMS; derive worst-case FNR with CIs.

For each surrogate (config/surrogates.yaml), running YOUR pipeline (not leaderboard numbers):
  binarize fitness -> apply filter at tau -> FNR(tau) -> sweep tau -> operating curve.
Pick tau: most aggressive tau with FNR < fnr_ceiling on EVERY surrogate (worst case).
Convert LLR to within-protein percentiles before transferring any threshold.
Bootstrap 10,000x: resample SITES (not variants); plus dataset-level bootstrap.
Report each surrogate's N_eff/L next to MtrC's.
Target sentence: "At threshold tau, the filter excludes X% of positions, FNR Y% (95% CI a-b)..."
"""


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
