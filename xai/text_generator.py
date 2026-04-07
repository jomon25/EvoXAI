class ExplanationToText:
    @staticmethod
    def generate(contributions: list[tuple], decision: str, confidence: float) -> str:
        """Converts feature contributions to human-readable explanation."""
        sorted_c = sorted(contributions, key=lambda x: abs(x[1]), reverse=True)
        parts = []
        for name, val in sorted_c[:3]:
            direction = 'elevated' if val > 0 else 'suppressed'
            parts.append(f'{name} {direction} (weight {abs(val):.2f})')
            
        text = f'{decision} signal: primary driver is {parts[0]}'
        if len(parts) > 1:
            text += f'; supported by {parts[1]}'
        if len(parts) > 2:
            text += f' and {parts[2]}'
        text += f'. Model confidence: {confidence:.0%}.'
        return text
