from PyQt5 import QtGui  
from PyQt5 import QtCore  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from util.qt_util import *
from util.pyqtgraph_util import *


class Plotter():
    def __init__(self):
        app,w = create_basic_app()

        layout_main = QVBoxLayout()
        layout_lower = QHBoxLayout()
        layout_upper = QHBoxLayout()
        
        layout_main.addLayout(layout_lower)
        layout_main.addLayout(layout_upper)

        fig = create_fig()
        fig.setTitle('rPPG')
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
        plt_x = plot(fig_fppg,np.arange(0,5),np.arange(0,5),[255,0,0])

        fig_bpm = create_fig()
        fig_bpm.setTitle('Frequency')
        fig_bpm.setXRange(0,300)
        addLabels(fig_bpm,'Frequency','intensity','-','BPM')
        plt_bpm = plot(fig_bpm,np.arange(0,5),np.arange(0,5),[255,0,0])


        layout_upper.addWidget(fig)
        layout_upper.addWidget(fig_fppg)

        layout_lower.addWidget(fig_snr)
        layout_lower.addWidget(fig_bpm)