import pytest
from strategies.dna import StrategyDNA
from strategies.generators.smc import SMCGenerator
from evolution.engine import EvolutionEngine

def test_smc_generator_output():
    gen = SMCGenerator()
    dna = gen.generate()
    assert dna.style == 'smc'
    assert 0 < dna.risk_params['risk_percent'] < 0.1
    assert dna.risk_params['rr_ratio'] > 1.0
    assert len(dna.entry_conditions) >= 1

def test_evolution_crossover():
    gen = SMCGenerator()
    p1, p2 = gen.generate(), gen.generate()
    eng = EvolutionEngine()
    child = eng.crossover(p1, p2)
    assert child.style == 'smc'
    assert child.parent_ids == [p1.id, p2.id]

def test_evolution_generation():
    eng = EvolutionEngine(pop_size=10)
    gen = SMCGenerator()
    eng.initialise(gen.generate, n=10)
    dummy = [{'strategy_id': s.id, 'sharpe': 1.0, 'max_drawdown': 0.1,
              'win_rate': 0.55} for s in eng.population]
    eng.evolve(dummy)
    assert eng.generation == 1
    assert len(eng.population) == 10
