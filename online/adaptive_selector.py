from online.drift_detector import DriftDetectorEnsemble
from strategies.style_router import StyleRouter
from loguru import logger

class AdaptiveStrategySelector:
    """Switches active strategy pool when drift is detected."""
    def __init__(self, pool_size: int = 10):
        self.drift_detector = DriftDetectorEnsemble()
        self.router = StyleRouter()
        self.active_pool = self.router.generate_batch(pool_size)
        self.pool_size = pool_size

    def update_and_select(self, error: float, regime: str) -> object:
        if self.drift_detector.update(error):
            # Refresh pool, bias towards regime-appropriate styles
            style_map = {
                'Bull Trend': 'swing', 'Bear Trend': 'swing',
                'Ranging': 'snr', 'High Volatility': 'scalping'
            }
            preferred = style_map.get(regime)
            self.active_pool = self.router.generate_batch(self.pool_size, preferred)
            logger.info(f'Pool refreshed for regime={regime}, style={preferred}')
            
        return self.active_pool
