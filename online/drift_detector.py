"""Drift detection ensemble - uses River when available, falls back to EWMA-based detector."""
from loguru import logger

try:
    from river import drift as river_drift
    # River's available detectors: ADWIN, KSWIN, PageHinkley
    _RIVER_AVAILABLE = True
except ImportError:
    _RIVER_AVAILABLE = False


if _RIVER_AVAILABLE:
    class DriftDetectorEnsemble:
        """Majority-vote ensemble using River (ADWIN, KSWIN, PageHinkley)."""
        def __init__(self):
            self.detectors = {
                'adwin': river_drift.ADWIN(delta=0.002),
                'kswin': river_drift.KSWIN(alpha=0.005),
                'pagehinkley': river_drift.PageHinkley(min_instances=30, delta=0.005),
            }
            self._votes: list[bool] = []

        def update(self, error: float) -> bool:
            votes = 0
            for name, det in self.detectors.items():
                det.update(error)
                if det.drift_detected:
                    votes += 1
                    logger.warning(f'Drift vote from {name}')
            detected = votes >= 2  # majority
            self._votes.append(detected)
            if detected:
                logger.warning('DRIFT CONFIRMED - triggering strategy pool refresh')
            return detected

        @property
        def drift_rate(self) -> float:
            tail = self._votes[-100:]
            return sum(tail) / len(tail) if tail else 0.0

else:
    logger.warning("River not installed - using EWMA-based drift detector fallback")

    class DriftDetectorEnsemble:  # type: ignore[no-redef]
        """EWMA-based drift detector fallback (no River dependency)."""
        def __init__(self, threshold: float = 0.65, window: int = 50):
            self._errors: list[float] = []
            self._threshold = threshold
            self._window = window
            self._votes: list[bool] = []

        def update(self, error: float) -> bool:
            self._errors.append(float(error))
            tail = self._errors[-self._window:]
            weights = [0.9 ** (len(tail) - 1 - i) for i in range(len(tail))]
            ewma = sum(e * w for e, w in zip(tail, weights)) / sum(weights)
            detected = ewma > self._threshold
            self._votes.append(detected)
            if detected:
                logger.warning('DRIFT CONFIRMED (EWMA) - triggering pool refresh')
            return detected

        @property
        def drift_rate(self) -> float:
            tail = self._votes[-100:]
            return sum(tail) / len(tail) if tail else 0.0
