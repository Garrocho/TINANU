from math import sin, cos, pi

import pygame

displayWidth = 640
displayHeight = 480
fpsLimit = 90

def sinInterpolation(start, end, steps=30):
    values = [start]
    delta = end - start
    for i in range(1, steps):
        n = (pi / 2.0) * (i / float(steps - 1))
        values.append(start + delta * sin(n))
    return values

class RotatingMenu:
    def __init__(self, x, y, radius, arc=pi*2, defaultAngle=0, wrap=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.arc = arc
        self.defaultAngle = defaultAngle
        self.wrap = wrap
        
        self.rotation = 0
        self.rotationTarget = 0
        self.rotationSteps = []
        
        self.items = []
        self.selectedItem = None
        self.selectedItemNumber = 0
    
    def addItem(self, item):
        self.items.append(item)
        if len(self.items) == 1:
            self.selectedItem = item
    
    def selectItem(self, itemNumber):
        if self.wrap == True:
            if itemNumber > len(self.items) - 1: itemNumber = 0
            if itemNumber < 0: itemNumber = len(self.items) - 1
        else:
            itemNumber = min(itemNumber, len(self.items) - 1)
            itemNumber = max(itemNumber, 0)
        
        self.selectedItem.deselect()
        self.selectedItem = self.items[itemNumber]
        self.selectedItem.select()
        
        self.selectedItemNumber = itemNumber
        
        self.rotationTarget = - self.arc * (itemNumber / float(len(self.items) - 1))
        
        self.rotationSteps = sinInterpolation(self.rotation,
                                              self.rotationTarget, 45)
    
    def rotate(self, angle):
        for i in range(len(self.items)):
            item = self.items[i]
            n = i / float(len(self.items) - 1)
            rot = self.defaultAngle + angle + self.arc * n
            
            item.x = self.x + cos(rot) * self.radius
            item.y = self.y + sin(rot) * self.radius
    
    def update(self):
        if len(self.rotationSteps) > 0:
            self.rotation = self.rotationSteps.pop(0)
            self.rotate(self.rotation)
    
    def draw(self, display):
        for item in self.items:
            item.draw(display)

class MenuItem:
    def __init__(self, text="Spam"):
        self.text = text
        
        self.defaultColor = (255,255,255)
        self.selectedColor = (255,0,0)
        self.color = self.defaultColor
        
        self.x = 0
        self.y = 0
        
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, self.color)
        size = self.font.size(self.text)
        self.xOffset = size[0] / 2
        self.yOffset = size[1] / 2
    
    def select(self):
        self.color = self.selectedColor
        self.redrawText()
    
    def deselect(self):
        self.color = self.defaultColor
        self.redrawText()
    
    def redrawText(self):
        self.font = pygame.font.Font(None, 20)
        self.image = self.font.render(self.text, True, self.color)
        size = self.font.size(self.text)
        self.xOffset = size[0] / 2
        self.yOffset = size[1] / 2
    
    def draw(self, display):
        display.blit(self.image, (self.x-self.xOffset, self.y-self.yOffset))

def main():
    pygame.init()
    
    display = pygame.display.set_mode((displayWidth, displayHeight))
    clock = pygame.time.Clock()
    
    menu = RotatingMenu(x=320, y=240, radius=220, arc=pi, defaultAngle=pi/2.0)
    menu.addItem(MenuItem("Iniciar"))
    menu.addItem(MenuItem("Sair"))
    menu.selectItem(0)
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    menu.selectItem(menu.selectedItemNumber + 1)
                if event.key == pygame.K_RIGHT:
                    menu.selectItem(menu.selectedItemNumber - 1)
        
        menu.update()
        display.fill((0,0,0))
        menu.draw(display)
        pygame.display.flip()
        clock.tick(fpsLimit)

if __name__ == "__main__":
    main()
