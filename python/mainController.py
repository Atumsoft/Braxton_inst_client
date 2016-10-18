import wx
import subprocess
import os

import datetime


from mainView import MainFrame
import images

RUST_APP_PATH = os.path.normpath("atumate-instrument-brew-gui")
SCAN_ARGS = "-f"
CONNECT_ARGS = "-c %s -o %s -s %s -e %s"  # -c: ip address of instrument -o: output file -s: starting date -e: ending date


class Controller:

    def __init__(self):
        self.mainWindow = MainFrame(None)

        # Setup event bindings
        self.mainWindow.Bind(wx.EVT_MENU, self.onExit, self.mainWindow.menuExit)
        self.mainWindow.Bind(wx.EVT_MENU, self.onScan, self.mainWindow.menuScan)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onExport, self.mainWindow.btnExport)

        # setup params
        curWindowSize = self.mainWindow.GetSize()
        self.mainWindow.SetMaxSize(curWindowSize)
        self.mainWindow.SetMinSize(curWindowSize)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(images.getLogoBitmap())
        self.mainWindow.SetIcon(icon)
        self.mainWindow.SetTitle("Atumate Bridge")

        self.mainWindow.cmbInstruments.SetEditable(False)

        # initialize program by scanning preemptively
        self.onScan()

    def show(self):
        self.mainWindow.Show()

    def onExit(self, event):
        self.mainWindow.Destroy()

    def onScan(self, event=None):
        # TODO: get instruments from UDP scan script

        command = "%s %s" % (RUST_APP_PATH, SCAN_ARGS)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        detectedInstruments, stderr = process.communicate()
        # detectedInstruments = ["test", "test1"]
        print detectedInstruments

        # self.mainWindow.cmbInstruments.Clear()
        # self.mainWindow.cmbInstruments.SetValue("Select an Instrument")
        # for inst in detectedInstruments:
        #     self.mainWindow.cmbInstruments.Append(inst)

    def onExport(self, event):
        startDate = self._wxdate2pydate(self.mainWindow.dpStartDate.GetValue())
        startDate = datetime.datetime.strftime(startDate, "%m/%d/%Y")

        endDate = self._wxdate2pydate(self.mainWindow.dpEndDate.GetValue())
        endDate = datetime.datetime.strftime(endDate, "%m/%d/%Y")

        selectedInst = self.mainWindow.cmbInstruments.GetValue()
        if not selectedInst:
            msgBox = wx.MessageDialog(self.mainWindow, "Please make an instrument selection", "Selection Error", wx.ICON_ERROR)
            msgBox.ShowModal()

        # TODO: call script with dates and instrument as params\

    def _wxdate2pydate(self, date):
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            return datetime.date(*ymd)
        else:
            return None
