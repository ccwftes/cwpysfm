class ComSW:
    def __init__(self):
        self.command = 0x01

    def test(self, module, p_val, p_id):
        print ('Start >>')
        module.send_command(self.command, 0, p_val, p_id)
        module.read_response_command()

        print ('<< End')
