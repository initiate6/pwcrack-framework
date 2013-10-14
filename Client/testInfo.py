import nonCL

test = nonCL.windowsInfo.getBits()
print (test)

cpus, cores = nonCL.windowsInfo.getCPUinfo()
print (cpus, cores)
