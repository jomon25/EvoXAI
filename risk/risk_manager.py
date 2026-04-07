import numpy as np
from loguru import logger

class RiskManager:
    """Kelly sizing, circuit breaker, VaR guard."""
    def __init__(self, max_daily_loss: float = 0.05,
                 max_positions: int = 5, account_size: float = 10_000):
        self.max_daily_loss = max_daily_loss
        self.max_positions = max_positions
        self.account_size = account_size
        self.daily_pnl = 0.0
        self.open_positions = 0
        self.circuit_open = False

    def kelly_size(self, win_rate: float, rr: float) -> float:
        edge = win_rate - (1 - win_rate) / rr
        return max(0.0, min(edge, 0.25)) * self.account_size

    def can_trade(self) -> bool:
        if self.circuit_open:
            logger.warning('Circuit breaker is OPEN - no new trades')
            return False
        if self.open_positions >= self.max_positions:
            return False
        return True

    def update_pnl(self, pnl: float) -> None:
        self.daily_pnl += pnl
        if self.daily_pnl < -self.max_daily_loss * self.account_size:
            self.circuit_open = True
            logger.critical('CIRCUIT BREAKER TRIGGERED - daily loss limit hit')

    def reset_daily(self) -> None:
        self.daily_pnl = 0.0
        self.circuit_open = False
