
class Test_Module():
    def __init__(self):
        ...

    def negate_payload(self, payload):
        self.paylod_lenght = len(payload)
        self.negated_payload = int(payload, 16) ^ 0xffffffffffffffff
        return (hex(self.negated_payload)[-self.paylod_lenght:])

    def increment_payload(self, payload):
        payload_lenght = len(payload)
        number = int(payload, 16) + 1
        return (hex(number)[-payload_lenght:])

    def decrement_payload(self, payload):
        payload_lenght = len(payload)
        number = int(payload, 16) - 1
        return (hex(number)[-payload_lenght:])

    def echo(self, payload):
        return payload