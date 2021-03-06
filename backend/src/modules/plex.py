import json
from typing import Dict

import requests

HEADERS = {'Content-Type': 'application/json'}


# Uses tautulli as api backend for plex
class Plex:
    API_KEY: str
    HOST: str

    def __init__(self, config: Dict):
        self.API_KEY = config["API_KEY"]
        self.HOST = config["HOST"]

    def get_activity(self) -> Dict:
        url = (
            self.HOST +
            "/api/v2?apikey={apikey}&cmd=get_activity&out_type=json").format(
                apikey=self.API_KEY)

        response = requests.get(url, headers=HEADERS)

        return json.loads(response.text)['response']

    def is_active(self) -> bool:
        data = self.get_activity().get('data')
        return True if int(data.get('stream_count')) > 0 else False


if not __name__ == "__main__":
    print("plex.py is imported")

# else:
#    env = os.getenv("ENV", ".config")
#    config = []
#    if env == ".config":
#        config = ConfigParser()
#        config.read(".config")
#        config = config["PLEX"]
#
#    plex = Plex(config)
#    print(json.dumps(plex.get_activity(), indent=4))
