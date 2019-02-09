from rppgsensor import PPGSensor
from signalprocessor import Proccessor
from evaluator import Evaluator
import pandas as pd
import os
import numpy

output_path = "C:\\Users\\marti\\source\\repos\\PythonVideoHeartbeat\\output"
def export_data(eval:Evaluator):
    name = input("Experiment name : ")
    np.savetxt(output_path + "\\" + name + "_snr.csv", eval.snr, delimiter=",")
    np.savetxt(output_path + "\\" +name + "_bpm.csv", eval.bpm, delimiter=",")

import scipy.io as sio
import csv
import numpy as np
import matplotlib.pyplot as plt


def export_to_matlab(sensor):
    matname = input("Experiment name : ")
    rPPG = np.transpose(np.array(sensor.rppgl))
    mat_dict = {"rPPG" : rPPG}
    sio.savemat(matname + ".mat",mat_dict)

def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)


        
if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [join(output_path, f) for f in listdir(output_path) if isfile(join(output_path, f))]
    bpm_arrs = [np.genfromtxt(f, delimiter=',') for f in onlyfiles if "_bpm" in f]
    snr_arrs = [np.genfromtxt(f,delimiter=',') for f in onlyfiles if "_snr" in f]

    fnames = [f for f in onlyfiles if "_bpm" in f]
    names = []
    for fname in fnames:
        parts = fname.split("\\")
        for part in parts:
            if "_bpm" in part:
                name = part[:-8]
                names.append(name)


    plt.figure()
    for bpm in bpm_arrs:
        plt.plot(bpm)
    plt.ylabel('BPM')
    plt.xlabel('frame')
    plt.legend(names)

    plt.figure()
    for snr in snr_arrs:
        plt.plot(running_mean(snr,20))
    plt.ylabel('SNR')
    plt.xlabel('frame')
    plt.legend(names)



    plt.show()








            
