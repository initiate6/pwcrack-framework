
import sys, string, re
from subprocess import Popen, PIPE
#Get operating system.
system = platform.system()
if system == 'Windows':
    import winreg

for ls /sys/devices/system/cpu/
ls /sys/devices/system/cpu/ | cpu[0-9]*/topology/core_id


class linuxInfo():
    def getCPUinfo():

        cat_process = Popen(['cat', '/proc/cpuinfo'], stdout=PIPE)

        grep_process = Popen(['grep', 'physical id\|processor\|name\|MHz'], stdin=cat_process.stdout, stdout=PIPE)

        cut_process = Popen(['cut', '-d:', '-f2'], stdin=grep_process.stdout, stdout=PIPE)

        stdoutdata = cut_process.communicate()[0]

        temp = []
        for item in stdoutdata.split('\n'):
            temp.append(item.strip())

        cpuInfo = [temp[x:x+4] for x in range(0, int(len(temp)-1),4)]

        CPUcount = 0
        CoresCount = 0
        phyid = 0
        for list in cpuInfo:
            if phyid == int(list[3]):
                CoresCount += 1
            else:
                phyid += 1
                CPUcount += 1
                CoresCount +=1
            name = list[1]
            mhz = list[2]
        if CPUcount == 0:
            CPUcount = 1
            
        cores = CoresCount / CPUcount

        return CPUcount, cores, speed, name, name
    
class windowsInfo():
    
    def getBits():
        argsBits = 'wmic', 'computersystem', 'get', 'SystemType'
        getBits = Popen(argsBits, stdout=PIPE)
        output = getBits.communicate()[0]
        if re.search('64', str(output)):
            bits = 64
        else:
            bits = 32
        return bits
            
    def getRAMinfo():
        args = 'wmic', 'computersystem', 'get', 'TotalPhysicalMemory'
        getRam = Popen(args, stdout=PIPE)
        output = getRam.communicate()[0]
        rambytes = int(output.split()[1])
        ramMB = rambytes / 1024 / 1024 / 1024
        return ramMB
        
    #Get CPU info on Windows computers.
    def getCPUinfo():
        
        argsCPUs = 'wmic', 'computersystem', 'get', 'NumberOfProcessors'
        getCPUs = Popen(argsCPUs, stdout=PIPE)
        CPUs = getCPUs.communicate()[0]
        cpus = str(CPUs, encoding='utf-8').strip('\r\n ').split()[1]

        argsCore = 'wmic', 'CPU', 'get', 'NumberOfCores'
        getCores = Popen(argsCore, stdout=PIPE)
        cores = getCores.communicate()[0]
        cores = str(cores, encoding='utf-8').strip('\r\n ').split()[1]

        argsSpeed = 'wmic', 'CPU', 'get', 'MaxClockSpeed'
        getSpeed = Popen(argsSpeed, stdout=PIPE)
        speed = getSpeed.communicate()[0]
        speed = str(speed, encoding='utf-8').strip('\r\n ').split()[1]
        
        argsName = 'wmic', 'CPU', 'get', 'Name'
        getCname = Popen(argsName, stdout=PIPE)
        cname = getCname.communicate()[0]
        cname = str(cname, encoding='utf-8').strip('\r\n ').split()[1]
        
        argsVendor = 'wmic', 'CPU', 'get', 'Manufacturer'
        getVendor = Popen(argsVendor, stdout=PIPE)
        vendor = getVendor.communicate()[0]
        vendor = str(vendor, encoding='utf-8').strip('\r\n ').split()[1]

        return cpus, cores, speed, cname, vendor


