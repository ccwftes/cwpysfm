import com_identification


class ComIT:
    def __init__(self):
        self.command = 0x13

    def test(self, module, OperTime, i):
        es = com_identification.ComIdentification(module)
        try:
            f = open('template' + format(i) + '.dat', 'rb')
        except IOError:
            module.disconnect()
            quit()
        data = f.read()
        f.close()
        id_range = 0
        es.do_identification(module, id_range, self.command, OperTime, data)

        print ('<< End')

