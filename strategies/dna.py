"""Core Strategy DNA - the genome of a trading strategy."""
from dataclasses import dataclass, field
from typing import List, Dict
import uuid, json

@dataclass
class StrategyDNA:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    style: str = 'smc'
    timeframe: str = '1h'
    entry_conditions: List[str] = field(default_factory=list)
    exit_conditions: List[str] = field(default_factory=list)
    filters: List[str] = field(default_factory=list)
    parameters: Dict[str, float] = field(default_factory=dict)
    risk_params: Dict[str, float] = field(default_factory=lambda: {
        'risk_percent': 0.01, 'rr_ratio': 2.0, 'max_positions': 3})
    parent_ids: List[str] = field(default_factory=list)
    generation: int = 0
    fitness: float = 0.0
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
        
    @classmethod
    def from_json(cls, s: str) -> 'StrategyDNA':
        return cls(**json.loads(s))
