import wx

import images
from mainController import Controller


class MainSplash(wx.SplashScreen):
    def __init__(self, app=None, parent=None):
        logo = images.getLogoBitmap()
        image = wx.ImageFromBitmap(logo)
        image = image.Scale(64, 64, wx.IMAGE_QUALITY_HIGH)
        logo = wx.BitmapFromImage(image)
        self.app=app

        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 2000 # milliseconds

        wx.SplashScreen.__init__(self, logo, splashStyle,
                                 splashDuration, parent)

        self.SetForegroundColour(wx.BLACK)
        self.Bind(wx.EVT_CLOSE, self.OnExit)


        wx.Yield()

    def OnExit(self, evt):
        self.Hide()
        MyFrame = Controller()
        self.app.SetTopWindow(MyFrame.mainWindow)
        MyFrame.show()
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...