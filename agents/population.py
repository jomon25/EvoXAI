import random, numpy as np
from agents.agent import TradingAgent
from loguru import logger

class AgentPopulation:
    """1000+ agent competitive ecosystem with evolutionary dynamics."""
    def __init__(self, n: int = 1000):
        self.agents = [TradingAgent(i) for i in range(n)]
        self.generation = 0

    def step(self, market_state: dict) -> None:
        crowd_sentiment = np.mean([1 if a.act(market_state, 0) > 0 else -1
                                   for a in self.agents])
        for agent in self.agents:
            position = agent.act(market_state, crowd_sentiment)
            pnl = position * market_state.get('return', 0)
            agent.update_pnl(pnl)

    def evolve(self, elite_ratio: float = 0.2) -> None:
        fitnesses = [a.fitness for a in self.agents]
        top_n = int(len(self.agents) * elite_ratio)
        elite_idx = np.argsort(fitnesses)[::-1][:top_n]
        elites = [self.agents[i] for i in elite_idx]
        
        new_pop = elites.copy()
        while len(new_pop) < len(self.agents):
            parent = random.choice(elites)
            child = TradingAgent(len(new_pop), capital=parent.capital)
            child.dna = {k: v * random.uniform(0.85, 1.15)
                         for k, v in parent.dna.items()}
            new_pop.append(child)
            
        self.agents = new_pop
        self.generation += 1
        logger.info(f'Agent gen {self.generation}: best_fitness={max(fitnesses):.4f}')
