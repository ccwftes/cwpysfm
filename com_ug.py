class ComUG:
    def __init__(self):
        self.command = 0x62

    def test(self, module):
        print ('Start >>')
        f = open('fw6020.bin', 'rb')
        data = f.read()
        data_list = []

        for x in data:
            data_list.append(ord(x))

        f.close()

        data_size = len(data_list)
        const_data_packet_size = 0x1000
        data_packet_size = const_data_packet_size
        num_of_packet = data_size / data_packet_size

        if (data_size % data_packet_size) > 0:
            num_of_packet += 1

        sent_len = 0
        module.send_command(self.command, 0, data_size)
        module.read_response_command()

        # module.deactivate_packet_trace()
        for i in range(num_of_packet):
            cs = 0
            if (data_size - sent_len) < data_packet_size:
                data_packet_size = data_size - sent_len

            module.send_command(self.command, ((i << 16) | num_of_packet), data_packet_size, 0)

            fw_data = data_list[(i * const_data_packet_size):(i * const_data_packet_size + data_packet_size)]
            module.send_data(fw_data)
            for x in fw_data:
                cs = cs + x
            checksum_data = [(cs >> 24) & 0xFF, (cs >> 16) & 0xFF, (cs >> 8) & 0xFF, (cs >> 0) & 0xFF]
            checksum_data.reverse()
            module.send_data(checksum_data)
            module.read_response_command()
            if module.response_command.error is not 0x83:
                break

            sent_len += data_packet_size

        # module.activate_packet_trace()
        module.read_response_command(100)

        print ('<< End')
