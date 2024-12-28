from exmo_trading_bot import ExmoTradingBot
from bot_stats_api import BotStatsAPI
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from config import API_KEY, API_SECRET
import atexit


lock = threading.Lock()


def start_bot(bot):
    """Run the bot periodically with APScheduler."""
    scheduler = BackgroundScheduler()

    def safe_trade_once():
        """Thread-safe execution of bot logic."""
        with lock:
            bot.trade_once()

    scheduler.add_job(safe_trade_once, "interval", seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    # Initialize the trading bot
    bot = ExmoTradingBot(
        api_key=API_KEY,
        api_secret=API_SECRET,
        symbol="ETH/USDT",
        quantity=0.01,
        buy_price=3000,
        sell_price=3500,
    )

    # Start the bot in a background thread
    bot_thread = threading.Thread(target=start_bot, args=(bot,))
    bot_thread.daemon = True
    bot_thread.start()

    # Start the Flask API server
    api = BotStatsAPI(bot, lock)
    api.run()
