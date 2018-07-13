import com_verification


class ComVS:
    def __init__(self):
        self.command = 0x08

    def test(self, module, OperTime, user_id):
        es = com_verification.ComVerification(module)

        es.do_verification(module, user_id, self.command, OperTime, '')

        print ('<< End')

