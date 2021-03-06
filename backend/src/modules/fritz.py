import asyncio
from typing import Dict, Tuple

from fritzconnection.lib.fritzstatus import FritzStatus

# import os
# from configparser import ConfigParser
from src.util.observable import Observable
from src.util.observer import Observer


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


class FritzStats(Observable):
    refresh: bool = False
    task: asyncio.Task

    def __init__(self, fritz: Fritz) -> None:
        super().__init__()
        self.fritz = fritz

    def subscribe(self, observer: Observer):
        if len(self._observers) == 0:
            self.start()
        super().subscribe(observer)

    def unsubscribe(self, observer: Observer):
        super().unsubscribe(observer)
        if len(self._observers) == 0:
            self.stop()

    def start(self):
        print('Starting fritz stats')
        self.refresh = True
        self.task = asyncio.create_task(self.refresh_stats_periodically())

    def stop(self):
        print('Stopping fritz stats')
        self.refresh = False
        self.task.cancel()

    def get_fritz_data(self) -> Dict[str, int]:
        return {
            "in":
                self.fritz.get_current_bandwidth()[1],
            "out":
                self.fritz.get_current_bandwidth()[0]
        }

    async def refresh_stats_periodically(self, rate: int = 1):
        while self.refresh:
            self.notify_observers(data=self.get_fritz_data())
            await asyncio.sleep(rate)


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
