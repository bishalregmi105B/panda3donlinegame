from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from direct.gui.DirectGui import *
class asd:
  def __init__(self):
    self.terrain = GeoMipTerrain("mySimpleTerrain")
    self.terrain.setHeightfield(Filename("Heightmap.png"))
    self.terrain.setColorMap(Filename("terrain.bmp"))  #pjb comment this line out if you want to set texture directly
    #myTexture = loader.loadTexture("terrain.bmp") #pjb UNcomment this line out if you want to set texture directly
    self.terrain.setBlockSize(40)
    self.terrain.setBruteforce(True)
    self.terrain.setNear(40)
    self.terrain.setFar(100)
    self.terrain.setFocalPoint(base.camera)
    self.terrain.getRoot().setSz(10)
    self.time = 0
    self.elapsed = 0
    self.terrain.getRoot().reparentTo(render)
    self.terrain.generate()
    #self.terrain.getRoot().setTexture(myTexture) #pjb UNcomment this line out if you want to set texture directly
    #taskMgr.doMethodLater(5, self.updateTerrain, 'Update the Terrain')
    #taskMgr.add(self.updateTerrain, "update")
   
  def updateTerrain(self,task):
    self.elapsed = globalClock.getDt()
    self.time += self.elapsed
    if (self.time > 5):
      self.terrain.update()
      self.time = 0
    return Task.again
