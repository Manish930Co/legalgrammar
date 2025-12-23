from typing import Set

try:
    from gramformer import Gramformer
    _gf = Gramformer(models=1, use_gpu=False)
except Exception:
    _gf = None

def gf_available() -> bool:
    return _gf is not None

def suggest_rewrites(text: str) -> Set[str]:
    if not _gf:
        return set()
    return _gf.correct(text, max_candidates=3)
