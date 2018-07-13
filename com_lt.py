class ComLT:
    def __init__(self):
        self.command = 0x18

    def test(self, module):
        print ('Start >>')
        module.send_command(self.command)
        module.read_response_command()
        templates_count = module.response_command.param
        data_size = module.response_command.size
        print ('Templates count : %d  Data size : %d' % (templates_count, data_size))
        module.read_data(data_size)
        module.disconnect()
        print ('<< End')
