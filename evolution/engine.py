"""NSGA-II Pareto-optimal genetic evolution for trading strategies."""
import random, numpy as np
from loguru import logger
from strategies.dna import StrategyDNA

class EvolutionEngine:
    def __init__(self, pop_size=100, elite_ratio=0.1, mutation_rate=0.3):
        self.pop_size = pop_size
        self.elite_ratio = elite_ratio
        self.mutation_rate = mutation_rate
        self.population: list[StrategyDNA] = []
        self.generation = 0
        self.history: list[dict] = []

    # --- Initialisation ---
    def initialise(self, generator_fn, n: int | None = None) -> None:
        self.population = [generator_fn() for _ in range(n or self.pop_size)]
        logger.info(f'Initialised population: {len(self.population)} strategies')

    # --- Tournament selection ---
    def _tournament(self, k: int = 3) -> StrategyDNA:
        contestants = random.sample(self.population, k)
        return max(contestants, key=lambda s: s.fitness)

    # --- Uniform crossover (same style) ---
    def crossover(self, p1: StrategyDNA, p2: StrategyDNA) -> StrategyDNA:
        if p1.style != p2.style:
            return random.choice([p1, p2])
            
        child = StrategyDNA(style=p1.style, parent_ids=[p1.id, p2.id],
                            generation=self.generation + 1)
                            
        for k in set(p1.parameters) | set(p2.parameters):
            child.parameters[k] = random.choice([
                p1.parameters.get(k), p2.parameters.get(k)])
                
        combined = list(set(p1.entry_conditions + p2.entry_conditions))
        child.entry_conditions = random.sample(combined, min(3, len(combined)))
        
        child.risk_params = {k: (p1.risk_params.get(k, 0) + p2.risk_params.get(k, 0)) / 2
                             for k in p1.risk_params}
        return child

    # --- Style-aware mutation ---
    def mutate(self, s: StrategyDNA) -> StrategyDNA:
        if random.random() > self.mutation_rate:
            return s
        for k in s.parameters:
            s.parameters[k] *= random.uniform(0.8, 1.2)
        s.risk_params['risk_percent'] = max(0.001,
            s.risk_params['risk_percent'] * random.uniform(0.85, 1.15))
        if random.random() < 0.15 and s.entry_conditions:
            s.entry_conditions.pop(random.randrange(len(s.entry_conditions)))
        return s

    # --- NSGA-II Pareto ranking (multi-objective) ---
    def pareto_rank(self, results: list[dict]) -> list[float]:
        n = len(results)
        scores = np.zeros(n)
        for i in range(n):
            dominated = 0
            for j in range(n):
                if i == j: continue
                if (results[j]['sharpe'] >= results[i]['sharpe'] and
                    results[j]['max_drawdown'] <= results[i]['max_drawdown'] and
                    results[j]['win_rate'] >= results[i]['win_rate']):
                    dominated += 1
            scores[i] = 1.0 / (1 + dominated)
        return scores.tolist()

    # --- Full generation step ---
    def evolve(self, results: list[dict]) -> None:
        # Assign fitness from backtest results
        id_to_result = {r['strategy_id']: r for r in results}
        scores = self.pareto_rank(results)
        for strat, score in zip(self.population, scores):
            strat.fitness = score
            
        elite_n = int(self.pop_size * self.elite_ratio)
        self.population.sort(key=lambda s: s.fitness, reverse=True)
        elites = self.population[:elite_n]
        next_gen = elites.copy()
        
        while len(next_gen) < self.pop_size:
            p1, p2 = self._tournament(), self._tournament()
            child = self.crossover(p1, p2)
            child = self.mutate(child)
            next_gen.append(child)
            
        self.population = next_gen[:self.pop_size]
        self.generation += 1
        best = self.population[0]
        logger.info(f'Gen {self.generation}: best fitness={best.fitness:.4f}')
        self.history.append({'gen': self.generation, 'best': best.fitness})
