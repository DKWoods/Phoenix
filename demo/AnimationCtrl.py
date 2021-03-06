#!/usr/bin/env python

import wx
from wx.adv import Animation

UseNative = True
if UseNative:
    # Use the native classes, if the platform has a native widget. It will fall
    # back to the generic version if there isn't a native one available.
    from wx.adv import AnimationCtrl
else:
    # Or we can force use of the generic widget on all platforms
    from wx.adv import GenericAnimationCtrl as AnimationCtrl

from Main import opj

GIFNames = [
    'bitmaps/AG00178_.gif',
    'bitmaps/BD13656_.gif',
    'bitmaps/AG00185_.gif',
    'bitmaps/AG00039_.gif',
    'bitmaps/AG00183_.gif',
    'bitmaps/AG00028_.gif',
    ]

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)

        for name in GIFNames:
            # There are a few usage patterns for creating the control and the
            # animation object. They're more-or-less equivalent, but if you have
            # non-standard needs in your application then one pattern may make
            # more sense for you to use.
            if False:
                # If you need a separate animation object then you can have the
                # control create one for you.
                ctrl = AnimationCtrl(self)
                ani = ctrl.CreateAnimation()
                ani.LoadFile(opj(name))
                ctrl.SetAnimation(ani)
            elif False:
                # if you need to have the animation object before the control is
                # created, then you can do it like this:
                ani = AnimationCtrl.CreateCompatibleAnimation()
                ani.LoadFile(opj(name))
                ctrl = AnimationCtrl(self, -1, ani)
            else:
                # Or you can keep it simple and just have the control make and
                # use its own animation object internally.
                ctrl = AnimationCtrl(self)
                ctrl.LoadFile(opj(name))

            ctrl.SetBackgroundColour(self.GetBackgroundColour())
            ctrl.Play()
            sizer.Add(ctrl, 0, wx.ALL, 10)

        if UseNative and 'wxGTK' in wx.PlatformInfo:
            # See comment in updateBestSizes below
            wx.CallAfter(self.updateBestSizes)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(border)

    def updateBestSizes(self):
        # The native control on GTK is not able to set the BestSize of the
        # animation widget until after it has finished loading the animation
        # images. So here we will invalidate the initial best size, so it will
        # be recalculated on the next layout of the sizer.
        for child in self.GetChildren():
            if isinstance(child, AnimationCtrl):
                child.InvalidateBestSize()
        self.Layout()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.adv.AnimationCtrl</center></h2>

wx.adv.AnimationCtrl is like a wx.StaticBitmap but is able to
display an animation by extracting frames from a multi-image GIF file.

</body></html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

