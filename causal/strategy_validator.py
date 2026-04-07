import pandas as pd, numpy as np
from causal.effect_estimator import CausalEffectEstimator
from strategies.dna import StrategyDNA
from loguru import logger

class StrategyCausalValidator:
    """Rejects strategies with spurious (non-causal) performance."""
    def validate(self, strategy: StrategyDNA, signal_series: pd.Series,
                 price_series: pd.Series, confounders: pd.DataFrame) -> bool:
        future_return = price_series.pct_change().shift(-1)
        
        data = confounders.copy()
        data['signal'] = signal_series.values
        data['future_return'] = future_return.values
        data = data.dropna()
        
        try:
            est = CausalEffectEstimator(data)
            ok = est.is_causal()
            if not ok:
                logger.warning(f'Strategy {strategy.id[:8]} rejected: spurious correlation')
            return ok
        except Exception as e:
            logger.error(f'Causal validation error: {e}')
            return False  # conservative: reject on error
