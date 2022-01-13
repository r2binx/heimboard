from typing import Dict


class Observer:
    value: Dict

    def __init__(self, observable):
        observable.subscribe(self)

    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'From', observable)
        self.value = kwargs.get('data')
