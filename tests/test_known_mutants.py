"""Held-out validation: CX8C cysteines and all CXXCH cysteines must be hard-off.

Derive residue numbers from STRUCTURE (disulfide SG-SG < ~2.3 A), assert, and only
THEN compare against Edwards et al. 2015. Do not hard-code numbers from the paper
before running the filter.
"""
from pathlib import Path
import pytest

ALPHABET = Path("data/processed/allowed_alphabet.parquet")
pytestmark = pytest.mark.skipif(not ALPHABET.exists(), reason="phase5 not run")


def test_cxxch_cysteines_hard_off():
    # TODO: CXXCH Cys positions from phase3 geometry output -> assert class == "hard_off"
    raise NotImplementedError


def test_cx8c_cysteines_hard_off():
    # TODO: disulfide Cys pair from 4LM8 SG-SG geometry (not the paper) -> assert hard_off
    raise NotImplementedError
