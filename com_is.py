import com_identification


class ComIS:
    def __init__(self):
        self.command = 0x11

    def test(self, module, OperTime):
        es = com_identification.ComIdentification(module)

        id_range = 0
        es.do_identification(module, id_range, self.command, OperTime, '')

        print ('<< End')

