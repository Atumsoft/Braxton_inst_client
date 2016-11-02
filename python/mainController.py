import wx
import subprocess
import os
import datetime
import csv

from mainView import MainFrame
import images

RUST_APP_PATH = "atumate-instrument-brew-gui.exe"
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
        # self.mainWindow.SetMaxSize(curWindowSize)
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
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        detectedInstruments, stderr = process.communicate()
        if not detectedInstruments.strip(): return

        self.instDict = {}
        for instInfo in detectedInstruments.split(":"):
            inst, ip = instInfo.split("=>")
            self.instDict[inst] = ip

        self.mainWindow.cmbInstruments.Clear()
        self.mainWindow.cmbInstruments.SetValue("Select an Instrument")
        for inst in self.instDict.keys():
            self.mainWindow.cmbInstruments.Append(inst)

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
        # if "file already exists" in data.lower():
        #     msgBox = wx.MessageDialog(self.mainWindow, data, "File Error", wx.ICON_ERROR)
        #     msgBox.ShowModal()
        #     return

        # dataList = []
        # for row in data.split("\n"):
        #     if row == "Response": continue
        #     if not row: continue
        #     print row
        #     dataList.append(eval(row))

        # # write to csv file
        # with open(outFile, "wb+") as csvFile:
        #     csvWriter = csv.writer(csvFile, delimiter=",")
        #
        #     headers = ["date", "time"] + dataList[0]["info"].keys()
        #     csvWriter.writerow(headers)
        #     for row in dataList:
        #         csvWriter.writerow([row["date"], row["time"]] + row["info"].values())
        #
        # selectedInst = self.mainWindow.cmbInstruments.GetValue()
        # if not selectedInst:
        #     msgBox = wx.MessageDialog(self.mainWindow, "Please make an instrument selection", "Selection Error", wx.ICON_ERROR)
        #     msgBox.ShowModal()
        #
        # subprocess.Popen(outFile, shell=True)


    def _wxdate2pydate(self, date):
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            return datetime.date(*ymd)
        else:
            return None
