import requests
import json
import logging

# log requests as they happen
# http_client.HTTPConnection.debuglevel = 1

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

HEADERS = {'Content-Type': 'application/json'}


# Uses tautulli as api backend for plex
class Plex:
    API_KEY: str
    HOST: str

    def __init__(self, config: dict):
        self.API_KEY = config["API_KEY"]
        self.HOST = config["HOST"]

    def get_activity(self) -> dict:
        url = (
            self.HOST +
            "/api/v2?apikey={apikey}&cmd=get_activity&out_type=json").format(
                apikey=self.API_KEY)

        response = requests.get(url, headers=HEADERS)

        return json.loads(response.text)['response']

    def is_active(self, data: dict) -> bool:
        return True if int(data.get('stream_count')) > 0 else False

    def is_plex_idle(self) -> bool:
        active = self.is_active(self.get_activity().get('data'))

        return not active


if not __name__ == "__main__":
    print("plex.py is imported")
#else:
#    env = os.getenv("ENV", ".config")
#    config = []
#    if env == ".config":
#        config = ConfigParser()
#        config.read(".config")
#        config = config["PLEX"]
#
#    plex = Plex(config)
#    print(json.dumps(plex.get_activity(), indent=4))