class ComRS:
    def __init__(self):
        self.command = 0xD0

    def test(self, module):
        print ('Start >>')
        module.send_command(self.command)
        module.read_response_command()
        if module.response_command.error == 0x61:
            print('     Success')
        print ('<< End')
