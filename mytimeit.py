import time
import sys
def timeit(f,name):
    tstart = time.time()
    r = f()
    dt = time.time()-tstart
    
    mystr = name + " time :  {:.2f}".format(dt*1000) + " (ms)" + " Fps :	{:.2f}".format(1/dt)
    sys.stdout.write("\r"+mystr)
    sys.stdout.flush()
    return r
