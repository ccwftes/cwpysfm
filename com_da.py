class ComDA:
    def __init__(self):
        self.command = 0x17

    def test(self, module):
        print ('Start >>')
        module.send_command(self.command)
        module.read_response_command(10000)
        print ('<< End')
