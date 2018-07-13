import com_image


class ComRI:
    def __init__(self):
        self.command = 0x20

    def test(self, module, OperTime, i):
        es = com_image.ComImage(module)
        try:
            f = open('img' + format(i) + '.raw', 'wb')
        except IOError:
            module.disconnect()
            quit()

        user_id = 0
        flag = 0
        es.do_image(module, user_id, self.command, OperTime, flag, f)
        f.close()

        print ('<< End')
