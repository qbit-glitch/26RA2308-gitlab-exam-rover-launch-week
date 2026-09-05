"""Threshold obstacle detector for the camera scores."""

THRESHOLD = 0.40


def detect(scores, threshold=THRESHOLD):
    """Return the indexes of the scores that are at or above the threshold."""
    return [i for i, s in enumerate(scores) if s >= threshold]
