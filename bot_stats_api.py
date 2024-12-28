from flask import Flask, jsonify, request


class BotStatsAPI:
    def __init__(self, bot, lock):
        self.bot = bot
        self.lock = lock
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/stats", methods=["GET"])
        def get_stats():
            """Return bot statistics as JSON"""
            with self.lock:
                return jsonify({
                    "current_price": self.bot.current_price,
                    "last_buy_price": self.bot.last_buy_price,
                    "last_sell_price": self.bot.last_sell_price,
                    "status": self.bot.status,
                })

        @self.app.route("/set", methods=["GET"])
        def set_price():
            """
            Set sell and buy prices
            URL example: http://127.0.0.1:5000/set?sell=3600.11&buy=3100.22
            """
            sell = request.args.get('sell')
            buy = request.args.get('buy')
            if sell:
                self.bot.sell_price = float(sell)
            if buy:
                self.bot.buy_price = float(buy)
            with self.lock:
                return jsonify({
                    "current_sell_price": self.bot.sell_price,
                    "current_but_price": self.bot.buy_price,
                })

    def run(self):
        """Run the Flask server."""
        self.app.run(host="0.0.0.0", port=5000, threaded=True)
