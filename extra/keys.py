from direct.showbase.DirectObject import DirectObject
import sys
class Keys(DirectObject):
  def __init__(self):
    self.buttons= {
            "left": 0, "right": 0,"cam":0, "forward":0, "cam-left": 0,"cam-up":0, "cam-right": 0,"cam-down": 0}

    self.isTyping = False
    self.accept("escape", sys.exit)
    self.accept("arrow_left", self.setKey, ["left", True])
    self.accept("arrow_right", self.setKey, ["right", True])
    self.accept("arrow_up", self.setKey, ["forward", True])
    self.accept("a", self.setKey, ["cam-left", True])
    self.accept("s", self.setKey, ["cam-right", True])
    self.accept("1", self.setKey, ["cam-down", True])
    self.accept("2", self.setKey, ["cam-up", True])
    self.accept("arrow_left-up", self.setKey, ["left", False])
    self.accept("arrow_right-up", self.setKey, ["right", False])
    self.accept("arrow_up-up", self.setKey, ["forward", False])
    self.accept("a-up", self.setKey, ["cam-left", False])
    self.accept("s-up", self.setKey, ["cam-right", False])
    self.accept("1-up", self.setKey, ["cam-down", False])
    self.accept("2-up", self.setKey, ["cam-up", False])

    #self.accept("a", base.oobe)
# Records the state of the arrow keys

  def setKey(self, key, value):
      self.buttons[key] = value

  def autoRun(self):
    if not self.buttons["autoRun"]:
      self.setKey("autoRun", 1)
      self.setKey("forward" , 1)
    else:
      self.setKey("autoRun", 0)
      self.setKey("forward" , 0)
     
 
  def toggleCam(self):
    if self.buttons["cam"] == 1:
      self.setKey("cam",2)
    elif self.buttons["cam"] == 0:
      self.setKey("cam",1)
    else:
      self.setKey("cam",0)
   
 
