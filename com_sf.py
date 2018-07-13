class ComSW:
    def __init__(self):
        self.command = 0x03

    def test(self, module):
        print ('Start >>')
        p_id = 0x84
        module.send_command(self.command, 0, 0, p_id)

        module.disconnect()
        print ('<< End')
