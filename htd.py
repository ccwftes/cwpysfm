import pysfm
import time


def read_file(module, command, i=0):
    if command == 0x05 or command == 0x08 or command == 0x11:
        data = ''
    elif command == 0x06 or command == 0x80 or command == 0x09 or command == 0x12 or command == 0x81 or command == 0x82\
            or command == 0x07 or command == 0x87 or command == 0x10 or command == 0x13 or command == 0x62:
        try:
            if command == 0x06 or command == 0x80 or command == 0x09 or command == 0x12 or command == 0x81 or command == 0x82:
                f = open('img' + format(i) + '.raw', 'rb')
            elif command == 0x07 or command == 0x87 or command == 0x10 or command == 0x13:
                f = open('template' + format(i) + '.dat', 'rb')
            elif command == 0x62:
                f = open('fw6020.bin', 'rb')
        except IOError:
            module.disconnect()
            quit()
        data = f.read()
        f.close()
    return data


def write_file(module, command, i, data_list):
    if command == 0x89:
        try:
            f = open('temp' + format(i) + '.dat', 'wb')
        except IOError:
            module.disconnect()
            quit()
        for x in data_list[:]:
            f.write(chr(x))
        f.close()
    elif command == 0x15 or command == 0x20 or command == 0x83 or command == 0x84:
        try:
            f = open('temp' + format(i) + '.dat', 'wb')
        except IOError:
            module.disconnect()
            quit()
        for x in data_list[28:]:
            f.write(chr(x))
        f.close()


def print_error(module, OperTime):
    module.read_response_command(OperTime)
    if module.response_command.error == 0x61:
        print('     Success')
    elif module.response_command.error == 0x6A:
        print('     Not match')
    elif module.response_command.error == 0x69:
        print('     Not found')
    elif module.response_command.error == 0x75:
        print('     Unsupported')
    elif module.response_command.error == 0x91:
        print('     Duress finger')
    elif module.response_command.error == 0x6E:
        print('     Exist ID')
    elif module.response_command.error == 0x86:
        print('     Exist finger')
    else:
        if module.response_command.error == 0x63:
            print('     Scan fail')
        elif module.response_command.error == 0x6B:
            print('     Try again')
        elif module.response_command.error == 0x6C:
            print('     Scan timeout')
        elif module.response_command.error == 0x7A:
            print('     Match timeout')
        elif module.response_command.error == 0x90:
            print('     Rejected ID')
        elif module.response_command.error == 0x94:
            print('     Entrance limit')
        elif module.response_command.error == 0xB0:
            print('     Fake detected')
        elif module.response_command.error == 0x76:
            print('     Invalid ID')
        elif module.response_command.error == 0x6D:
            print('     Memory full')
        elif module.response_command.error == 0x72:
            print('     Fingerprint limit')
        module.disconnect()
        quit()


def send_exdtp(module, command, OperTime, data_list, const_data_packet_size):
    data_packet_size = const_data_packet_size
    num_of_packet = len(data_list) / data_packet_size

    if (len(data_list) % data_packet_size) > 0:
        num_of_packet += 1

    sent_len = 0
    print_error(module, OperTime)

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
        print_error(module, OperTime)

        if module.response_command.error is not pysfm.UF_PROTO_RET_DATA_OK:
            break
        sent_len += data_packet_size


def read_exdtp(module, command, OperTime, i):
    data_list = []
    while True:
        print_error(module, OperTime)
        param = module.response_command.param
        size = module.response_command.size
        data_list += module.read_data(size)
        module.read_data(4)
        module.send_command(command, 0, 0, pysfm.UF_PROTO_RET_DATA_OK)
        if ((param >> 16) & 0xFF) is ((param & 0xFF) - 1):
            break

    write_file(module, command, i, data_list)


def do_iv(module, user_id, command, OperTime, i, tt=0):
    data = read_file(module, command, i)
    data_list = []
    for x in data:
        data_list.append(ord(x))

    module.send_command(command, user_id, len(data_list))
    if command == 0x09 or command == 0x10 or command == 0x12 or command == 0x13:
        module.send_data(data)
        module.send_end_packet()
    elif command == 0x81 or command == 0x82:
        const_data_packet_size = 0x1000
        send_exdtp(module, command, OperTime, data_list, const_data_packet_size)
    print_error(module, OperTime)
    if module.response_command.error == 0x62:
        if tt == 1:
            start_time = time.time()
        print_error(module, OperTime)
    if tt == 1:
        final_time = time.time() - start_time
        return final_time


def do_image(module, command, OperTime, i):
    if command == 0x83 or command == 0x84:
        size = 0x1000
    else:
        size = 0
    module.send_command(command, 0, size)
    print_error(module, OperTime)

    if command == 0x83 or command == 0x84:
        if module.response_command.error == 0x62:
            print_error(module, OperTime)
            if module.response_command.error == 0x61:
                read_exdtp(module, command, OperTime, i)
                print_error(module, OperTime)
    elif command == 0x15 or command == 0x20:
        if module.response_command.error == 0x62:
            print_error(module, OperTime)
        if module.response_command.error == 0x61:
            size = module.response_command.size
            data_list = module.read_data(size)
            write_file(module, command, i, data_list)
            module.read_data(1)


def do_delete(module, user_id, command, OperTime, sub_index, flag):
    module.send_command(command, user_id, sub_index, flag)
    print_error(module, OperTime)
    if module.response_command.error == 0x62:
        print_error(module, OperTime)


class ComEnroll:
    def __init__(self, module):
        # module.deactivate_packet_trace()
        self.enroll_mode = 0
        self.enroll_option = 1
        module.send_command(command=0x03, param=0, size=0, flag=0x64)
        print_error(module, 0)
        self.template_size = module.response_command.size

    def print_enroll_mode(self, module):
        print ('Enroll Mode >>')
        module.send_command(command=0x03, param=0, size=0, flag=0x65)
        print_error(module, 0)
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
        # module.activate_packet_trace()

    def select_enroll_option(self, enroll_option):
        if enroll_option == 0x71:           print ('Option : ADD NEW >>')
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

    def do_enroll(self, module, user_id, command, OperTime, i, enroll_option):
        enroll_mode = self.enroll_mode
        data = read_file(module, command, i)
        data_list = []
        for x in data:
            data_list.append(ord(x))

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
            send_exdtp(module, command, OperTime, data_list, const_data_packet_size)
        print_error(module, OperTime)
        if module.response_command.error == 0x62:
            print_error(module, OperTime)
            if command == 0x05 and module.response_command.error == 0x61:
                if enroll_mode == 0x32 or enroll_mode == 0x42:
                    module.send_command(command, user_id, len(data_list), 0x74)
                if enroll_mode == 0x32 or enroll_mode == 0x42 or enroll_mode == 0x31 or enroll_mode == 0x41:
                    print_error(module, OperTime)
                    if module.response_command.error == 0x62:
                        print_error(module, OperTime)


class ComTemplate:
    def __init__(self, module):
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x64)
        print_error(module, 0)
        self.template_size = module.response_command.size

    def do_template(self, module, user_id, command, OperTime, flag, sub_index=0):
        i = 0
        if command == 0x89:
            size = (sub_index << 16) | self.template_size
        else:
            size = 0
        module.send_command(command, user_id, size, flag)
        print_error(module, OperTime)
        if command == 0x89 and module.response_command.error == 0x61:
            count = module.response_command.size
            while i < (count >> 16):
                print_error(module, OperTime)
                param = module.response_command.param
                data_list = module.read_data(self.template_size)
                write_file(module, command, i, data_list)
                module.read_data(4)
                if ((param >> 16) & 0xFF) is ((param & 0xFF) - 1):
                    break
                module.send_command(command, 0, 0, pysfm.UF_PROTO_RET_DATA_OK)
                i = i + 1
        elif command == 0x14 or command == 0x21:
            if module.response_command.error == 0x62:
                print_error(module, OperTime)
            while module.response_command.error == 0x74 or module.response_command.error == 0x61:
                data_list = module.read_data(self.template_size)
                write_file(module, command, i, data_list)
                module.read_data(1)
                if module.response_command.error == 0x61:
                    break
                print_error(module, OperTime)
                i = i+1
