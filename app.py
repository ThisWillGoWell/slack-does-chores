from flask import Flask, request
from chores import Manger
from slack import Bot

class App:
    app = Flask(__name__)
    manager = Manger(Bot())

    @staticmethod
    @app.route('/api', methods=['POST'])
    def api():
        print(request.form)

    def __init__(self):
        self.app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    App()

