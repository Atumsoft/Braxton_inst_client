import wx


from mainController import Controller


if __name__ == '__main__':
    app = wx.App()
    controller = Controller()
    controller.show()
    app.MainLoop()