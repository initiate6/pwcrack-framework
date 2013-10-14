



#system = platform.system()
#if system == 'Windows':
#    import _winreg
#    from subprocess import Popen, PIPE
#if system == 'Linux':
#    import subprocess
'''
class LinuxInfo():
    
    import subprocess

    #def getGpuMemory():
        #clinfo_process = subprocess.Popen(['clinfo'], stdout=subprocess.PIPE)
	#grep1_process = subprocess.Popen(['grep', 'Max memory allocation'], stdin=clinfo_process.stdout, stdout=subprocess.PIPE)
	#cut_process = subprocess.Popen(['cut', '-d:', '-f2'], stdin=grep1_process.stdout, stdout=subprocess.PIPE)
	#gpuMem = cut_process.communicate()[0]
	#gpuMem = int(gpuMem.split()[0]) / 1024 / 1024
	#return str(gpuMem)
    
    def checkamddriver():
	try:

	        clinfo_process = subprocess.Popen(['clinfo'], 
	                                            stdout=subprocess.PIPE)
	        
	        grep1_process = subprocess.Popen(['grep', 'Driver version'],
	                                            stdin=clinfo_process.stdout,
	                                            stdout=subprocess.PIPE)
	        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
	                                            stdin=grep1_process.stdout,
	                                            stdout=subprocess.PIPE)
	                                                            
	        amddriveroutput = cut_process.communicate()[0]
	        amdDriver = float(amddriveroutput.split()[0])
	        #Change to new requirements.
	        if amdDriver == 1084.4:
	            return '13.1'
	        else:
	            return None
	except:
		return None

    def checknvdriver():
	try:
        
	        clinfo_process = subprocess.Popen(['clinfo'], 
	                                            stdout=subprocess.PIPE)
	        grep1_process = subprocess.Popen(['grep', 'Driver version'],
	                                            stdin=clinfo_process.stdout,
	                                            stdout=subprocess.PIPE)
	        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
	                                            stdin=grep1_process.stdout,
	                                            stdout=subprocess.PIPE)
	                                                            
	        nvdriveroutput = cut_process.communicate()[0] 
	        nvDriver = float(nvdriveroutput.split()[0]) 
	        if nvDriver >= 310.32:
	            return str(nvDriver)
	        else:
            	    return None
	except:
		return None
	
    def getdevicename(device):
        result = device.split(':')
        return result[len(result)-1]
    
    def GetGPUinfo():

        lspci_process = subprocess.Popen(['lspci'], 
                                            stdout=subprocess.PIPE)
        grep_process = subprocess.Popen(['grep', 'VGA'],
                                            stdin=lspci_process.stdout,
                                            stdout=subprocess.PIPE)
        stdoutdata = grep_process.communicate()[0] 
        
        vcDevices = []
        for item in stdoutdata.split('\n'):
            vcDevices.append(item)
            
        for device in vcDevices:
            if re.search('AMD|ATI', device):
                amddriver = checkamddriver()
                if amddriver != None:
                    gpuType = "ocl" 
                else:
                    gpuType = None

                deviceName = getdevicename(device)
                gpuMem = getGpuMemory()
                return gpuType, deviceName,  amddriver, gpuMem
                
            elif re.search('NVIDIA', device):
                nvdriver = checknvdriver()
                if nvdriver != None:
                    gpuType = "cuda"
                else:
                    gpuType = None

                deviceName = getdevicename(device)
                gpuMem = getGpuMemory()
                return gpuType, deviceName,  nvdriver, gpuMem
                
            else:
                gpudriver = None
                gpuType = None
                deviceName = None
                gpuMem = None
                return gpuType, deviceName,  gpudriver, gpuMem

    def getCPUinfo():
        cpuInfo = []
        
        cat_process = subprocess.Popen(['cat', '/proc/cpuinfo'],
                                            stdout=subprocess.PIPE)

        grep_process = subprocess.Popen(['grep', 'processor\|name\|MHz'],
                                            stdin=cat_process.stdout,
                                            stdout=subprocess.PIPE)

        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
                                stdin=grep_process.stdout,
                                stdout=subprocess.PIPE)

        stdoutdata = cut_process.communicate()[0]	
        temp = []
        for item in stdoutdata.split('\n'):
            temp.append(item.strip())
            
        temp2 = [temp[x:x+3] for x in range(0, len(temp),3)]
                    
        for list in temp2:
            cpuInfo.append('.'.join(list))
                    
        last = cpuInfo.pop()
        if last == '':
            return cpuInfo
        else:
            cpuInfo.append(last)
            return cpuInfo

    def getRAMinfo():
        cat_process = subprocess.Popen(['cat', '/proc/meminfo'], 
                                            stdout=subprocess.PIPE)

        grep_process = subprocess.Popen(['grep', 'MemTotal'], 
                                            stdin=cat_process.stdout, 
                                            stdout=subprocess.PIPE)

        awk_process = subprocess.Popen(['awk', '{print $2}'], 
                                            stdin=grep_process.stdout, 
                                            stdout=subprocess.PIPE)

        stdoutdata = awk_process.communicate()[0]
        ramsize = int(stdoutdata) / 1024 / 1024
        return ramsize
    '''
import sys, string, re
from subprocess import Popen, PIPE
import winreg
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
        argsCore = 'wmic', 'computersystem', 'get', 'NumberOfLogicalProcessors'
        argsCPUs = 'wmic', 'computersystem', 'get', 'NumberOfProcessors'

        getCPUs = Popen(argsCPUs, stdout=PIPE)
        CPUs = getCPUs.communicate()[0]
        getCores = Popen(argsCore, stdout=PIPE)
        cores = getCores.communicate()[0]
        
        return CPUs, cores


