import os
import re
import threading
import time

from slackclient import *


class Bot(object):
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
    SLEEP_INTERVAL = 1

    class User(object):
        def __init__(self, id, name, real_name, **kwargs):
            self.slack_id = id
            self.name = name
            self.real_name = real_name

    def __init__(self):
        self.commands = {}
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        self.users = {}
        if self.slack_client.rtm_connect(with_team_state=False):
            info = self.slack_client.api_call("auth.test")
            self.bot_id = self.slack_client.api_call("auth.test")["user_id"]
            self._populate_users()
            self.command_thread = threading.Thread(target=self._run_command_reader, daemon=True)
            self.command_thread.start()
            pass
        else:
            print("Connection Failed")

    def _populate_users(self):
        users = self.slack_client.api_call("users.list")
        for u in users['members']:
            user = Bot.User(**u)
            self.users[user.slack_id] = user

    def _run_command_reader(self):
        """
        Run the channel parser
        check if the command exists in the
        :return:
        """
        while True:
            self.parse_events(self.slack_client.rtm_read())
            time.sleep(1)

    def parse_events(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API
            Will run the command thats with those events
        """

        for event in slack_events:
            # check mention
            print("event: " + str(event))
            if event["type"] == "message" and not "subtype" in event:
                self._parse_direct_mention(event['text'], event['channel'])

    def _parse_direct_mention(self, message_text, channel):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(Bot.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        if matches:
            mentioned_id = matches.group(1)
            message = matches.group(2).strip()
            if mentioned_id == self.bot_id:
                self.send_message(message, channel)
                print("Bot mentioned: ", message, 'channel: ', channel)

    def send_message(self, msg, channel):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=msg
        )

    def register_command(self, command, func):
        self.commands[command] = func


if __name__ == '__main__':
    b = Bot()
    while True:
        pass
