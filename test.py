from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task.Task import Task
from direct.gui.DirectGui import *
import sys
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject

from extra.terrain import*
from extra.player import*
from extra.keys import*
from extra.sounds import*
#########################Sound Section##################
walksound = base.loader.loadSfx("sounds/run.wav")
gamesound = base.loader.loadSfx("sounds/game-sound.mp3")

############################End Sound Section##############
class Client(DirectObject):
  def __init__(self,p,i):
    self.cManager = QueuedConnectionManager() #Manages connections
    self.cReader = QueuedConnectionReader(self.cManager, 0) #Reads incoming Data
    self.cWriter = ConnectionWriter(self.cManager,0) #Sends Data
    self.port = 8000
    self.ip = "127.0.0.1"
    timeout = False
    self.Connection = self.cManager.openTCPClientConnection(self.ip,self.port,timeout) #Create the connection
    if self.Connection:
      self.cReader.addConnection(self.Connection)  # receive messages from server
    else:
      print ('connection failed')

  def tskReaderPolling(self,m,playerRegulator,chatClass):#this function checks to see if there is any data from the server
    if self.cReader.dataAvailable():
      self.datagram=NetDatagram()  # catch the incoming data in this instance
    # Check the return value; if we were threaded, someone else could have
    # snagged this data before we did
      if self.cReader.getData(self.datagram):
        playerRegulator.ProcessData(self.datagram, m,chatClass)
        self.datagram.clear()
    return Task.cont
   
class PlayerReg(DirectObject): #This class will regulate the players
  def __init__(self):
    self.playerList = []
    self.numofplayers = 0
   
  def ProcessData(self,datagram, m,chatClass):
    #process received data
    self.iterator = PyDatagramIterator(datagram)
    self.type = self.iterator.getString()
    if (self.type == "init"):
      print ("initializing")
      #initialize
      m.setPlayerNum(self.iterator.getUint8())
      self.num = self.iterator.getFloat64()
      for i in range(int(self.num)):
        if (i != m.playernum):
          self.playerList.append(Player())
          self.playerList[i].username = self.iterator.getString()
          self.playerList[i].load()
          self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
          print ("player ", str(i), " initialized")
        else:
          self.playerList.append(Player())
      self.numofplayers = self.num
    if (self.type == "update"):
      self.num = self.iterator.getFloat64()
      if (self.num > self.numofplayers):
        for i in range(int(self.numofplayers)):
          self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['h'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['p'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['r'] = self.iterator.getFloat64()
        for i in range(int(self.numofplayers),int(self.num)):
          if (i != m.playernum):
            self.playerList.append(Player())
            self.playerList[i].load()
            self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
            self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
            self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
            self.playerList[i].currentPos['h'] = self.iterator.getFloat64()
            self.playerList[i].currentPos['p'] = self.iterator.getFloat64()
            self.playerList[i].currentPos['r'] = self.iterator.getFloat64()
          else:
            self.playerList.append(Player())
        self.numofplayers = self.num
      else:
        for i in range(int(self.numofplayers)):
          self.playerList[i].currentPos['x'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['y'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['z'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['h'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['p'] = self.iterator.getFloat64()
          self.playerList[i].currentPos['r'] = self.iterator.getFloat64()
    if (self.type == "chat"):
      self.text = self.iterator.getString()
      chatClass.setText(self.text)
 
  def updatePlayers(self,m):
   
    if (self.numofplayers != 0):
      for k in range(int(self.numofplayers)):
        #As long as the player is not the client put it where the server says
        if(k != m.playernum):
          self.playerList[k].model.setPosHpr(self.playerList[k].currentPos['x'],self.playerList[k].currentPos['y'],self.playerList[k].currentPos['z'],self.playerList[k].currentPos['h'],self.playerList[k].currentPos['p'],self.playerList[k].currentPos['r'])
    return Task.cont




from direct.gui.OnscreenText import OnscreenText 
class Me(DirectObject):
  def __init__(self, terrainClass):
    #####################instructions#########
    # Function to put instructions on the screen.
    def addInstructions(pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                            shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                            pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

    # Function to put title on the screen.
    def addTitle(text):
        return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.07,
                            parent=base.a2dBottomRight, align=TextNode.ARight,
                            pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))
    # Post the instructions
    self.title = addTitle(
        "Panda3D Tutorial: Roaming Ralph (Walking on Uneven Terrain)")
    self.inst1 = addInstructions(0.06, "[ESC]: Quit")
    self.inst2 = addInstructions(0.12, "[Left Arrow]: Rotate Ralph Left")
    self.inst3 = addInstructions(0.18, "[Right Arrow]: Rotate Ralph Right")
    self.inst4 = addInstructions(0.24, "[Up Arrow]: Run Ralph Forward")
    self.inst6 = addInstructions(0.30, "[A]: Rotate Camera Left")
    self.inst7 = addInstructions(0.36, "[S]: Rotate Camera Right")
    ######################end instructions##############
    obj = asd()
    mode = player()
    self.model = mode.model
    self.model.setHpr(90,0,0)
    self.actorHead = self.model.exposeJoint(None, 'modelRoot','Joint8')
    #self.model.setScale(4)
    self.playernum = None
    self.timeSinceLastUpdate = 0
    self.model.reparentTo(render)
    self.model.setScale(0.5)
        # Game state variables
    self.isMoving = False
    self.AnimControl=self.model.getAnimControl('walk')
    self.AnimControl.setPlayRate(0.05)
    self.model.setBlend(frameBlend=1)
    self.model.setPos(244,188,0)
    #STORE TERRAIN SCALE FOR LATER USE#
    self.terrainScale = terrainClass.terrain.getRoot().getSz()

    base.camera.setPos(self.model.getX(), self.model.getY() + 10, 2)

    self.floater = NodePath(PandaNode("floater"))
    self.floater.reparentTo(self.model)
    self.floater.setZ(2.0)
# We will detect the height of the terrain by
# ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.
    self.cTrav = CollisionTraverser()

    self.modelGroundRay = CollisionRay()
    self.modelGroundRay.setOrigin(0, 0, 9)
    self.modelGroundRay.setDirection(0, 0, -1)
    self.modelGroundCol = CollisionNode('ralphRay')
    self.modelGroundCol.addSolid(self.modelGroundRay)
    self.modelGroundCol.setFromCollideMask(CollideMask.bit(0))
    self.modelGroundCol.setIntoCollideMask(CollideMask.allOff())
    self.modelGroundColNp = self.model.attachNewNode(self.modelGroundCol)
    self.modelGroundHandler = CollisionHandlerQueue()
    self.cTrav.addCollider(self.modelGroundColNp, self.modelGroundHandler)

    self.camGroundRay = CollisionRay()
    self.camGroundRay.setOrigin(0, 0, 9)
    self.camGroundRay.setDirection(0, 0, -1)
    self.camGroundCol = CollisionNode('camRay')
    self.camGroundCol.addSolid(self.camGroundRay)
    self.camGroundCol.setFromCollideMask(CollideMask.bit(0))
    self.camGroundCol.setIntoCollideMask(CollideMask.allOff())
    self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
    self.camGroundHandler = CollisionHandlerQueue()
    self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

# Uncomment this line to see the collision rays
    self.modelGroundColNp.show()
    self.camGroundColNp.show()

        # Uncomment this line to show a visual representation of the
        # collisions occuring
    self.cTrav.showCollisions(render)
  def setPlayerNum(self,int):
      self.playernum = int
   
  def move(self, keyClass, terrainClass):


    #self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),self.model.getY()) * self.terrainScale
    #self.camTerrainHeight = terrainClass.terrain.getElevation(camera.getX(),camera.getY()) * self.terrainScale
    self.elapsed = globalClock.getDt()
    #base.camera.lookAt(self.actorHead)
   
    # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
    dt = globalClock.getDt()

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

    if keyClass.buttons["cam-left"]:
        base.camera.setX(base.camera, -20 * dt)
    if keyClass.buttons["cam-right"]:
        base.camera.setX(base.camera, +20 * dt)

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

    startpos = self.model.getPos()

        # If a move-key is pressed, move ralph in the specified direction.

    if keyClass.buttons["left"]:
      self.model.setH(self.model.getH() + 300 * dt)
  
    if keyClass.buttons["right"]:
      self.model.setH(self.model.getH() - 300 * dt)
    if keyClass.buttons["forward"]:
      self.model.setY(self.model, -25 * dt)

        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

    if keyClass.buttons["forward"] or keyClass.buttons["left"] or keyClass.buttons["right"]:
      
      if self.isMoving is False:
          walksound.play()
          self.model.loop("run")
          self.isMoving = True
    else:
      if self.isMoving:
          self.model.stop()
          walksound.stop()
          self.model.pose("walk", 5)
          self.isMoving = False
   
    self.meTerrainHeight = terrainClass.terrain.getElevation(self.model.getX(),self.model.getY()) * self.terrainScale
    self.model.setZ(self.meTerrainHeight )
   
    #CAMERA CONTROL#
   
   # If the camera is too far from ralph, move it closer.
     # If the camera is too close to ralph, move it farther.

    startpos = self.model.getPos()

    camvec = self.model.getPos() - base.camera.getPos()
    camvec.setZ(0)
    camdist = camvec.length()
    camvec.normalize()
    if camdist > 10.0:
        base.camera.setPos(base.camera.getPos() + camvec * (camdist - 10))
        camdist = 10.0
    if camdist < 5.0:
        base.camera.setPos(base.camera.getPos() - camvec * (5 - camdist))
        camdist = 5.0

        # Normally, we would have to call traverse() to check for collisions.
        # However, the class ShowBase that we inherit from has a task to do
        # this for us, if we assign a CollisionTraverser to self.cTrav.
        #self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

    entries = list(self.modelGroundHandler.getEntries())
    entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

    if len(entries) > 0 and entries[0].getIntoNode().getName() == "terrain":
        self.model.setZ(entries[0].getSurfacePoint(render).getZ())
    else:
        self.model.setPos(startpos)

        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.

    entries = list(self.camGroundHandler.getEntries())
    entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

    if len(entries) > 0 and entries[0].getIntoNode().getName() == "terrain":
        base.camera.setZ(entries[0].getSurfacePoint(render).getZ() + 1.0)
    if base.camera.getZ() < self.model.getZ() + 2.0:
        base.camera.setZ(self.model.getZ() + 2.0)

        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
    base.camera.lookAt(self.floater)  
   
    

    return Task.cont
   
class World(DirectObject): #This class will control anything related to the virtual world
  def __init__(self):
    self.timeSinceLastUpdate = 0
  def UpdateWorld(self,meClass,clientClass):
    #get the time since the last framerate
    self.elapsed = globalClock.getDt()
    #add it to the time since we last set our position to where the server thinks we are     
    #add the elapsed time to the time since the last update sent to the server
    self.timeSinceLastUpdate += self.elapsed
    if (self.timeSinceLastUpdate > 0.1):
      self.datagram = PyDatagram()
      self.datagram.addString("positions")
      self.datagram.addFloat64(meClass.model.getX())
      self.datagram.addFloat64(meClass.model.getY())
      self.datagram.addFloat64(meClass.model.getZ())                   
      self.datagram.addFloat64(meClass.model.getH())
      self.datagram.addFloat64(meClass.model.getP())
      self.datagram.addFloat64(meClass.model.getR())
      try:
        clientClass.cWriter.send(self.datagram,clientClass.Connection)
      except:
        print ("No connection to the server. You are in stand alone mode.")
        return Task.done
      self.timeSinceLastUpdate = 0
    return Task.cont



class Player(DirectObject):
  def __init__(self):
    self.currentPos = {'x':244,'y':188,'z':0,'h':0,'p':0,'r':0} #stores rotation too
    self.isMoving = False
    self.username = ""
  def load(self):
    self.model = Actor("models/ralph",
                        {"run": "models/ralph-run",
                          "walk": "models/ralph-walk"})
    self.model.reparentTo(render)
    self.model.setScale(0.5)
    self.isMoving = False
    self.AnimControl=self.model.getAnimControl('walk')
    self.AnimControl.setPlayRate(0.05)
    self.model.setBlend(frameBlend=1)
   
   
class chatRegulator(DirectObject):
  def __init__(self,clientClass,keysClass):
    self.maxMessages = 14
    self.messageList = []
    self.client = clientClass
    self.keys = keysClass
    #for gui debug
    self.accept("p", self.getWidgetTransformsF)
    #Create GUI
    #self.frame =
    self.chatInput = DirectEntry(initialText = "Press 't' or click here to chat",
                                 cursorKeys = 1,
                                 numLines = 1,
                                 command = self.send,
                                 focusInCommand=self.handleTpress,
                                 focusOutCommand = self.resetText,
                                 focus = 0,
                                 width = 20)
    #self.chatInput.setPos(-1.31667,0,-0.97)
    self.chatInput.setScale(0.05)
    self.chatInput.reparentTo(base.a2dBottomLeft)
    self.chatInput.setPos(.05,0,.05)   
   
    self.messages = []
    self.txt = []
    for k in range(14):
      self.txt.append(OnscreenText(mayChange = 1))
      self.messages.append(DirectLabel(activeState = 1, text = "hi"))
      #self.messages[k].setScale(0.0498732)
      #self.messages[k].setPos(-1.31667,0,-0.9)
    self.accept("t",self.handleTpress)
    self.accept("control-t",self.resetText)
    self.calls = 0
  def handleTpress(self):
    if not self.keys.isTyping:
      self.clearText()
   
   
     


  def clearText(self):
    self.chatInput.enterText('')
    self.keys.isTyping = True
    self.chatInput["focus"]=True
  def resetText(self):
    self.chatInput.enterText('')
    self.keys.isTyping = False
  #def leaveText(self):
  #  self.keys.isTyping = False
  def send(self,text):
    self.datagram = PyDatagram()
    self.datagram.addString("chat")
    self.datagram.addString(text)
    self.client.cWriter.send(self.datagram,self.client.Connection)
  def setText(self,text):
    self.index = 0
    #put the messages on screen
    self.messageList.append(text)
    if (len(self.messageList)>14):
      self.messageList.reverse()
      del self.messageList[14]
      self.messageList.reverse()
    for k in self.messageList:
      self.text(k,(-.95,( -.8 + (.06 * self.index ) )),self.index)
      self.index += 1

  def getWidgetTransformsF(self):
    for child in aspect2d.getChildren():
      print (child, "  position = ", child.getPos())
      print (child, "  scale = ", child.getScale())
  def text(self,msg,position,index):
    self.txt[index].destroy()
    self.txt[index] = OnscreenText(text = msg, pos = position,fg=(1,1,1,1),align = TextNode.ALeft, scale = .05,mayChange = 1)
    self.txt[index].reparentTo(base.a2dBottomLeft)
    self.txt[index].setPos(.05,.15+.05*index)
