import ast
# import os
# from configparser import ConfigParser
from typing import Dict, List, Any

import psutil


class Storage:
    DISKS: List[str]
    MOUNTPOINTS: List[str]

    def __init__(self, config: Dict):
        self.DISKS = list(ast.literal_eval(config['DISKS']))
        self.MOUNTPOINTS = list(ast.literal_eval(config['MOUNTS']))

    def get_usage(self) -> List[Dict[str, Any]]:
        usage = []
        for mount in self.MOUNTPOINTS:
            usage.append({"name": mount, "usage": psutil.disk_usage(mount)._asdict()})

        return usage


if not __name__ == "__main__":
    print("storage.py is imported")

# else:
#    env = os.getenv("ENV", ".config")
#    config = []
#    if env == ".config":
#        config = ConfigParser()
#        config.read(".config")
#        config = config["STORAGE"]
#
#    storage = Storage(config)
#    print(json.dumps(storage.get_usage(), indent=4))
