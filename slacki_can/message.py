class Message(object):
    def __init__(self, message_id, data, dlc=None):
        if not isinstance(message_id, int):
            raise CanMessageRangeError('Message ID must be an int')
        if message_id not in range(0, 0x7ff + 1):
            raise CanMessageRangeError(
                'Message ID must be in range of <0, 2047>')
        self.message_id = message_id

        if dlc is not None:
            if dlc not in range(0, 8 + 1):
                raise CanMessageRangeError(
                    'DLC parameter must be in range of <0, 8>')
            self.dlc = dlc
        else:
            self.dlc = len(data)

        self.data = data[:self.dlc]

    def __str__(self):
        s = ''
        for b in self.data:
            s += str(b)

        return s

    def __iter__(self):
        length = len(self.data)
        i = 0
        while i < length:
            yield self.data[i]
            i += 1


class CanMessageRangeError(Exception):
    pass
