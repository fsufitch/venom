import unittest, io
from venom import venom
from unittest.mock import call, MagicMock

import hello

class TestHelloSayer(unittest.TestCase):
    @venom.with_definitions({
        'hello.author': 'XXX',
        'hello.recipient': 'YYY',
    })
    def run(self, *args, **kwargs):
        # Amend test running with DI definitions
        super().run(*args, **kwargs)

    def test_init_value_injection(self):
        h = hello.HelloSayer()
        self.assertEqual(h.author, 'XXX')
        self.assertEqual(h.recipient, 'YYY')

    def test_writer_injection(self):
        h = hello.HelloSayer()
        output = MagicMock()
        with venom.define('hello.output', output):
            h.say_hello("foo bar")
            output.write.assert_has_calls([
                call('Dear YYY,'),
                call('foo bar'),
                call('  -- XXX')
            ])

if __name__ == '__main__': unittest.main()
