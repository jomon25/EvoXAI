"""Parallel backtester - uses Ray when available, falls back to serial execution."""
import pandas as pd
import numpy as np
from loguru import logger
from strategies.dna import StrategyDNA
from backtest.vectorbt_engine import VectorBTEngine

try:
    import ray
    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False
    logger.warning("Ray not installed - using serial backtest execution (pip install ray to enable parallel)")


class ParallelBacktester:
    def __init__(self, data: pd.DataFrame, n_workers: int = 8):
        self.data = data
        self.n = n_workers
        self._ray_mode = False

        if RAY_AVAILABLE:
            try:
                ray.init(ignore_reinit_error=True, num_cpus=n_workers)
                self._ray_mode = True
                logger.info(f"Parallel backtester: {n_workers} Ray workers")
            except Exception as e:
                logger.warning(f"Ray init failed ({e}) - falling back to serial mode")
        else:
            logger.info("Parallel backtester: serial mode (Ray not installed)")

    def _run_serial(self, strategies: list) -> list:
        engine = VectorBTEngine(self.data)
        results = [engine.run(s) for s in strategies]
        logger.success(f"Serial backtested {len(results)} strategies")
        return results

    def run(self, strategies: list) -> list:
        if not self._ray_mode:
            return self._run_serial(strategies)

        @ray.remote
        def _worker(data, strat_batch):
            eng = VectorBTEngine(data)
            return [eng.run(s) for s in strat_batch]

        batches = [strategies[i::self.n] for i in range(self.n)]
        futures = [_worker.remote(self.data, b) for b in batches if b]
        results = []
        for r in ray.get(futures):
            results.extend(r)
        logger.success(f"Backtested {len(results)} strategies (parallel)")
        return results

    def shutdown(self) -> None:
        if self._ray_mode and RAY_AVAILABLE:
            ray.shutdown()

