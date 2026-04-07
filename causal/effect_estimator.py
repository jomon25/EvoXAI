import pandas as pd
from dowhy import CausalModel
from loguru import logger

class CausalEffectEstimator:
    """Estimates causal effect of strategy signal on future return."""
    CONFOUNDERS = ['market_return', 'volatility', 'volume_ratio', 'regime']

    def __init__(self, data: pd.DataFrame, treatment: str = 'signal',
                 outcome: str = 'future_return'):
        self.model = CausalModel(
            data=data,
            treatment=treatment,
            outcome=outcome,
            common_causes=[c for c in self.CONFOUNDERS if c in data.columns]
        )

    def estimate(self) -> float:
        estimand = self.model.identify_effect(proceed_when_unidentifiable=True)
        estimate = self.model.estimate_effect(
            estimand, method_name='backdoor.linear_regression')
        return float(estimate.value)

    def is_causal(self, threshold: float = 0.005) -> bool:
        effect = self.estimate()
        result = abs(effect) > threshold
        logger.info(f'Causal effect={effect:.5f}, is_causal={result}')
        return result
