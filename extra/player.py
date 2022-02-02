from direct.actor.Actor import Actor
class player:
    def __init__(self):
        self.model = Actor("models/ralph",
                        {"run": "models/ralph-run",
                          "walk": "models/ralph-walk"})

