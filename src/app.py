from flask import Flask, request, Response
from src.chores import Manger
from src.slack import Bot


class App:
    app = Flask(__name__)
    manager = Manger(Bot())

    @staticmethod
    @app.route('/chore/api', methods=['POST'])
    def api():
        print(request.json)
        return Response(status=404)

    def __init__(self):
        self.app.run(host='0.0.0.0', port=8080, debug=True)

