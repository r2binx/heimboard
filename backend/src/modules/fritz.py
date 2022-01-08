from fritzconnection import FritzConnection
from fritzconnection.lib.fritzstatus import FritzStatus
from typing import Dict, Tuple

import os
from configparser import ConfigParser


class Fritz:
    config: Dict
    fbs: FritzStatus
    HOST: str
    USER: str
    PASS: str

    def __init__(self, config: Dict) -> None:
        self.config = config
        self.HOST = config["HOST"]
        self.USER = config["USER"]
        self.PASS = config["PASS"]
        self.fbs = FritzStatus(address=self.HOST,
                               user=self.USER,
                               password=self.PASS,
                               timeout=3.5)

    def get_max_bandwidth(self) -> Tuple[int, int]:
        return self.fbs.max_bit_rate

    def get_current_bandwidth(self) -> Tuple[int, int]:
        return self.fbs.transmission_rate

    def get_external_ip(self) -> Tuple[str, str]:
        return self.fbs.external_ip, self.fbs.external_ipv6


if not __name__ == "__main__":
    print("fritz.py is imported")

# else:
#     env = os.getenv("ENV", ".config")
#     config = []
#     if env == ".config":
#         config = ConfigParser()
#         config.read(".config")
#         config = config["FRITZ"]

#     fritz = Fritz(config)
#     print(fritz.get_max_bandwidth())
#     print(fritz.get_current_bandwidth())
#     print(fritz.get_external_ip())