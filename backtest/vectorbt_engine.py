"""Vectorised backtesting - uses VectorBT when available, falls back to pure NumPy."""
import pandas as pd
import numpy as np
from loguru import logger
from strategies.dna import StrategyDNA

try:
    import vectorbt as vbt
    VBT_AVAILABLE = True
except ImportError:
    VBT_AVAILABLE = False
    logger.warning("VectorBT not installed - using NumPy fallback backtester")


class VectorBTEngine:
    def __init__(self, price_data: pd.DataFrame, init_cash: float = 10_000):
        # Normalize column names just in case
        col_map = {c.lower(): c for c in price_data.columns if isinstance(c, str)}
        close_key = col_map.get('close', list(price_data.columns)[3])
        volume_key = col_map.get('volume', list(price_data.columns)[4])
        self.price = price_data[close_key]
        self.volume = price_data[volume_key]
        self.init_cash = init_cash

    def run(self, strategy: StrategyDNA) -> dict:
        entries, exits = self._strategy_to_signals(strategy)
        if VBT_AVAILABLE:
            return self._run_vbt(strategy, entries, exits)
        return self._run_numpy(entries, exits, strategy)

    def _run_vbt(self, strategy: StrategyDNA, entries, exits) -> dict:
        pf = vbt.Portfolio.from_signals(
            self.price, entries, exits,
            init_cash=self.init_cash,
            sl_stop=strategy.risk_params.get('stop_loss', 0.02),
            tp_stop=strategy.risk_params.get('take_profit', 0.04),
            freq='1D'
        )
        return {
            'strategy_id': strategy.id,
            'sharpe': float(pf.sharpe_ratio()),
            'max_drawdown': float(pf.max_drawdown()),
            'total_return': float(pf.total_return()),
            'win_rate': float(pf.trades.win_rate()),
            'total_trades': int(pf.trades.count()),
            'profit_factor': float(pf.trades.profit_factor()),
        }

    def _run_numpy(self, entries: pd.Series, exits: pd.Series, strategy: StrategyDNA) -> dict:
        """Lightweight NumPy fallback - simulates simple long-only strategy."""
        prices = self.price.values
        cash = float(self.init_cash)
        position = 0.0
        equity = []
        trades_pnl: list[float] = []
        entry_price = 0.0

        for i in range(len(prices)):
            if entries.iloc[i] and position == 0:
                position = cash / prices[i]
                entry_price = prices[i]
                cash = 0.0
            elif exits.iloc[i] and position > 0:
                pnl = position * (prices[i] - entry_price)
                trades_pnl.append(pnl)
                cash = position * prices[i]
                position = 0.0
            equity.append(cash + position * prices[i])

        eq = np.array(equity) if equity else np.array([self.init_cash])
        rets = np.diff(eq) / (eq[:-1] + 1e-9)
        sharpe = float((np.mean(rets) / (np.std(rets) + 1e-9)) * np.sqrt(252)) if len(rets) > 1 else 0.0
        peak = np.maximum.accumulate(eq)
        max_dd = float(((eq - peak) / (peak + 1e-9)).min())
        wins = [p for p in trades_pnl if p > 0]
        losses = [p for p in trades_pnl if p <= 0]
        win_rate = len(wins) / len(trades_pnl) if trades_pnl else 0.5
        profit_factor = float(sum(wins) / (abs(sum(losses)) + 1e-9)) if losses else 1.0
        total_return = float((eq[-1] - self.init_cash) / self.init_cash)

        return {
            'strategy_id': strategy.id,
            'sharpe': sharpe,
            'max_drawdown': max_dd,
            'total_return': total_return,
            'win_rate': win_rate,
            'total_trades': len(trades_pnl),
            'profit_factor': profit_factor,
        }

    def _strategy_to_signals(self, strategy: StrategyDNA):
        rsi = self._rsi(self.price)
        if strategy.style == 'smc':
            entries = (rsi < 35) & (self.volume > self.volume.rolling(20).mean() * 1.5)
            exits = rsi > 65
        else:
            fast = int(strategy.parameters.get('fast_window', 10))
            slow = int(strategy.parameters.get('slow_window', 50))
            sma_fast = self.price.rolling(fast).mean()
            sma_slow = self.price.rolling(slow).mean()
            entries = sma_fast > sma_slow
            exits = sma_fast < sma_slow
        return entries.fillna(False), exits.fillna(False)

    @staticmethod
    def _rsi(price: pd.Series, period: int = 14) -> pd.Series:
        d = price.diff()
        g = d.clip(lower=0).rolling(period).mean()
        lo = (-d.clip(upper=0)).rolling(period).mean()
        return 100 - 100 / (1 + g / lo.replace(0, 1e-9))
