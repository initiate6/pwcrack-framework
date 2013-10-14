



#system = platform.system()
#if system == 'Windows':
#    import _winreg
#    from subprocess import Popen, PIPE
#if system == 'Linux':
#    import subprocess

class LinuxInfo:
    import subprocess

    def getGpuMemory():
	try:
	        clinfo_process = subprocess.Popen(['clinfo'], 
	                                            stdout=subprocess.PIPE)
	        
	        grep1_process = subprocess.Popen(['grep', 'Max memory allocation'],
	                                            stdin=clinfo_process.stdout,
	                                            stdout=subprocess.PIPE)
	        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
	                                            stdin=grep1_process.stdout,
	                                            stdout=subprocess.PIPE)
	                                                            
	        gpuMem = cut_process.communicate()[0] 
	        gpuMem = int(gpuMem.split()[0]) / 1024 / 1024
		
		return str(gpuMem)
	except:
		return 0

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

class windowsInfo:

    #Checks if system is 64bit.
    def checkBits():
        bits = sys.maxsize > 2**32
        if bits == True:
            return "64bit"
        else:
            return "32bit"

    def getRAMinfo():
        args = 'wmic', 'computersystem', 'get', 'TotalPhysicalMemory'
        getRam = Popen(args, stdout=PIPE)
        output = getRam.communicate()[0]
        rambytes = int(output.split()[1])
        ramMB = rambytes / 1024 / 1024 / 1024
        return ramMB
        
    #Get CPU info on Windows computers.
    def getCPUinfo():
        """Retrieves Machine information from the registry"""
        cpuInfo = []
        try:
           hHardwareReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "HARDWARE")
           hDescriptionReg = _winreg.OpenKey(hHardwareReg, "DESCRIPTION")
           hSystemReg = _winreg.OpenKey(hDescriptionReg, "SYSTEM")
           hCentralProcessorReg = _winreg.OpenKey(hSystemReg, "CentralProcessor")
           nbProcessors = _winreg.QueryInfoKey(hCentralProcessorReg)[0]

           for idxKey in range(nbProcessors):
               hProcessorIDReg = _winreg.OpenKey(hCentralProcessorReg, str(idxKey))
               processorDescription = _winreg.QueryValueEx(hProcessorIDReg,"ProcessorNameString")[0]
               mhz = _winreg.QueryValueEx(hProcessorIDReg, "~MHz")[0]
               cpuInfo.append(str(idxKey)+'.'+string.lstrip(processorDescription)+'.'+str(mhz))
                
           return cpuInfo

        except WindowsError:
           print "Cannot retrieve processor information from registry!"

    #Get GPU info on Windows computers.
    def getGPUinfo():
        try:
            hHardwareReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "HARDWARE")
            hDeviceMapReg = _winreg.OpenKey(hHardwareReg, "DEVICEMAP")
            hVideoReg = _winreg.OpenKey(hDeviceMapReg, "VIDEO")
            hVideoDevices = _winreg.QueryInfoKey(hVideoReg)[1]
            VideoCardString = []
            for x in range(0, hVideoDevices, 1):
                VideoCardString.append(_winreg.EnumValue(hVideoReg, x)[1])
                ClearnVideoCardString = []
                for line in VideoCardString:
                    ClearnVideoCardString.append("\\".join(str(line).split("\\")[3:]))

                    done = False #So it only runs once for GPU info. 
                    #Get the graphics card information
                    for line in ClearnVideoCardString:
                        for item in line.split("\\")[2:3]:
                            if done == False and item == 'Control':
                                hVideoCardReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, str(line))
                                VideoCardDescription  = _winreg.QueryValueEx(hVideoCardReg,"Device Description")[0]
                                
                                #check if its a AMD/ATI card and if so return detailed info.
                                if re.search('AMD|ATI', str(VideoCardDescription)) != None:
                                    gpuDesc = str(VideoCardDescription)
                                    amdCatalystVer = _winreg.QueryValueEx(hVideoCardReg, "Catalyst_Version")[0]
                                    VideoCardMemorySize = _winreg.QueryValueEx(hVideoCardReg,"HardwareInformation.MemorySize")[0]
                                    gpuMem = str(VideoCardMemorySize / 1024 / 1024)
                                    gpuType = "ocl"
                                    done = True 
                            
                            
                                #check if its a Nvidia card and if so return detailed info.
                                elif re.search('nvidia', str(VideoCardDescription)) != None:
                                    gpuDesc = str(VideoCardDescription)
                                    nvDriverVer = _winreg.QueryValueEx(hVideoCardReg, "DriverVersion")[0]
                                    VideoCardMemorySize = _winreg.QueryValueEx(hVideoCardReg,"HardwareInformation.MemorySize")[0]
                                    gpuMem = str(VideoCardMemorySize / 1024 / 1024)
                                    gpuType = "cuda"
                                    done = True

                #breaks to step out of for loops once done.                                        
                        if done == True:
                            break
                    if done == True:
                        break
                if done == True:
                    break
                
            #checks if gpu driver is good and return info
            if re.search('AMD|ATI', gpuDesc):
                if amdCatalystVer == '13.1':
                    return gpuType, gpuDesc, amdCatalystVer, VideoCardMemorySize
                else:
                    print "Your GPU driver for  %s is %s and needs to be upgraded or downgraded to match oclhashcat requirements 13.1" % ( gpuDesc, amdCatalystVer )
                    return None, None, None, None
                
            elif re.search('nvidia', gpuDesc):
                if float(nvDriverVer) >= float(310.02):
                    return gpuType, gpuDesc, nvDriverVer, VideoCardMemorySize
                else:
                    print "Your GPU driver for  %s is %s and needs to be upgraded or downgraded to match oclhashcat requirements 13.1" % ( gpuDesc, nvDriverVer )
                    return None, None, None, None
            else:
                return None, None, None, None
         
        except WindowsError:
            print "Cannot Retrieve Graphics Card Name and Memory Size!"
