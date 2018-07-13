class ComDA:
    def __init__(self):
        self.command = 0x16

    def test(self, module):
        print ('Start >>')
        user_id = 1
        sub_index = 1
        flag = 0x70
        module.send_command(self.command, user_id, sub_index, flag)
        module.read_response_command(10000)
        print ('<< End')
