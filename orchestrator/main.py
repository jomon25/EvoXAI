"""EvoXAI main orchestration loop."""
import asyncio, numpy as np, yfinance as yf
from loguru import logger

from strategies.style_router import StyleRouter
from backtest.parallel_runner import ParallelBacktester
from evolution.engine import EvolutionEngine
from online.adaptive_selector import AdaptiveStrategySelector
from agents.population import AgentPopulation
from xai.text_generator import ExplanationToText
from regime.regime_detector import RegimeDetector
from features.feature_engineer import FeatureEngineer

class EvoXAIOrchestrator:
    def __init__(self):
        self.router = StyleRouter()
        self.evolution = EvolutionEngine(pop_size=200)
        self.selector = AdaptiveStrategySelector(pool_size=20)
        self.agent_pop = AgentPopulation(n=500)
        self.explainer = ExplanationToText()
        self.regime_det = RegimeDetector()
        self.feat_eng = FeatureEngineer()
        self._initialised = False

    async def initialise(self) -> None:
        logger.info('Initialising EvoXAI...')
        data = yf.download('BTC-USD', period='2y', interval='1d')
        df = self.feat_eng.add_indicators(data)
        
        rets = df['returns'].dropna().values
        vols = df['volume'].dropna().values[:len(rets)]
        self.regime_det.fit(rets, vols)
        
        self.evolution.initialise(self.router.generate, n=200)
        self._initialised = True
        logger.success('EvoXAI initialised')

    async def run_cycle(self, symbols: list[str] | None = None) -> dict:
        symbols = symbols or ['BTC-USD']
        results = {}
        for symbol in symbols:
            data = yf.download(symbol, period='60d', interval='1h')
            df = self.feat_eng.add_indicators(data)
            rets = df['returns'].dropna().values
            vols = df['volume'].dropna().values[:len(rets)]
            
            # 1. Detect regime
            regime_id, regime_name, probs = self.regime_det.predict(rets[-100:], vols[-100:])
            logger.info(f'{symbol}: regime={regime_name} ({probs[regime_id]:.0%})')
            
            # 2. Select strategy pool (drift-aware)
            error = float(np.random.binomial(1, 0.1)) # replace with real trade error
            pool = self.selector.update_and_select(error, regime_name)
            
            # 3. Evolve population
            dummy_results = [{'strategy_id': s.id, 'sharpe': np.random.uniform(-1,2),
                              'max_drawdown': np.random.uniform(0,0.3),
                              'win_rate': np.random.uniform(0.4,0.6)} for s in pool]
            self.evolution.evolve(dummy_results)
            
            # 4. Multi-agent step
            market_state = {'momentum': rets[-1], 'vol_ratio': vols[-1]/vols[-20:].mean(),
                            'return': float(rets[-1])}
            self.agent_pop.step(market_state)
            
            # 5. Generate explanation for best strategy
            best = self.evolution.population[0]
            contrib = [('RSI', 0.45), ('Volume', 0.30), ('ATR', 0.15)]
            expl = self.explainer.generate(contrib, 'BUY', 0.82)
            logger.info(f'Explanation: {expl}')
            
            results[symbol] = {'regime': regime_name, 'explanation': expl,
                               'best_strategy_id': best.id[:8],
                               'evolution_gen': self.evolution.generation}
        return results

    async def run_forever(self, interval_s: int = 60) -> None:
        if not self._initialised:
            await self.initialise()
        while True:
            try:
                res = await self.run_cycle()
                logger.success(f'Cycle complete: {res}')
            except Exception as e:
                logger.error(f'Cycle error: {e}')
            await asyncio.sleep(interval_s)

if __name__ == '__main__':
    asyncio.run(EvoXAIOrchestrator().run_forever(interval_s=30))
