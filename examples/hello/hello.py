from venom import venom

class NormalPrinter:
    def write(self, text):
        print(text)

class UpperPrinter:
    def write(self, text):
        print(text.upper())

@venom.inject('printer.prefix')
class PrefixPrinter:
    def __init__(self, prefix):
        self.prefix = prefix

    def write(self, text):
        for line in text.split('\n'):
            print(self.prefix, line)

###############################

@venom.inject('hello.author', recipient='hello.recipient')
class HelloSayer:
    def __init__(self, author, recipient=None):
        self.author = author
        self.recipient = recipient

    @venom.inject(None, None, 'hello.output')
    def say_hello(self, message, stream):
        if self.recipient is not None:
            stream.write("Dear %s," % self.recipient)
        stream.write(message)
        stream.write("  -- %s" % self.author)

################################

@venom.with_definitions({
    'hello.author': 'Ann',
    'hello.recipient': 'Bob',
})
def main():
    message = "All work and no play\nmakes Jack a dull boy.\nHave a good day!"
    sayer = HelloSayer()

    with venom.define('hello.output', NormalPrinter()):
        sayer.say_hello(message)

    print("---")
    with venom.define('hello.output', UpperPrinter()):
        sayer.say_hello(message)


    print("---")
    with venom.define('hello.output', PrefixPrinter('> ')):
        sayer.say_hello(message)



if __name__ == '__main__': main()
