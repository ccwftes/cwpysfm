import pysfm
import wtd  # form: wtd.test(module, OperTime, command, param, size, flag, i, timetest)
import time
from pprint import pprint

print pysfm.__version__

module = pysfm.Module("COM5", 115200)

if module.connect() == False:
    exit(-100)

wtd.test(module, 30, 0x03, 0, 0, 0x62)
OperTime = module.response_command.size + 50
print ('Start >> ' '%X' % OperTime)
OperTime = OperTime - 0x30
print ('Operation Timeout = ' '%d' % OperTime)

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x05, 1, 0, 0x79)  # AutoID
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x05, i+1, 0, 0x71)  # AddNew
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x05, i+1, 0, 0x70)  # Check ID
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x05, 1, 0, 0x84)  # Check Finger
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x08, i+1, 0, 0)  # Verification UserID
    i = i+1

i = 0  # Identification UserID 10
while i < 10:
    wtd.test(module, OperTime, 0x11, 0, 0, 0)  # Identification UserID
    i = i+1

wtd.test(module, OperTime, 0x17, 0, 0, 0)  # Delete All = 0x17

wtd.test(module, OperTime, 0x01, 0, 0x31, 0x96)  # System Parameter (Template type) -> 0x31 (ISO)
wtd.test(module, OperTime, 0x02, 0, 0, 0)

wtd.test(module, OperTime, 0x87, 1, 0, 0x79, 0)  # Other Type Template -> Unsupported

wtd.test(module, OperTime, 0x01, 0, 0x30, 0x96)  # System Parameter (Template type) -> 0x30 (Suprema)
wtd.test(module, OperTime, 0x02, 0, 0, 0)

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x87, 1, 0, 0x79, i)
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x10, i + 1, 0, i)  # Verification by Template 10
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x10, (i + 1) % 10 + 1, 0, i)  # Verification by Template 10
    i = i+1

i = 0
while i < 10:
    wtd.test(module, OperTime, 0x13, 0, 0, i)  # Identification by Template 10
    i = i+1

# i = 0
# while i < 10:
#     wtd.test(module, OperTime, 0x80, 1, 0, 0x79, i)  # Enroll by Image 10
#     i = i+1
#
# i = 0
# while i < 10:
#     wtd.test(module, OperTime, 0x82, i + 11, 0, i)  # Verification by Image 10
#     i = i+1
#
# i = 0
# while i < 10:
#     wtd.test(module, OperTime, 0x82, (i + 1) % 10 + 11, 0, i)  # Verification by Image 10
#     i = i+1
#
# i = 0
# while i < 10:
#     wtd.test(module, OperTime, 0x81, 0, 0, i)  # Identification by Image 10
#     i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x31, 0x84)  # System Parameter (Freescan) -> 0x31 (On)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
wtd.test(module, OperTime, 0x17, 0, 0, 0)

i = 0
while i < 1000:
    wtd.test(module, OperTime, 0x87, 1, 0, 0x79, i % 10)
    i = i+1

time_normal = 0.0
time_f1 = 0.0
time_f2 = 0.0
time_f3 = 0.0
time_f4 = 0.0
time_f5 = 0.0

wtd.test(module, OperTime, 0x01, 0, 0x30, 0x93)  # System Parameter (Fast Mode) -> 0x30 (Normal)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
i = 0
while i < 10:  # 6020 = 0 - 9 (True), 10 - 19 (False) / 5030 = 20 - 29 (False)
    time_normal += wtd.test(module, OperTime, 0x81, 0, 0, 0, i+20, 1)  # Identification by Image 10
    i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x31, 0x93)  # System Parameter (Fast Mode) -> 0x31 (Fast Mode 1)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
i = 0
while i < 10:
    time_f1 += wtd.test(module, OperTime, 0x81, 0, 0, 0, i+20, 1)
    i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x32, 0x93)  # System Parameter (Fast Mode) -> 0x32 (Fast Mode 2)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
i = 0
while i < 10:
    time_f2 += wtd.test(module, OperTime, 0x81, 0, 0, 0, i+20, 1)
    i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x33, 0x93)  # System Parameter (Fast Mode) -> 0x33 (Fast Mode 3)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
i = 0
while i < 10:
    time_f3 += wtd.test(module, OperTime, 0x81, 0, 0, 0, i+20, 1)
    i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x34, 0x93)  # System Parameter (Fast Mode) -> 0x34 (Fast Mode 4)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
i = 0
while i < 10:
    time_f4 += wtd.test(module, OperTime, 0x81, 0, 0, 0, i+20, 1)
    i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x35, 0x93)  # System Parameter (Fast Mode) -> 0x35 (Fast Mode 5)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
i = 0
while i < 10:
    time_f5 += wtd.test(module, OperTime, 0x81, 0, 0, 0, i+20, 1)
    i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x36, 0x93)  # System Parameter (Fast Mode) -> 0x36 (Automatic)
wtd.test(module, OperTime, 0x02, 0, 0, 0)

time_dict = {"time_normal": time_normal/10, "time_f1": time_f1/10, "time_f2": time_f2/10, "time_f3": time_f3/10, "time_f4": time_f4/10, "time_f5": time_f5/10}
pprint(time_dict)

wtd.test(module, OperTime, 0x17, 0, 0, 0)

# wtd.test(module, OperTime, 0x62, 0, 0, 0)  # fw UPGRADE

# i = 0  # Make DB Full
# while i < 5000:
#     wtd.test(module, OperTime, 0x87, 1, 0, 0x79, i % 10)
#     i = i+1
#
# i = 0  # Verification
# while i < 5000:
#     wtd.test(module, OperTime, 0x10, i + 1, 0, i % 10)
#     i = i+1
#
# i = 0  # Verification
# while i < 5000:
#     wtd.test(module, OperTime, 0x10, (i + 1) % 5000 + 1, 0, i % 10)
#     i = i+1
#
# wtd.test(module, OperTime, 0x17, 0, 0, 0)

wtd.test(module, OperTime, 0xD0, 0, 0, 0)  # Reset
time.sleep(2)
wtd.test(module, OperTime, 0x01, 0, 0x31, 0x90)  # System Parameter (Light condition) -> 0x31 (Indoor)
wtd.test(module, OperTime, 0x02, 0, 0, 0)

# i = 0
# while i < 10:
#     wtd.test(module, OperTime, 0x83, 0, 0, 0, i)  # Scan Image
#     i = i+1

wtd.test(module, OperTime, 0x01, 0, 0x30, 0x84)  # System Parameter (Freescan) -> 0x30 (Off)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
wtd.test(module, OperTime, 0x01, 0, 0x30, 0x90)  # System Parameter (Light condition) -> 0x30 (Outdoor)
wtd.test(module, OperTime, 0x02, 0, 0, 0)
module.disconnect()
