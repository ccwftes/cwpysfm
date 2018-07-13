import com_identification


class ComIIX:
    def __init__(self):
        self.command = 0x81

    def test(self, module, OperTime, i):
        es = com_identification.ComIdentification(module)
        try:
            f = open('img' + format(i) + '.raw', 'rb')
        except IOError:
            module.disconnect()
            quit()
        data = f.read()
        f.close()
        id_range = 0
        es.do_identification(module, id_range, self.command, OperTime, data)

        print ('<< End')

