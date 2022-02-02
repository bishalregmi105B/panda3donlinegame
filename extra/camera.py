from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task.Task import Task
from direct.gui.DirectGui import *
import sys
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

class camera():
    def __init__(self):
        self.focus = LVector3(55, -55, 20)
        self.heading = 180
        self.pitch = 0
        self.mouseX = 0
        self.mouseY = 0
        self.last = 0
        self.mousebtn = [0, 0, 0]
    def controlCamera(self, task):
       # figure out how much the mouse has moved (in pixels)
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2
        if self.pitch < -45:
            self.pitch = -45
        if self.pitch > 45:
            self.pitch = 45
        base.camera.setHpr(self.heading, self.pitch, 0)
        dir = base.camera.getMat().getRow3(1)
        elapsed = task.time - self.last
        if self.last == 0:
            elapsed = 0
        if self.mousebtn[0]:
            self.focus = self.focus + dir * elapsed * 30
        if self.mousebtn[1] or self.mousebtn[2]:
            self.focus = self.focus - dir * elapsed * 30
        base.camera.setPos(self.focus - (dir * 5))
        if base.camera.getX() < -59.0:
            base.camera.setX(-59)
        if base.camera.getX() > 59.0:
            base.camera.setX(59)
        if base.camera.getY() < -59.0:
            base.camera.setY(-59)
        if base.camera.getY() > 59.0:
            base.camera.setY(59)
        if base.camera.getZ() < 5.0:
            base.camera.setZ(5)
        if base.camera.getZ() > 45.0:
            base.camera.setZ(45)
        self.focus = base.camera.getPos() + (dir * 5)
        self.last = task.time

          
        return Task.cont
