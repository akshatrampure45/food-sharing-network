"""
Freshness estimation service.

Stubbed for now so the app runs without TensorFlow/OpenCV installed.
Swap `estimate_freshness` for a real model call once ml/freshness_model.py
is trained — keep the same function signature so routers don't need to change.
"""
import random


def estimate_freshness(photo_url: str | None) -> float:
    """Returns a freshness score between 0.0 (spoiled) and 1.0 (fresh)."""
    if not photo_url:
        return 0.75  # neutral default when no photo supplied
    # TODO: replace with ml/freshness_model.py inference (TF/OpenCV)
    return round(random.uniform(0.6, 0.98), 2)
