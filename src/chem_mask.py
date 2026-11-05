"""Phase 3: deterministic geometry from 4LM8 -> hard-off mask.

Per residue: d_fe, d_porph, d_prop, d_ca (min heavy-atom distances);
rsa_holo, rsa_apo (waters excluded, Ca included), rsa_apo - rsa_holo.
Axial ligands: His N-eps2/N-delta1 or Met S-delta within 2.6 A of Fe.
ASSERT exactly 2 axial ligands per heme (fail loudly); 10 hemes; 5 Ca.
Fe-Fe distances for true spatial heme order (not sequence order).
Cross-check: geometric CXXCH His == regex CXXCH His (tests/test_numbering.py).
Output: data/processed/covariates.parquet (one row per residue, UniProt-keyed).
"""


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
