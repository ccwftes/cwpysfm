import com_template


class ComRT:
    def __init__(self):
        self.command = 0x14

    def test(self, module):
        es = com_template.ComTemplate(module)

        print ('Start >>')
        module.send_command(command=0x03, param=0, size=0, flag=0x62)
        module.read_response_command()
        OperTime = module.response_command.size + 3
        print ('Start >> ' '%X' % OperTime)
        OperTime = OperTime - 0x30
        print ('Operation Timeout = ' '%d' % OperTime)

        user_id = 1
        flag = 0
        sub_index = 0
        es.do_template(module, user_id, self.command, OperTime, flag, sub_index)

        module.disconnect()
        print ('<< End')
