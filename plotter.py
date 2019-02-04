from PyQt5 import QtGui  
from PyQt5 import QtCore  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from util.qt_util import *
from util.pyqtgraph_util import *
from rppgsensor import PPGSensor
from signalprocessor import Proccessor
from evaluator import Evaluator
from multiprocessing import Process, Manager, Queue
import sched, time, threading


def create_plotter(fs,fftlength,q):
    
    app,w = create_basic_app()
    f = np.linspace(0,fs/2,fftlength/2 + 1) * 60
    layout_main = QVBoxLayout()
    layout_lower = QHBoxLayout()
    layout_upper = QHBoxLayout()
    
    layout_main.addLayout(layout_lower)
    layout_main.addLayout(layout_upper)

    fig = create_fig()
    fig.setTitle('Raw PPG')
    addLabels(fig,'time','intensity','-','sec')

    plt_r = plot(fig,np.arange(0,5),np.arange(0,5),[255,0,0])
    plt_g = plot(fig,np.arange(0,5),np.arange(0,5),[0,255,0])
    plt_b = plot(fig,np.arange(0,5),np.arange(0,5),[0,0,255])

    fig_fppg = create_fig()
    fig_fppg.setTitle('Filtered PPG')
    addLabels(fig,'time','intensity','-','sec')
    plt_x = plot(fig_fppg,np.arange(0,5),np.arange(0,5),[255,0,0])

    fig_snr = create_fig()
    fig_snr.setTitle('SNR')
    addLabels(fig,'time','SNR','-','sec')
    plt_snr = plot(fig_snr,np.arange(0,5),np.arange(0,5),[255,0,0])

    fig_bpm = create_fig()
    fig_bpm.setTitle('Frequency')
    fig_bpm.setXRange(0,300)
    addLabels(fig_bpm,'Frequency','intensity','-','BPM')
    plt_bpm = plot(fig_bpm,np.arange(0,5),np.arange(0,5),[255,0,0])

    fig_bpmdt = create_fig()
    fig_bpmdt.setTitle('Hearbeat over time')
    addLabels(fig_bpm,'Frequency','intensity','-','BPM')
    plt_bpmdt = plot(fig_bpmdt,np.arange(0,5),np.arange(0,5),[255,0,0])

    layout_upper.addWidget(fig)
    layout_upper.addWidget(fig_fppg)
    layout_lower.addWidget(fig_snr)
    layout_lower.addWidget(fig_bpm)
    layout_lower.addWidget(fig_bpmdt)
    
    w.setLayout(layout_main)

    def update_plots(q):
        try:
            item = q.get()
            r = item[0]
            g = item[1]
            b = item[2]
            t = item[3]
            plt_r.setData(t,r)
        except Exception:
            pass
       

    timer = QtCore.QTimer()
    timer.start(50)
    timer.timeout.connect(lambda : update_plots(q))

    execute_app(app,w)   




# Executed on main thread
def update_data(q,sensor,proccessor):
    
    
    num_frames = sensor.rppg.shape[1]
    start = max([num_frames-100,0])
    t = np.arange(num_frames)/proccessor.fs
    rPPG = sensor.rppg
    t = t[start:num_frames]
    r = rPPG[0,start:num_frames]
    g = rPPG[1,start:num_frames]
    b = rPPG[2,start:num_frames]
    item = [r,g,b,t]
    q.put(item)
    # plt_r.setData(t[start:num_frames],rPPG[0,start:num_frames])
    # plt_g.setData(t[start:num_frames],rPPG[1,start:num_frames])
    # plt_b.setData(t[start:num_frames],rPPG[2,start:num_frames])
    
    # if processor.enough_samples:
    #     plt_x.setData(t[-300:],processor.x_stride_method)
    #     snr = evaluator.snr
    #     plt_snr.setData(t[-min(100,len(snr)):],snr[-min(100,len(snr)):])
    #     plt_bpm.setData(f,processor.normalized_amplitude)
    #     bpm_movavg = evaluator.bpm
    #     #bpm_movavg = np.convolve(evaluator.bpm, np.ones((100,))/100, mode='valid')
    #     plt_bpmdt.setData(t[-min(200,len(bpm_movavg)):],bpm_movavg[-min(200,len(bpm_movavg)):])
    
