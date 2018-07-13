import pysfm
import com_es
import com_ei
import com_et
import com_eix
import com_etx
import com_lt
import com_ltx
import com_vs
import com_vi
import com_vt
import com_vix
import com_is
import com_ii
import com_it
import com_iix
import com_da
import com_dt
import com_ds
import com_rt
import com_rtx
import com_st
import com_si
import com_six
import com_sw
import com_sr
import com_ug
import com_rs
import time
import com_iixft
from pprint import pprint

print pysfm.__version__

module = pysfm.Module("COM5", 115200)

if module.connect() == False:
    exit(-100)

print ('Start >>')
module.send_command(command=0x03, param=0, size=0, flag=0x62)
module.read_response_command()
OperTime = module.response_command.size + 3
print ('Start >> ' '%X' % OperTime)
OperTime = OperTime - 0x30
print ('Operation Timeout = ' '%d' % OperTime)

i = 0
# test_module1 = com_six.ComSIX()
# while i < 11:
#     test_module1.test(module, OperTime, i)
#     i = i+1
# test_module1 = com_es.ComES()
# enroll_option = 0x79  # AutoID 10
# while i < 10:
#     test_module1.test(module, OperTime, 1, enroll_option)
#     i = i+1
#
# i = 0
# enroll_option = 0x71  # AddNew 10
# while i < 10:
#     test_module1.test(module, OperTime, i+1, enroll_option)
#     i = i+1
#
# i = 0
# enroll_option = 0x70  # Check ID 10
# while i < 10:
#     test_module1.test(module, OperTime, i+1, enroll_option)
#     i = i+1
#
# i = 0
# enroll_option = 0x84  # Check Finger 10
# while i < 10:
#     test_module1.test(module, OperTime, i+1, enroll_option)
#     i = i+1
#
# test_module2 = com_vs.ComVS()
# i = 0  # Verification UserID 1 to 10
# while i < 10:
#     test_module2.test(module, OperTime, i+1)
#     i = i+1
#
# test_module3 = com_is.ComIS()
# i = 0  # Identification UserID 10
# while i < 10:
#     test_module3.test(module, OperTime)
#     i = i+1

test_module4 = com_da.ComDA()  # Delete All
# test_module4.test(module)
#
test_module5 = com_sw.ComSW()  # System Parameter (Template type) -> 0x31 (ISO)
# test_module5.test(module, 0x31, 0x96)
#
# test_module6 = com_etx.ComETX()
# enroll_option = 0x79  # Other Type Template -> Unsupported
# test_module6.test(module, OperTime, 1, enroll_option, 0)
#
# test_module5.test(module, 0x30, 0x96)  # System Parameter (Template type) -> 0x30 (Suprema)
#
# i = 0
# enroll_option = 0x79  # Enroll by Template : AutoID 10
# while i < 10:
#     test_module6.test(module, OperTime, 1, enroll_option, i)
#     i = i+1
#
# test_module7 = com_vt.ComVT()
# i = 0  # Verification by Template 10
# while i < 10:
#     test_module7.test(module, OperTime, i+1, i)
#     i = i+1
#
# i = 0  # Verification by Template 10
# while i < 10:
#     test_module7.test(module, OperTime, (i+1) % 10 + 1, i)
#     i = i+1
#
# test_module8 = com_it.ComIT()
# i = 0  # Identification by Template 10
# while i < 10:
#     test_module8.test(module, OperTime, i)
#     i = i+1
#
test_module9 = com_eix.ComEIX()
# enroll_option = 0x79  # Enroll by Image 10
# while i < 10:
#     test_module9.test(module, OperTime, 1, enroll_option, i)
#     i = i+1
#
# test_module10 = com_vix.ComVIX()
# i = 0  # Verification by Image 10
# while i < 10:
#     test_module10.test(module, OperTime, i+11, i)
#     i = i+1
#
# i = 0  # Verification by Image 10
# while i < 10:
#     test_module10.test(module, OperTime, (i+1) % 10 + 11, i)
#     i = i+1
#
# test_module11 = com_iix.ComIIX()
# i = 0  # Identification by Image 10
# while i < 10:
#     test_module11.test(module, OperTime, i)
#     i = i+1
#
# test_module5.test(module, 0x31, 0x84)  # System Parameter (Freescan) -> 0x31 (On)

# test_module4.test(module)
# i = 0
# enroll_option = 0x79
# while i < 1000:
#     test_module9.test(module, OperTime, 1, enroll_option, i % 10)
#     i = i+1

test_module14 = com_iixft.ComIIX()
test_module5.test(module, 0x30, 0x93)  # System Parameter (Fast Mode) -> 0x30 (Normal)
time_normal = test_module14.test(module, OperTime, 10)
test_module5.test(module, 0x31, 0x93)  # System Parameter (Fast Mode) -> 0x31 (Fast Mode 1)
time_f1 = test_module14.test(module, OperTime, 10)
test_module5.test(module, 0x32, 0x93)  # System Parameter (Fast Mode) -> 0x32 (Fast Mode 2)
time_f2 = test_module14.test(module, OperTime, 10)
test_module5.test(module, 0x33, 0x93)  # System Parameter (Fast Mode) -> 0x33 (Fast Mode 3)
time_f3 = test_module14.test(module, OperTime, 10)
test_module5.test(module, 0x34, 0x93)  # System Parameter (Fast Mode) -> 0x34 (Fast Mode 4)
time_f4 = test_module14.test(module, OperTime, 10)
test_module5.test(module, 0x35, 0x93)  # System Parameter (Fast Mode) -> 0x35 (Fast Mode 5)
time_f5 = test_module14.test(module, OperTime, 10)
test_module5.test(module, 0x36, 0x93)  # System Parameter (Fast Mode) -> 0x36 (Automatic)
time_auto = test_module14.test(module, OperTime, 10)
time_dict = {"time_normal":time_normal, "time_f1":time_f1, "time_f2":time_f2, "time_f3":time_f3, "time_f4":time_f4, "time_f5":time_f5, "time_auto":time_auto}
pprint(time_dict)
# test_module4.test(module)
# test_module11 = com_ug.ComUG()
# test_module11.test(module)

# i = 0
# enroll_option = 0x79  # Make DB Full
# while i < 5000:
#     test_module6.test(module, OperTime, 1, enroll_option, i % 10)
#     i = i+1
#
# i = 0  # Verification
# while i < 5000:
#     test_module7.test(module, OperTime, i+1, i % 10)
#     i = i+1
#
# i = 0  # Verification
# while i < 5000:
#     test_module7.test(module, OperTime, i+1, (i+1) % 10)
#     i = i+1
#
# test_module4.test(module)  # Delete All

# i = 0
# enroll_option = 0x79  # Enroll by Template 10
# while i < 10:
#     test_module6.test(module, OperTime, 1, enroll_option, i)
#     i = i+1

# test_module12 = com_rs.ComRS()  # Reset
# test_module12.test(module)

# test_module5.test(module, 0x31, 0x90)  # System Parameter (Light condition) -> 0x31 (Indoor)
#
# i = 0
# test_module13 = com_six.ComSIX()  # Scan Image 10
# while i < 10:
#     test_module13.test(module, OperTime, i)
#     i = i+1
#
# test_module5.test(module, 0x30, 0x84)  # System Parameter (Freescan) -> 0x30 (Off)
# test_module5.test(module, 0x30, 0x90)  # System Parameter (Light condition) -> 0x30 (Outdoor)

module.disconnect()
