import com_enroll


class ComES:
    def __init__(self):
        self.command = 0x05

    def test(self, module, OperTime, user_id, enroll_option):
        es = com_enroll.ComEnroll(module)

        es.print_enroll_mode(module)
        es.select_enroll_option(enroll_option)

        es.do_enroll(module, user_id, self.command, OperTime, '')

        print ('<< End')

