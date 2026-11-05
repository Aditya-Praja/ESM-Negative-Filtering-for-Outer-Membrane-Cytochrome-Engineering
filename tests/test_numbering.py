"""Regex CXXCH must equal geometric CXXCH. Run in CI. Write this FIRST."""
from pathlib import Path
import pytest
from src import numbering

PROCESSED = Path("data/processed/covariates.parquet")
FASTA = Path("data/raw/Q8EG34.fasta")


def _read_fasta(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">"))


def test_roundtrip():
    for p in (1, 26, 100, 671):
        assert numbering.idx_to_uniprot(numbering.uniprot_to_idx(p)) == p
    for p in (26, 100, 671):
        assert numbering.mature_idx_to_uniprot(numbering.uniprot_to_mature_idx(p)) == p


def test_cxxch_finder_synthetic():
    hits = numbering.find_cxxch("AACAACHAA")
    assert hits == [{"cys1": 3, "cys4": 6, "his5": 7}]


@pytest.mark.skipif(not FASTA.exists(), reason="Q8EG34.fasta not in data/raw")
def test_ten_cxxch_motifs():
    assert len(numbering.find_cxxch(_read_fasta(FASTA))) == 10


@pytest.mark.skipif(not (FASTA.exists() and PROCESSED.exists()), reason="phase3 not run")
def test_regex_matches_geometry():
    import pandas as pd
    df = pd.read_parquet(PROCESSED)
    geo_his = set(df.loc[df["is_proximal_his"], "pos_uniprot"])  # column produced by phase3
    rx_his = {h["his5"] for h in numbering.find_cxxch(_read_fasta(FASTA))}
    assert geo_his == rx_his
