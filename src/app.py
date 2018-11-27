import urllib

from flask import Flask, request, Response
from src.chores import Manger
from src.slack import Bot


class App:
    app = Flask(__name__)
    manager = Manger(Bot())

    @staticmethod
    @app.route('/chore/api', methods=['POST'])
    def api():
        data = request.get_data()
        data = urllib.unquote(data).decode('utf8')

        App.app.logger.info(data )
        return Response(status=200)

    def __init__(self):
        self.app.run(host='0.0.0.0', port=8080, debug=True)

