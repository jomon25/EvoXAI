"""Quick single-cycle smoke test for EvoXAI orchestrator."""
import asyncio, sys
sys.path.insert(0, '.')
from orchestrator.main import EvoXAIOrchestrator

async def test_run():
    orch = EvoXAIOrchestrator()
    print("--- Initialising EvoXAI ---")
    await orch.initialise()
    print("--- Running one cycle (BTC-USD) ---")
    results = await orch.run_cycle(["BTC-USD"])
    print("--- Cycle Results ---")
    for sym, r in results.items():
        print(f"  Symbol : {sym}")
        print(f"  Regime : {r['regime']}")
        print(f"  Best ID: {r['best_strategy_id']}")
        print(f"  Evo Gen: {r['evolution_gen']}")
        print(f"  Explain: {r['explanation']}")
    print("--- SUCCESS: orchestrator is working ---")

asyncio.run(test_run())
