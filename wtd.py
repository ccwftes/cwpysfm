import htd


def test(module, OperTime, command, param, size, flag, i=0, timetest=0):
    print ('Start >>')
    if command == 0x05 or command == 0x06 or command == 0x07 or command == 0x80 or command == 0x87:
        es = htd.ComEnroll(module)
        es.print_enroll_mode(module)
        es.select_enroll_option(flag)
        es.do_enroll(module, param, command, OperTime, i, flag)
    elif command == 0x15 or command == 0x20 or command == 0x83 or command == 0x84:
        htd.do_image(module, command, OperTime, i)
    elif command == 0x01 or command == 0x02 or command == 0x03 or command == 0xD0:
        module.send_command(command, 0, size, flag)
        htd.print_error(module, OperTime)
    elif command == 0x14 or command == 0x21 or command == 0x89:
        es = htd.ComTemplate(module)
        es.do_template(module, param, command, OperTime, flag, size)
    elif command == 0x11 or command == 0x12 or command == 0x13 or command == 0x81 or command == 0x08 or command == 0x09 or command == 0x10 or command == 0x82:
        if timetest == 0:
            htd.do_iv(module, param, command, OperTime, i)
        elif timetest == 1:
            extime = htd.do_iv(module, param, command, OperTime, i, 1)
            print ('<< End')
            return extime
    elif command == 0x17 or command == 0x16 or command == 0x1E:
        htd.do_delete(module, param, command, OperTime, size, flag)
    elif command == 0x18 or command == 0x86:
        module.send_command(command, param, size)
        htd.print_error(module, OperTime)
        templates_count = module.response_command.param
        data_size = module.response_command.size
        print ('Templates count : %d  Data size : %d' % (templates_count, data_size))
        if command == 0x18:
            module.read_data(data_size)
        elif command == 0x86:
            htd.print_error(module, OperTime)
            for x in range(templates_count):
                module.read_data(8)
    elif command == 0x62:
        data = htd.read_file(module, command)
        data_list = []
        for x in data:
            data_list.append(ord(x))
        const_data_packet_size = 0x1000
        htd.send_exdtp(module, command, OperTime, data_list, const_data_packet_size)
        module.read_response_command(100)

    print ('<< End')
