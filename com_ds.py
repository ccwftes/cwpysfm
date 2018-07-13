import com_delete


class ComDS:
    def __init__(self):
        self.command = 0x1E

    def test(self, module):
        es = com_delete.ComDelete(module)

        print ('Start >>')
        module.send_command(command=0x03, param=0, size=0, flag=0x62)
        module.read_response_command()
        OperTime = module.response_command.size + 3
        print ('Start >> ' '%X' % OperTime)
        OperTime = OperTime - 0x30
        print ('Operation Timeout = ' '%d' % OperTime)

        i = 0
        while i < 10:
            id_range = 0
            es.do_delete(module, id_range, self.command, OperTime)
            i = i + 1

        module.disconnect()
        print ('<< End')
