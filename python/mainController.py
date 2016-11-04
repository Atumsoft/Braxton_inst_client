import wx
import subprocess
import os
import datetime
import sys

import wx.lib.agw.advancedsplash as splash

import thread

from mainView import MainFrame
import images


if "linux" in sys.platform:
    RUST_APP_PATH = "./atumate-instrument-brew-gui"
else:
    RUST_APP_PATH = "atumate-instrument-brew-gui.exe"
SCAN_ARGS = "-f"
CONNECT_ARGS = "-c %s -o %s -s %s -e %s"  # -c: ip address of instrument -o: output file -s: starting date -e: ending date


class Controller:

    def __init__(self):
        self.mainWindow = MainFrame(None)
        logo = images.getAtumate_logo_socialBitmap()
        self.splashscreen = splash.AdvancedSplash(self.mainWindow, bitmap=logo, agwStyle=splash.AS_CENTER_ON_SCREEN)  # Try this later: | splash.AS_SHADOW_BITMAP, shadowcolour=wx.BLACK)
        self.splashscreen.Hide()
        self.splashscreen.Bind(wx.EVT_MOUSE_EVENTS, self.onSplashMouse)
        self.splashscreen.SetText("Scanning network, please wait...")
        self.splashscreen.SetTextColour(wx.WHITE)
        self.splashscreen.SetTextPosition(((logo.GetWidth()/2)-len(self.splashscreen.GetText())*3.7, logo.GetHeight()-28))
        self.splashscreen.Show()
        self.splashscreen.SetFocus()
        self.splashscreenShown = True

        # Setup event bindings
        self.mainWindow.Bind(wx.EVT_MENU, self.onExit, self.mainWindow.menuExit)
        self.mainWindow.Bind(wx.EVT_MENU, self.onScan, self.mainWindow.menuScan)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onExport, self.mainWindow.btnExport)

        # setup params
        curWindowSize = self.mainWindow.GetSize()
        # self.mainWindow.SetMaxSize(curWindowSize)
        self.mainWindow.SetMinSize(curWindowSize)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(images.getLogoBitmap())
        self.mainWindow.SetIcon(icon)
        self.mainWindow.SetTitle("Atumate Bridge")

        self.mainWindow.cmbInstruments.SetEditable(False)

        # initialize program by scanning preemptively
        thread.start_new_thread(self.onScan, tuple())

    def show(self):
        self.mainWindow.Show()

    def onSplashMouse(self, event):
        pass

    def onExit(self, event):
        self.mainWindow.Destroy()

    def hideSplash(self, event=None):
        self.splashscreen.Hide()
        self.mainWindow.SetFocus()
        self.mainWindow.Show()
        self.splashscreenShown = False

    def onScan(self, event=None):
        command = "%s %s" % (RUST_APP_PATH, SCAN_ARGS)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        detectedInstruments, stderr = process.communicate()
        if detectedInstruments.strip():
            self.instDict = {}
            for instInfo in detectedInstruments.split(":"):
                inst, ip = instInfo.split("=>")
                self.instDict[inst] = ip

            self.mainWindow.cmbInstruments.Clear()
            self.mainWindow.cmbInstruments.SetValue("Select an Instrument")
            for inst in self.instDict.keys():
                self.mainWindow.cmbInstruments.Append(inst)

        if self.splashscreenShown:
            wx.CallAfter(self.hideSplash)

    def onExport(self, event):
        filePicker = wx.FileDialog(self.mainWindow,
                                   "Select Save Location",
                                   os.getcwd(),
                                  "output.csv",
                                   "CSV files (*.csv)|*.csv|All files (*.*)|*.*",
                                   wx.FD_SAVE)
        if filePicker.ShowModal() == wx.ID_CANCEL: return
        outFile = filePicker.GetPath()

        startDate = self._wxdate2pydate(self.mainWindow.dpStartDate.GetValue())
        startDate = datetime.datetime.strftime(startDate, "%m/%d/%Y")

        endDate = self._wxdate2pydate(self.mainWindow.dpEndDate.GetValue())
        endDate = datetime.datetime.strftime(endDate, "%m/%d/%Y")

        selectedInstIp = self.instDict.get(self.mainWindow.cmbInstruments.GetValue())

        if not selectedInstIp:
            msgBox = wx.MessageDialog(self.mainWindow, "Please select an instrument to pull data from", "Selection Error", wx.ICON_ERROR)
            msgBox.ShowModal()
            return

        command = "%s %s" % (RUST_APP_PATH, CONNECT_ARGS % (selectedInstIp.strip(), outFile, startDate, endDate))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        data, stderr = process.communicate()

    def _wxdate2pydate(self, date):
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            return datetime.date(*ymd)
        else:
            return None
