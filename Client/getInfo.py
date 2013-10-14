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


# TODO
# implement nonCL.py for computers that don't have openCL aka nonGPU

import pycl as cl
import re, platform, json, random

def main():
    json_db = {}
    json_db['CPUs'] = {}
    json_db['GPUs'] = {}

    #email = raw_input("What is your e-mail address?: ")
    email = "init6@init6.me"
    
    #Get operating system.
    system = platform.system()     


    #Get RAM, bits, CPU and GPU information.
    CPUcount = 0
    GPUcount = 0
    gpuType = None
    gpuDriver = None


    CL_Devices = cl.clGetDeviceIDs()
    for device in CL_Devices:
        if re.search('CPU', str(device.type)):
            CPUcount += 1
            CPUd = dict([("DeviceName", str(device.name)), \
                         ("DeviceVendor", str(device.vendor)), \
                         ("DeviceBits", int(device.address_bits)), \
                         ("DeviceSpeedMHz", int(device.max_clock_frequency)), \
                         ("DeviceCores", int(device.max_compute_units)), \
                         ])
                        
            
            json_db['CPUs']['CPU'+str(CPUcount)] = CPUd

        elif re.search('GPU', str(device.type)):
            GPUcount += 1
            if re.search('AMD', str(device.vendor)):
                gpuType = 'ocl'
                #Do a RE for ###.# and test its above cut off
                gpuDriver = 'test'
            if re.search('NV'|'nvidia', str(device.vendor)):
                gpuType = 'cuda'
                #Do a RE for ###.# and test its above cut off
                gpuDriver = 'test'
                        
                GPUd = dict([("DeviceName", str(device.name)), \
                             ("DeviceVendor", str(device.vendor)), \
                             ("Device platform", str(device.platform)), \
                             ("DeviceBits", int(device.address_bits)), \
                             ("Device memory", int(device.global_mem_size) / 1024/1024 ), \
                             ("DeviceSpeedMHz", int(device.max_clock_frequency)), \
                             ("DeviceCores", int(device.max_compute_units)), \
                             ("GpuType", str(gpuType)), \
                             ])
                json_db['GPUs']['GPU'+str(GPUcount)] = GPUd
        else:
                print("Unknown device")

    #Create a clientID based off system information + 4digit random number
    clientID = system[0] + str(device.address_bits)[0] + str(CPUcount) + str(GPUcount) + str(gpuType)[0] + '.' + str(random.randint(0000,9999)).rjust(4, '0')        
    SYSd = dict([ ("OS", str(system)), \
                      ("RAM", int(device.local_mem_size) / 1024), \
                      ("Bits", int(device.address_bits)), \
                      ("CPUs", CPUcount), \
                      ("GPUs", GPUcount), \
                      ("email", str(email)), \
                      ("ClientID", clientID), \
                    ])
    json_db['System'] = SYSd

        
    test = json.dumps(json_db, sort_keys=True, indent=4)
    print (test)
    #TODO Save to file info.json

main()
