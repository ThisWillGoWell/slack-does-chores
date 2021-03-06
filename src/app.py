import json
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
        try:
            form_json = json.loads(request.form["payload"])
            App.app.logger.info(str(form_json))
            App.manager.button_response(form_json)
        except KeyError:
            App.manager.button_response(request.get_json())
        return Response(status=200)

    def __init__(self):
        self.app.run(host='0.0.0.0', port=8080, debug=True)

