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


class Sabnzbd:
    API_KEY: str
    HOST: str

    def __init__(self, config: dict):
        self.API_KEY = config["API_KEY"]
        self.HOST = config["HOST"]

    def get_queue(self) -> dict:
        url = (self.HOST +
               "/api?mode=queue&limit=5&apikey={apikey}&output=json").format(
                   apikey=self.API_KEY)

        response = requests.get(url, headers=HEADERS)

        return json.loads(response.text)['queue']

    def is_active(self) -> bool:
        return True if self.get_queue().get(
            'status') == "Downloading" else False

    def is_nzb_idle(self) -> bool:
        active = self.is_active()

        return not active


if not __name__ == "__main__":
    print("sabnzbd.py is imported")
#else:
#    env = os.getenv("ENV", ".config")
#    config = []
#    if env == ".config":
#        config = ConfigParser()
#        config.read(".config")
#        config = config["NZB"]
#
#    nzb = Sabnzbd(config)
#    print(json.dumps(nzb.get_queue(), indent=4))