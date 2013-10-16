
import sys, string, re
from subprocess import Popen, PIPE
#Get operating system.
system = platform.system()
if system == 'Windows':
    import winreg


class linuxInfo():
    def getCPUinfo(self):

            cat_process = Popen(['cat', '/proc/cpuinfo'], stdout=PIPE)

            grep_process = Popen(['grep', 'vendor_id\|name\|MHz'], stdin=cat_process.stdout, stdout=PIPE)

            cut_process = Popen(['cut', '-d:', '-f2'], stdin=grep_process.stdout, stdout=PIPE)

            stdoutdata = cut_process.communicate()[0]

            # how many = cores unquie = cpus cat /sys/devices/system/cpu/cpu[0-9]*/topology/physical_package_id

            temp = []
            for item in stdoutdata.split('\n'):
                temp.append(item.strip())

            cpuInfo = [temp[x:x+3] for x in range(0, int(len(temp)-1),3)]

            for list in cpuInfo:
                vendor = list[0]
                name = list[1]
                mhz = list[2]
                break

            phyids = []
            ls_process = Popen(['ls', '/sys/devices/system/cpu/'], stdout=PIPE)
            grep_process = Popen(['grep', 'cpu[0-9]'], stdin=ls_process.stdout, stdout=PIPE)
            folders = grep_process.communicate()[0]

            base = '/sys/devices/system/cpu/'
            for folder in folders.split('\n'):
                if folder == '':
                    break
                args = 'cat', base + str(folder) + '/topology/physical_package_id'
                cat_ps = Popen(args, stdout=PIPE)
                out2 = cat_ps.communicate()[0]
                phyids.append(out2.strip('\n'))

            coreCount = len(phyids)
            cpuCount = 0
            phyids = phyids.sort()
            if phyids != None:
                for phyid in phyids:
                    if int(phyid) != cpuCount:
                        cpuCount += 1
            #add one to cpu count so counting starts from 1
            cpuCount += 1
            cores = coreCount / cpuCount
            return cpuCount, cores, mhz, name, vendor

    def getBits(self):
        bits = 64
        return bits

    def getRAMinfo(self):
        cat_process = Popen(['cat', '/proc/meminfo'], stdout=PIPE)
        grep_process = Popen(['grep', 'MemTotal'], stdin=cat_process.stdout, stdout=PIPE)
        awk_process = Popen(['awk', '{print $2}'], stdin=grep_process.stdout, stdout=PIPE)

        stdoutdata = awk_process.communicate()[0]
        ramsize = int(stdoutdata) / 1024 / 1024
        return ramsize

        
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


