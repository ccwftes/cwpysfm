class ComLTX:
    def __init__(self):
        self.command = 0x86

    def test(self, module):
        print ('Start >>')
        module.send_command(self.command)
        module.read_response_command()
        templates_count = module.response_command.param
        data_size = module.response_command.size
        print ('Templates count : %d  Data size : %d' % (templates_count, data_size))

        module.read_response_command()
        for x in range(templates_count):
            module.read_data(8)

        module.disconnect()
        print ('<< End')
