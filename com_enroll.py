import pysfm
import time


class ComEnroll:
    def __init__(self, module):
        module.deactivate_packet_trace()
        self.enroll_mode = 0
        self.enroll_option = 1
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x75)
        module.read_response_command()
        self.send_scan_success = module.response_command.size
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x64)
        module.read_response_command()
        self.template_size = module.response_command.size

    def print_enroll_mode(self, module):
        print ('Enroll Mode >>')
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x65)
        module.read_response_command()
        enroll_mode = module.response_command.size

        if enroll_mode == 0x30:
            print ('Current Mode = 1 time')
        elif enroll_mode == 0x31:
            print ('Current Mode = 2 times I')
        elif enroll_mode == 0x32:
            print ('Current Mode = 2 times II')
        elif enroll_mode == 0x41:
            print ('Current Mode = 2 temp I')
        elif enroll_mode == 0x42:
            print ('Current Mode = 2 temp II')

        self.enroll_mode = enroll_mode
        module.activate_packet_trace()

    def select_enroll_mode(self, module):
        enroll_mode = 0
        while enroll_mode != 0x30 and enroll_mode != 0x31 and enroll_mode != 0x32 and enroll_mode != 0x41 and enroll_mode != 0x42:
            print ('Select Enroll Mode: ')
            enroll_mode = input()
            if enroll_mode == 1:
                enroll_mode = 0x30
            elif enroll_mode == 2:
                enroll_mode = 0x31
            elif enroll_mode == 3:
                enroll_mode = 0x32
            elif enroll_mode == 4:
                enroll_mode = 0x41
            elif enroll_mode == 5:
                enroll_mode = 0x42

        module.send_command(command=pysfm.UF_COM_SW, param=0, size=enroll_mode, flag=0x65)
        module.read_response_command()
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x65)
        module.read_response_command()
        enroll_mode = module.response_command.size

        if enroll_mode == 0x30:
            print ('Current Mode = 1 time')
        elif enroll_mode == 0x31:
            print ('Current Mode = 2 times I')
        elif enroll_mode == 0x32:
            print ('Current Mode = 2 times II')
        elif enroll_mode == 0x41:
            print ('Current Mode = 2 temp I')
        elif enroll_mode == 0x42:
            print ('Current Mode = 2 temp II')

        self.enroll_mode = enroll_mode

    def select_enroll_option(self, enroll_option):
        # enroll_option = self.enroll_option
        # while enroll_option != 0x71 and enroll_option != 0x79 and enroll_option != 0x70 and enroll_option != 0x84 and enroll_option != 0x85 and enroll_option != 0x92 and enroll_option != 0x0:
        #     print ('Select Enroll option: ')
        #     enroll_option = input()
        #     if enroll_option == 1:
        #         enroll_option = 0x71
        #     elif enroll_option == 2:
        #         enroll_option = 0x79
        #     elif enroll_option == 3:
        #         enroll_option = 0x70
        #     elif enroll_option == 4:
        #         enroll_option = 0x84
        #     elif enroll_option == 5:
        #         enroll_option = 0x85
        #     elif enroll_option == 6:
        #         enroll_option = 0x92
        #     elif enroll_option == 0:
        #         enroll_option = 0x0

        if enroll_option == 0x71:
            print ('Option : ADD NEW >>')
        elif enroll_option == 0x79:
            print ('Option : AUTO ID >>')
        elif enroll_option == 0x70:
            print ('Option : CHECK ID >>')
        elif enroll_option == 0x84:
            print ('Option : CHECK FINGER >>')
        elif enroll_option == 0x85:
            print ('Option : CHECK FINGER AUTO ID >>')
        elif enroll_option == 0x92:
            print ('Option : ADD DURESS >>')
        elif enroll_option == 0x0:
            print ('Option : NONE >>')

        self.enroll_option = enroll_option

    def do_enroll(self, module, user_id, command, OperTime, data):
        send_scan_success = self.send_scan_success
        enroll_option = self.enroll_option
        enroll_mode = self.enroll_mode
        data_list = []
        for x in data:
            data_list.append(ord(x))

        time.sleep(0.5)
        module.send_command(command, user_id, len(data_list), enroll_option)
        if command == 0x06 or command == 0x07:
            module.send_data(data)
            module.send_end_packet()
        elif command == 0x80 or command == 0x87:
            const_data_packet_size = 0
            if command == 0x80:
                const_data_packet_size = 0x1000
            elif command == 0x87:
                const_data_packet_size = self.template_size
            data_packet_size = const_data_packet_size
            num_of_packet = len(data_list) / data_packet_size

            if (len(data_list) % data_packet_size) > 0:
                num_of_packet += 1

            sent_len = 0
            module.read_response_command(OperTime)

            for l in range(num_of_packet):
                cs = 0
                if (len(data_list) - sent_len) < data_packet_size:
                    data_packet_size = len(data_list) - sent_len

                module.send_command(command, ((l << 16) | num_of_packet), data_packet_size, 0)

                image_data = data_list[(l * const_data_packet_size):(l * const_data_packet_size + data_packet_size)]
                for x in image_data:
                    cs = cs + x
                checksum = [(cs >> 24) & 0xFF, (cs >> 16) & 0xFF, (cs >> 8) & 0xFF, (cs >> 0) & 0xFF]
                module.send_data(image_data)
                checksum.reverse()
                module.send_data(checksum)
                module.read_response_command(OperTime)

                if module.response_command.error is not pysfm.UF_PROTO_RET_DATA_OK:
                    break
                sent_len += data_packet_size
        module.read_response_command(OperTime)
        if send_scan_success == 0x31 and module.response_command.error == 0x62:
            module.read_response_command(OperTime)
            if module.response_command.error == 0x61:
                print('     Success')
                if command == 0x05:
                    if enroll_mode == 0x32 or enroll_mode == 0x42:
                        module.send_command(command, user_id, len(data_list), 0x74)
                    if enroll_mode == 0x32 or enroll_mode == 0x42 or enroll_mode == 0x31 or enroll_mode == 0x41:
                        module.read_response_command(OperTime)
                        if send_scan_success == 0x31 and module.response_command.error == 0x62:
                            module.read_response_command(OperTime)
                            if module.response_command.error == 0x61:
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
                            elif module.response_command.error == 0x6D:
                                print('     Memory full')
                                module.disconnect()
                                quit()
                            elif module.response_command.error == 0x72:
                                print('     Fingerprint limit')
                                module.disconnect()
                                quit()
                            elif module.response_command.error == 0x75:
                                print('     Unsupported')
                            elif module.response_command.error == 0x76:
                                print('     Invalid ID')
                                module.disconnect()
                                quit()
                            elif module.response_command.error == 0x6E:
                                print('     Exist ID')
                            elif module.response_command.error == 0x86:
                                print('     Exist finger')
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
            elif module.response_command.error == 0x6D:
                print('     Memory full')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x72:
                print('     Fingerprint limit')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x75:
                print('     Unsupported')
            elif module.response_command.error == 0x76:
                print('     Invalid ID')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x6E:
                print('     Exist ID')
            elif module.response_command.error == 0x86:
                print('     Exist finger')
        else:
            if module.response_command.error == 0x63:
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
            elif module.response_command.error == 0x6D:
                print('     Memory full')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x72:
                print('     Fingerprint limit')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x75:
                print('     Unsupported')
            elif module.response_command.error == 0x76:
                print('     Invalid ID')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x6E:
                print('     Exist ID')
            elif module.response_command.error == 0x86:
                print('     Exist finger')
            elif module.response_command.error == 0x61:
                print('     Success')
