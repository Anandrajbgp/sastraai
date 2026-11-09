import hashlib
import numpy as np

def get_embedding(text: str, dim: int = 384) -> list:
    hasher = hashlib.sha256(text.encode("utf-8"))
    digest = hasher.digest()
    np.random.seed(int.from_bytes(digest[:4], "big"))
    vec = np.random.randn(dim).astype(float)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()
