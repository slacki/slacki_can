import unittest
from random import randint

from slacki_can.message import Message, CanMessageRangeError


class MessageTest(unittest.TestCase):
    def test_iteration(self):
        randbytes = self._random_bytes()
        m = Message(0xF1, randbytes, dlc=8)

        i = 0
        for d in m:
            self.assertEqual(d, randbytes[i])
            i += 1

    def test_id_range(self):
        ids = [-1, -100, -0x02, 0x800]
        for id in ids:
            try:
                m = Message(id, self._random_bytes(i=4), dlc=4)
            except Exception as e:
                self.assertIsInstance(e, CanMessageRangeError)

    def _random_bytes(self, i=8):
        b = []
        for x in range(0, i):
            b.append(randint(0, 0xff))

        return bytes(b)

if __name__ == 'main':
    unittest.main()
