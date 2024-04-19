class Reminder:
    params: dict = dict()
    message: str = ''
    period: str = ''

    def __repr__(self):
        return f'params: {self.params} message: {self.message} period: {self.period}'