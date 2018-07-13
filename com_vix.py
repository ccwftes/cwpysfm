import com_verification


class ComVIX:
    def __init__(self):
        self.command = 0x82

    def test(self, module, OperTime, user_id, i):
        es = com_verification.ComVerification(module)
        try:
            f = open('img' + format(i) + '.raw', 'rb')
        except IOError:
            module.disconnect()
            quit()
        data = f.read()
        f.close()

        es.do_verification(module, user_id, self.command, OperTime, data)

        print ('<< End')
