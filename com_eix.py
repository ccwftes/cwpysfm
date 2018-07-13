import com_enroll


class ComEIX:
    def __init__(self):
        self.command = 0x80

    def test(self, module, OperTime, user_id, enroll_option, i):
        es = com_enroll.ComEnroll(module)

        es.print_enroll_mode(module)
        es.select_enroll_option(enroll_option)

        try:
            f = open('img' + format(i) + '.raw', 'rb')
        except IOError:
            module.disconnect()
            quit()
        data = f.read()
        f.close()

        es.do_enroll(module, user_id, self.command, OperTime, data)

        print ('<< End')
