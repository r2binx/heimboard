import ast
import json
import os
from configparser import ConfigParser
from datetime import datetime
from typing import Dict, List

import requests
from dateutil import parser


class Jelly:
    config: dict
    IGNORED: List[str]
    JELLY_HEADERS = dict

    def __init__(self, config: Dict):
        self.config = config
        self.IGNORED = list(ast.literal_eval(config["IGNORED"]))
        self.JELLY_HEADERS = {
            'X-Emby-Authorization':
            f'Emby Client=idlereporter, Device=heimboard, DeviceId=heimboard, Version=1, Token={config["TOKEN"]}',
            'Content-Type': 'application/json'
        }

    def get_sessions(self) -> List[Dict]:
        try:
            url = self.config["HOST"] + "/Sessions?activeWithinSeconds=300"

            response = requests.get(url, headers=self.JELLY_HEADERS)

            return json.loads(response.text)
        except requests.ConnectionError:
            print("Connection failed")
            return []

    def get_active_sessions(self) -> List[Dict]:
        sessions = []
        for session in self.get_sessions():
            if self.active_session(session):
                sessions.append(session)

        return sessions

    def active_session(self, session: Dict) -> bool:
        last_activity = parser.parse(
            session['LastActivityDate']).replace(tzinfo=None)
        relative_activity = (datetime.utcnow() - last_activity).seconds

        if session['Client'] == 'DLNA' or session['DeviceName'] in self.IGNORED:
            return False
        elif session['IsActive'] and session.get(
                'NowPlayingItem') is None and relative_activity < 2000:
            print(relative_activity)

            return True
        elif session.get('NowPlayingItem') is not None:
            return True
        else:
            return False

    def is_active(self) -> bool:
        playing_paused = []
        active_sessions = self.get_active_sessions()
        for session in active_sessions:

            if session.get('NowPlayingItem') is not None:
                paused = session.get('PlayState').get('IsPaused')
                if paused:
                    playing_paused.append(session)

        return True if len(active_sessions) > 0 else False


if not __name__ == "__main__":
    print("jelly.py is imported")

else:
    env = os.getenv("ENV", ".config")
    config = []
    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["JELLY"]

    jelly = Jelly(config)
    print(json.dumps(jelly.get_active_sessions(), indent=4))
