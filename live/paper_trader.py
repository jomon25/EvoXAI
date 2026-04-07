import asyncio, os
from loguru import logger

class PaperTrader:
    """Connects to Alpaca paper trading API."""
    def __init__(self):
        import alpaca_trade_api as tradeapi
        self.api = tradeapi.REST(
            os.getenv('ALPACA_KEY'), os.getenv('ALPACA_SECRET'),
            base_url='https://paper-api.alpaca.markets'
        )

    def get_account(self) -> dict:
        acct = self.api.get_account()
        return {'equity': float(acct.equity), 'cash': float(acct.cash)}

    def submit_order(self, symbol: str, qty: float, side: str) -> str:
        try:
            order = self.api.submit_order(
                symbol=symbol, qty=qty, side=side,
                type='market', time_in_force='gtc'
            )
            logger.info(f'Order submitted: {side} {qty} {symbol} -> {order.id}')
            return order.id
        except Exception as e:
            logger.error(f'Order failed: {e}')
            return ''
