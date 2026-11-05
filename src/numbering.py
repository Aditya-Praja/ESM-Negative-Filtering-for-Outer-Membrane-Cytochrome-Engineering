"""Single source of truth for residue indices.

Four systems are in play: UniProt (1-671, CANONICAL), PDB author numbering in 4LM8,
zero-indexed Python arrays, and MSA column indices. Nothing else in the repo does
index arithmetic inline -- import from here.
"""
from __future__ import annotations
import re

UNIPROT_LEN = 671
MATURE_START, MATURE_END = 26, 671   # 4LM8 covers UniProt 26-671
SIGNAL_PEPTIDE = (1, 25)

CXXCH_RE = re.compile(r"(?=(C..CH))")   # lookahead: catches overlapping motifs


# --- UniProt <-> zero-indexed arrays -----------------------------------------
def uniprot_to_idx(pos: int, start: int = 1) -> int:
    """UniProt position -> 0-based index into a sequence beginning at UniProt `start`."""
    i = pos - start
    if i < 0:
        raise ValueError(f"UniProt {pos} precedes sequence start {start}")
    return i


def idx_to_uniprot(idx: int, start: int = 1) -> int:
    return idx + start


def mature_idx_to_uniprot(idx: int) -> int:
    return idx_to_uniprot(idx, start=MATURE_START)


def uniprot_to_mature_idx(pos: int) -> int:
    return uniprot_to_idx(pos, start=MATURE_START)


# --- PDB author numbering <-> UniProt -----------------------------------------
def build_pdb_to_uniprot(pdb_seq_by_resnum: dict[int, str], uniprot_seq: str) -> dict[int, int]:
    """Map PDB author resnum -> UniProt position by explicit sequence alignment.

    Do NOT assume a constant offset. Verify empirically, then assert.
    TODO: implement (e.g. Bio.Align.PairwiseAligner on modelled residues; fail
    loudly on any mismatch; report residues missing from the model).
    """
    raise NotImplementedError


# --- sequence motifs -----------------------------------------------------------
def find_cxxch(seq: str, start: int = 1) -> list[dict]:
    """CXXCH motifs by regex. Returns UniProt positions of Cys1, Cys4, His5."""
    hits = []
    for m in CXXCH_RE.finditer(seq):
        i = m.start()
        hits.append({
            "cys1": idx_to_uniprot(i, start),
            "cys4": idx_to_uniprot(i + 3, start),
            "his5": idx_to_uniprot(i + 4, start),
        })
    return hits


def find_cx8c(seq: str, start: int = 1) -> list[tuple[int, int]]:
    """CX8C candidate pairs by regex (sequence-level only; confirm by SG-SG geometry)."""
    return [(idx_to_uniprot(m.start(), start), idx_to_uniprot(m.start() + 9, start))
            for m in re.finditer(r"(?=(C.{8}C))", seq)]
