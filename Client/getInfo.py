##
#Copyright 2013 (Jason Wheeler INIT6@INIT6.me) and DC214.org
#
#This file is part of DPCS (Distributed Password Cracking System.)
#
#    DPCS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    DPCS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    To receive a copy of the GNU General Public License
#    see <http://www.gnu.org/licenses/>.
##

# Gather info about the computer and save to file info.json for client.py.
# client.py will only call getInfo.py if info.json file doesn't exist or --re-config.

import pycl as cl

CL_Devices = cl.clGetDeviceIDs()
for device in CL_Devices:
        print("===============================================================")
        print("Device name:", device.name)
        print("Device profile:", device.profile)
        print("Device vendor:", device.vendor)
        print("Device version:", device.version)
        print("Device platform:", device.platform)
        print("Device addressBits:", device.address_bits)
        print("Device memory: ", int(device.local_mem_size) / 1024, 'MB')
        print("Device memory: ", int(device.global_mem_size) / 1024/1024, 'MB')
        print("Device max clock speed:", device.max_clock_frequency, 'MHz')
        print("Device compute units:", device.max_compute_units)
