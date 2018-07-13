# coding=cp949
import pysfm
import time


class ComDelete:
    def __init__(self, module):
        module.send_command(command=pysfm.UF_COM_SR, param=0, size=0, flag=0x75)
        module.read_response_command()
        self.send_scan_success = module.response_command.size

    def do_delete(self, module, id_range, command, OperTime):
        send_scan_success = self.send_scan_success

        time.sleep(2)
        module.send_command(command, id_range)
        if send_scan_success == 0x31:
            module.read_response_command(OperTime)
        module.read_response_command(OperTime)
        if module.response_command.error == 0x61:
            print('     Success')
        else:
            if module.response_command.error == 0x63:
                print('     Scan fail')
            elif module.response_command.error == 0x6B:
                print('     Try again')
            elif module.response_command.error == 0x6C:
                print('     Scan timeout')
            elif module.response_command.error == 0x7A:
                print('     Timeout match')
            elif module.response_command.error == 0x69:
                print('     Not found')
            module.disconnect()
            quit()
