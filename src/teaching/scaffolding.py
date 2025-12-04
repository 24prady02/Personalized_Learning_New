"""
Scaffolding Manager - Implements graduated support
Based on Vygotsky's Zone of Proximal Development
"""

from typing import Dict, List, Optional
import random


class ScaffoldingManager:
    """
    Manages scaffolding (support) that is gradually removed as student learns
    
    Scaffolding Levels:
    5 - Maximum: Code templates, step-by-step, full solutions
    4 - High: Partial templates, detailed hints, examples
    3 - Medium: Structure guidance, hints on request
    2 - Low: Minimal hints, must attempt first
    1 - Minimal: Only if stuck for extended time
    0 - None: Independent work
    """
    
    def __init__(self, config: Dict):
        self.config = config
    
    def get_scaffolding_level(self, mastery: float, attempts: int) -> int:
        """Determine appropriate scaffolding based on mastery"""
        if mastery < 0.2 or attempts == 0:
            return 5  # Maximum support for beginners
        elif mastery < 0.4:
            return 4
        elif mastery < 0.6:
            return 3
        elif mastery < 0.8:
            return 2
        else:
            return 0  # Independent work for advanced




















