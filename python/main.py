import wx


from mainSplash import MainSplash


if __name__ == '__main__':
    app = wx.App()
    controller = MainSplash(app=app)
    app.MainLoop()