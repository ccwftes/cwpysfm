# coding=cp949
import pysfm
import time


class ComImage:
    def __init__(self, module):
        module.deactivate_packet_trace()
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x75)
        module.read_response_command()
        self.send_scan_success = module.response_command.size
        module.activate_packet_trace()

    def do_image(self, module, user_id, command, OperTime, flag, f):
        send_scan_success = self.send_scan_success
        if command == 0x83 or command == 0x84:
            size = 0x1000
        else:
            size = 0
        module.send_command(command, user_id, size, flag)
        module.read_response_command(OperTime)

        if command == 0x84:
            if module.response_command.error == 0x61:
                data_list = []
                while True:
                    module.read_response_command(OperTime)
                    param = module.response_command.param
                    size = module.response_command.size
                    data_list += module.read_data(size)
                    module.read_data(4)
                    module.send_command(command, 0, 0, pysfm.UF_PROTO_RET_DATA_OK)
                    if ((param >> 16) & 0xFF) is ((param & 0xFF) - 1):
                        break

                for x in data_list[28:]:
                    f.write(chr(x))
                module.read_response_command(OperTime)
                print('     Success')
            elif module.response_command.error == 0x63:
                print('     Scan fail')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x6B:
                print('     Try again')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x6C:
                print('     Scan Timeout')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x69:
                print('     Not found')
            elif module.response_command.error == 0x75:
                print('     Unsupported')
        elif command == 0x20:
            if module.response_command.error == 0x61:
                size = module.response_command.size
                data_list = module.read_data(size)

                for x in data_list[28:]:
                    f.write(chr(x))
        elif command == 0x15:
            if send_scan_success == 0x31:
                module.read_response_command(OperTime)
            if module.response_command.error == 0x61:
                size = module.response_command.size
                data_list = module.read_data(size)

                for x in data_list[28:]:
                    f.write(chr(x))
                module.read_data(1)
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
        elif command == 0x83:
            if send_scan_success == 0x31 and module.response_command.error == 0x62:
                module.read_response_command(OperTime)
                if module.response_command.error == 0x61:
                    data_list = []
                    while True:
                        module.read_response_command(OperTime)
                        param = module.response_command.param
                        size = module.response_command.size
                        data_list += module.read_data(size)
                        module.read_data(4)
                        module.send_command(command, 0, 0, pysfm.UF_PROTO_RET_DATA_OK)
                        if ((param >> 16) & 0xFF) is ((param & 0xFF) - 1):
                            break

                    for x in data_list[28:]:
                        f.write(chr(x))
                    print('     Success')
                elif module.response_command.error == 0x63:
                    print('     Scan fail')
                    module.disconnect()
                    quit()
                elif module.response_command.error == 0x6B:
                    print('     Try again')
                    module.disconnect()
                    quit()
                elif module.response_command.error == 0x6C:
                    print('     Scan Timeout')
                    module.disconnect()
                    quit()
                elif module.response_command.error == 0x69:
                    print('     Not found')
                elif module.response_command.error == 0x75:
                    print('     Unsupported')
            elif module.response_command.error == 0x63:
                print('     Scan fail')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x6B:
                print('     Try again')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x6C:
                print('     Scan Timeout')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x69:
                print('     Not found')
            elif module.response_command.error == 0x75:
                print('     Unsupported')
