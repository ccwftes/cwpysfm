class ComSR:
    def __init__(self):
        self.command = 0x03

    def test(self, module, p_id):
        print ('Start >>')
        module.send_command(self.command, 0, 0, p_id)
        module.read_response_command()
        print ('<< End')
