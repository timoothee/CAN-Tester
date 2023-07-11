
class Test_Module():
    def __init__(self):
        ...

    def negate_payload (self, payload):
        self.paylod_lenght = len(payload)
        self.negated_payload = int(payload, 16) ^ 0xffffffffffffffff
        return (hex(self.negated_payload)[-self.paylod_lenght:])

    def increment_payload(self, payload):
        ...

    def decrement_payload(self, payload):
        ...

    def echo(self, payload):
        ...