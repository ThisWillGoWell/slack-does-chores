import json
import threading

from croniter import croniter
from datetime import datetime, timedelta
from threading import Lock, Thread
from time import sleep

class Manger(object):

    def __init__(self, slack_client):
        self.slack_client = slack_client
        self.chores = {}
        self.users = {}
        self.chore_lock = Lock()
        self._populate()
        self.thread = Thread(target=self.run_alerts, daemon=True)
        self.thread.start()

    def _populate(self):
        with open('config.json') as f:
            config = json.load(f)

        for user_name, user in config['users'].items():
            self.users[user_name] = User(user_name, **user)

        for chore_name, c in config['chores'].items():
            chore = Chore(chore_name, **c)
            self.chores[chore_name] = chore
            chore.assign_user(self.users[chore.assigned_to])

    def run_alerts(self):
        while True:
            self.chore_lock.acquire()
            now = datetime.now()
            for chore in self.chores.values():
                if chore.state == ChoreState.idle():
                    if now > chore.alert_at.get_next(datetime):
                        self.chore_alert(chore)

                if chore.state == ChoreState.alerted():
                    if now > chore.complete_by.get_next(datetime):
                        self.chore_failed(chore)
                    elif datetime.now() > chore.last_alert_at + timedelta(seconds=10):
                        self.chore_alert(chore)
            self.chore_lock.release()
            sleep(1)

    def mark_complete(self, chore_name):
        self.chore_lock.acquire()
        self.chore_complete(self.chores[chore_name])
        self.chore_lock.release()

    def chore_alert(self, chore):
        chore.state = ChoreState.alerted()
        self.slack_client.send_message("hey " + chore.user.name + " do " + chore.title)
        chore.alert()

    def chore_failed(self, chore):
        self.slack_client.send_message("chore failed, better luck next time")
        chore.state = ChoreState.idle()

    def chore_complete(self, chore):
        self.slack_client.send_message("chore " + chore.title + " marked as complete")
        chore.state = ChoreState.idle()


class ChoreState:
    @staticmethod
    def idle():
        return "idle"

    @staticmethod
    def alerted():
        return "alerted"

    @staticmethod
    def complete():
        return "complete"


class Chore(object):
    def __init__(self, name, title, alert_at, complete_by, assigned_to):
        self.state = ChoreState.idle()
        self.name = name
        self.title = title

        self.alert_at = croniter(alert_at)
        self.next_alert = self.alert_at.get_next(datetime)

        self.complete_by = croniter(complete_by)
        self.next_complete = self.complete_by.get_next(datetime)

        self.assigned_to = assigned_to
        self.last_alert_at = datetime.now()
        self.user = None

    def assign_user(self, user):
        self.user = user

    def alert(self):
        self.last_alert_at = datetime.now()
        self.next_alert = self.alert_at.get_next(datetime)

    def complete(self):
        self.next_complete = self.complete_by.get_next(datetime)
        self.state = ChoreState.complete()

    def reset(self):
        self.nex


class User(object):
    def __init__(self, user_name, name, slack_id):
        self.name = name
        self.user_name = user_name
        self.slack_id = slack_id







if __name__ == '__main__':
    populate()
