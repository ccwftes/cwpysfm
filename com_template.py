# coding=cp949
import pysfm
import time


class ComTemplate:
    def __init__(self, module):
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x75)
        module.read_response_command()
        self.send_scan_success = module.response_command.size
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x64)
        module.read_response_command()
        self.template_size = module.response_command.size

    def do_template(self, module, user_id, command, OperTime, flag, sub_index=0):
        send_scan_success = self.send_scan_success
        i = 0
        time.sleep(2)
        if command == 0x89:
            size = (sub_index << 16) | self.template_size
        else:
            size = 0
        module.send_command(command, user_id, size, flag)
        module.read_response_command(OperTime)

        if command == 0x89:
            count = module.response_command.size
            if module.response_command.error == 0x61:
                while i < (count >> 16):
                    module.read_response_command(OperTime)
                    param = module.response_command.param
                    data_list = module.read_data(self.template_size)
                    try:
                        f = open('temp' + format(i) + '.dat', 'wb')
                    except IOError:
                        break
                    for x in data_list[:]:
                        f.write(chr(x))
                    f.close()
                    module.read_data(4)
                    if ((param >> 16) & 0xFF) is ((param & 0xFF)-1):
                        break
                    module.send_command(command, 0, 0, pysfm.UF_PROTO_RET_DATA_OK)
                    i = i + 1
            else:
                if module.response_command.error == 0x63:
                    print('     Scan fail')
                elif module.response_command.error == 0x6B:
                    print('     Try again')
                elif module.response_command.error == 0x6C:
                    print('     Scan Timeout')
                elif module.response_command.error == 0x69:
                    print('     Not found')
                elif module.response_command.error == 0x75:
                    print('     Unsupported')
                module.disconnect()
                quit()
        elif command == 0x14:
            while module.response_command.error == 0x74:
                data_list = module.read_data(self.template_size)
                try:
                    f = open('temp' + format(i) + '.dat', 'wb')
                except IOError:
                    break
                for x in data_list[:]:
                    f.write(chr(x))
                f.close()
                module.read_data(1)
                module.read_response_command(OperTime)
                i = i+1
            if module.response_command.error == 0x61:
                data_list = module.read_data(self.template_size)
                try:
                    f = open('temp' + format(i) + '.dat', 'wb')
                except IOError:
                    module.disconnect()
                    quit()
                for x in data_list[:]:
                    f.write(chr(x))
                f.close()
                module.read_data(1)
        elif command == 0x21:
            if send_scan_success == 0x31:
                module.read_response_command(OperTime)
            if module.response_command.error == 0x61:
                data_list = module.read_data(self.template_size)
                try:
                    f = open('temp' + format(i) + '.dat', 'wb')
                except IOError:
                    module.disconnect()
                    quit()
                for x in data_list[:]:
                    f.write(chr(x))
                f.close()
            else:
                if module.response_command.error == 0x63:
                    print('     Scan fail')
                elif module.response_command.error == 0x6B:
                    print('     Try again')
                elif module.response_command.error == 0x6C:
                    print('     Scan Timeout')
                elif module.response_command.error == 0x69:
                    print('     Not found')
                elif module.response_command.error == 0x75:
                    print('     Unsupported')
                module.disconnect()
                quit()
