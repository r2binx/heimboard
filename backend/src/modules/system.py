import asyncio

import psutil

from src.util.observable import Observable
from src.util.observer import Observer


class SystemStats(Observable):
    refresh: bool = False
    task: asyncio.Task

    def subscribe(self, observer: Observer):
        if len(self._observers) == 0:
            self.start()
        super().subscribe(observer)

    def unsubscribe(self, observer: Observer):
        super().unsubscribe(observer)
        if len(self._observers) == 0:
            self.stop()

    def start(self):
        print('Starting system stats')
        self.refresh = True
        self.task = asyncio.create_task(self.refresh_stats_periodically())

    def stop(self):
        print('Stopping system stats')
        self.refresh = False
        self.task.cancel()

    async def refresh_stats_periodically(self, rate: int = 1):
        while self.refresh:
            self.notify_observers(data=get_system_stats())
            await asyncio.sleep(rate)


def get_system_stats():
    cpu_pct = psutil.cpu_percent(interval=0.1)
    total, available, used, *_ = psutil.virtual_memory()
    netio = psutil.net_io_counters(pernic=True)
    return {
        "cpu": cpu_pct,
        "net": {
            "in": netio["enp5s0"].bytes_recv,
            "out": netio["enp5s0"].bytes_sent
        },
        "memory": {
            "total": total,
            "used": used,
            "free": available
        }
    }
