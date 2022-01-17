class Observer:
    def __init__(self, observable):
        observable.subscribe(self)
        self.value = None

    def notify(self, observable, *args, **kwargs):
        self.value = kwargs.get('data')
