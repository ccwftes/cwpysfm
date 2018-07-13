# coding=cp949
import pysfm
import time


class ComIdentification:
    def __init__(self, module):
        module.deactivate_packet_trace()
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x75)
        module.read_response_command()
        self.send_scan_success = module.response_command.size
        module.activate_packet_trace()

    def do_identification(self, module, id_range, command, OperTime, data):
        send_scan_success = self.send_scan_success
        data_list = []
        for x in data:
            data_list.append(ord(x))

        module.send_command(command, id_range, len(data_list))
        if command == 0x12 or command == 0x13:
            module.send_data(data)
            module.send_end_packet()
        elif command == 0x81:
            const_data_packet_size = 0x1000
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
            start_time = time.time()
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
                print('     Scan timeout')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x7A:
                print('     Timeout match')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x69:
                print('     Not found')
            elif module.response_command.error == 0x75:
                print('     Unsupported')
            elif module.response_command.error == 0x90:
                print('     Rejected ID')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x91:
                print('     Duress finger')
            elif module.response_command.error == 0x94:
                print('     Entrance limit')
                module.disconnect()
                quit()
            elif module.response_command.error == 0xB0:
                print('     Fake detected')
                module.disconnect()
                quit()
        else:
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
                print('     Scan timeout')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x7A:
                print('     Timeout match')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x69:
                print('     Not found')
            elif module.response_command.error == 0x75:
                print('     Unsupported')
            elif module.response_command.error == 0x90:
                print('     Rejected ID')
                module.disconnect()
                quit()
            elif module.response_command.error == 0x91:
                print('     Duress finger')
            elif module.response_command.error == 0x94:
                print('     Entrance limit')
                module.disconnect()
                quit()
            elif module.response_command.error == 0xB0:
                print('     Fake detected')
                module.disconnect()
                quit()
        final_time = time.time() - start_time
        return final_time
