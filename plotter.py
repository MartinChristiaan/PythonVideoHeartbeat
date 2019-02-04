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
            #[r,g,b,x_stride,snr,bpm,bpmdt,t_snr,t_bpm,t]
            item = q.get()
            r = item[0]
            g = item[1]
            b = item[2]
            x_stride = item[3]
            snr = item[4]
            amp = item[5]
            bpmdt = item[6]
            tx = item[7]
            t_snr = item[8]
            t_bpm = item[9]
            t = item[10]

            plt_r.setData(t,r)
            plt_g.setData(t,g)
            plt_b.setData(t,b)
            if len(t_bpm)>1:
                plt_x.setData(tx,x_stride)
                plt_snr.setData(t_snr,snr)
                plt_bpm.setData(f,amp)
                plt_bpmdt.setData(t_bpm,bpmdt)

        except Exception:
            pass
       

    timer = QtCore.QTimer()
    timer.start(20)
    timer.timeout.connect(lambda : update_plots(q))

    execute_app(app,w)   


class Plotter():
    def __init__(self,sensor,proccessor,evaluator):
        self.q = Queue()
        self.sensor = sensor
        self.proccessor = proccessor
        self.evalu = evaluator
        self.p = Process(target=create_plotter, args=(proccessor.fs,proccessor.fftlength,self.q))
        self.p.start()
    def stop(self):
        self.p.join()

    def update_data(self):

        num_frames = self.sensor.rppg.shape[1]
        start = max([num_frames-100,0])
        t_ = np.arange(num_frames)/self.proccessor.fs
        rPPG = self.sensor.rppg
        
        t = t_[start:]
        r = rPPG[0,start:]
        g = rPPG[1,start:]
        b = rPPG[2,start:]
        x_stride = np.zeros(300)
        snr = np.zeros(10)
      
        amp = np.zeros(300)
        bpmdt = np.zeros(1)
        t_snr = t[-10:]
        t_bpm = t[-1:]
        tx = t_
        if self.proccessor.enough_samples:
            x_stride = self.proccessor.x_stride_method
            tx = t_[-300:]
            snr = self.evalu.snr
            snr = snr[-min(100,len(snr)):]
            t_snr = t[-min(100,len(snr)):]
            amp = self.proccessor.normalized_amplitude
            bpmdt = self.evalu.bpm
            bpmdt = bpmdt[-min(200,len(bpmdt)):]
            t_bpm = t[-min(200,len(bpmdt)):]
        
        item = [r,g,b,x_stride,snr,amp,bpmdt,tx,t_snr,t_bpm,t]
        self.q.put(item)
