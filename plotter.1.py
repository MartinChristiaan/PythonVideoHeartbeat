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
class Plotter():
    def __init__(self,sensor:PPGSensor,signal_processor:Proccessor,evaluator : Evaluator):
        
        self.app,self.w = create_basic_app()
        
        self.sensor = sensor
        self.processor = signal_processor
        self.evaluator = evaluator
        self.f = np.linspace(0,signal_processor.fs/2,signal_processor.fftlength/2 + 1) * 60
        layout_main = QVBoxLayout()
        layout_lower = QHBoxLayout()
        layout_upper = QHBoxLayout()
        
        layout_main.addLayout(layout_lower)
        layout_main.addLayout(layout_upper)

        fig = create_fig()
        fig.setTitle('Raw PPG')
        addLabels(fig,'time','intensity','-','sec')

        self.plt_r = plot(fig,np.arange(0,5),np.arange(0,5),[255,0,0])
        self.plt_g = plot(fig,np.arange(0,5),np.arange(0,5),[0,255,0])
        self.plt_b = plot(fig,np.arange(0,5),np.arange(0,5),[0,0,255])

        fig_fppg = create_fig()
        fig_fppg.setTitle('Filtered PPG')
        addLabels(fig,'time','intensity','-','sec')
        self.plt_x = plot(fig_fppg,np.arange(0,5),np.arange(0,5),[255,0,0])

        fig_snr = create_fig()
        fig_snr.setTitle('SNR')
        addLabels(fig,'time','SNR','-','sec')
        self.plt_snr = plot(fig_snr,np.arange(0,5),np.arange(0,5),[255,0,0])

        fig_bpm = create_fig()
        fig_bpm.setTitle('Frequency')
        fig_bpm.setXRange(0,300)
        addLabels(fig_bpm,'Frequency','intensity','-','BPM')
        self.plt_bpm = plot(fig_bpm,np.arange(0,5),np.arange(0,5),[255,0,0])

        fig_bpmdt = create_fig()
        fig_bpmdt.setTitle('Hearbeat over time')
        addLabels(fig_bpm,'Frequency','intensity','-','BPM')
        self.plt_bpmdt = plot(fig_bpmdt,np.arange(0,5),np.arange(0,5),[255,0,0])
        layout_upper.addWidget(fig)
        layout_upper.addWidget(fig_fppg)
        layout_lower.addWidget(fig_snr)
        layout_lower.addWidget(fig_bpm)
        layout_lower.addWidget(fig_bpmdt)
        w.setLayout(layout_main)
        timer = QtCore.QTimer()
        timer.start(10)
        timer.timeout.connect(self.update)
        execute_app(self.app,self.w)   

    def update_plots(self):
    
    def update_data(self):
        
        num_frames = self.sensor.rppg.shape[1]
        start = max([num_frames-100,0])
        t = np.arange(num_frames)/self.processor.fs
        rPPG = self.sensor.rppg
        self.plt_r.setData(t[start:num_frames],rPPG[0,start:num_frames])
        self.plt_g.setData(t[start:num_frames],rPPG[1,start:num_frames])
        self.plt_b.setData(t[start:num_frames],rPPG[2,start:num_frames])
        
        if self.processor.enough_samples:
            self.plt_x.setData(t[-300:],self.processor.x_stride_method)
            snr = self.evaluator.snr
            self.plt_snr.setData(t[-min(100,len(snr)):],snr[-min(100,len(snr)):])
            self.plt_bpm.setData(self.f,self.processor.normalized_amplitude)
            bpm_movavg = self.evaluator.bpm
            #bpm_movavg = np.convolve(self.evaluator.bpm, np.ones((100,))/100, mode='valid')
            self.plt_bpmdt.setData(t[-min(200,len(bpm_movavg)):],bpm_movavg[-min(200,len(bpm_movavg)):])
        
