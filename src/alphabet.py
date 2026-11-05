"""Phase 5: emit the per-position allowed alphabet, one mask per mechanism.

Output (data/processed/allowed_alphabet.parquet):
  pos_uniprot:int, wt:str, allowed:list[str], class:{hard_off,conditional,free},
  llr_mean:float, llr_sd:float, residual:float, mask_reason:str, gap_freq:float
Also emit LigandMPNN per-position bias file alongside it.
"""


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
