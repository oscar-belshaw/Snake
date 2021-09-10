import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#This cube class is the crux of the game since both the snake
#and the snacks both inherit from it
class cube(object):
	rows = 20
	w = 500
	def __init__(self, start, dirnx=1, dirny=0, colour=(255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.colour = colour
		
	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
	def draw(self, surface, eyes=False):
		distance = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]
		
		pygame.draw.rect(surface, self.colour, (i*distance+1, j*distance+1, distance-2, distance-2))
		if eyes:
			centre = distance//2
			radius = 3
			circleMiddle = (i*distance+centre-radius, j*distance+8)
			circleMiddle2 = (i*distance + distance - radius*2, j*distance+8)
			pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
			pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius) 
		
class snake(object):
	body = []
	turns = {}
	def __init__(self, colour, pos):
		self.colour = colour
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				
			keys = pygame.key.get_pressed()
			
			#This loop just defines the direction of movement for each arrow key
			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					
				elif keys[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
					
				elif keys[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
		
		#This keeps track of all the turns the snake has made and pops
		#these moves off the stack once all parts of the snake have
		#been moved
		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
				else: c.move(c.dirnx, c.dirny)
	
	#The initital conditions of the snake		
	def reset(self, pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1
		
	#Adds a cube to the snake, inheriting from the previous class	
	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny
		
		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
		
		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy
	
	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)

#This just draws the white grid on the window		
def drawGrid(w, rows, surface):
	sizeBtwn = w // rows
	
	x = 0
	y = 0
	
	for l in range(rows):
		x = x + sizeBtwn
		y = y + sizeBtwn
		
		pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))
		pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))
	pass

#This popylates the window with everything require
#for the game, ie the snake and snacks	
def redrawWindow(surface):
	global rows, width, s, snack
	surface.fill((0, 0, 0))
	s.draw(surface)
	snack.draw(surface)
	drawGrid(width, rows, surface)
	pygame.display.update()
	pass

#This places the snack somewhere randomly on the window
#grid everytime the previous snack was eaten
def randomSnack(rows, item):
	
	positions = item.body
	
	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			continue
		else:
			break
			
	return (x,y)

#Defining the message box for the game over text
def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy
	except:
		pass

#The main game loop
def main():
	global width, rows, s, snack
	width = 500
	rows = 20
	win = pygame.display.set_mode((width, width))
	s = snake((255, 0, 0), (10, 10))
	snack = cube(randomSnack(rows, s), colour = (0,255,0))
	flag = True
	
	clock = pygame.time.Clock()
	
	#This while loops runs to refresh the window everytime the snake moves
	while flag:
		pygame.time.delay(50)
		clock.tick(10)
		s.move()
		#If the snakes head is above a snack then the snack is consumed,
		#the snake grows by 1 unit, and a new random snack is generated
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows, s), colour = (0,255,0))
		
		#If the snakes head occupies the same space as another body part then it
		#is game over, a score is printed (equal to the length of the snake)
		#and a message is displayed, while the snake is reset to it's initial condition
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
				print("Score " + str(len(s.body)))
				message_box("You Lost!", "Play Again?") 
				s.reset((10, 10))
				break
		#The window is redrawn at every instance of a clock tick
		redrawWindow(win)
		
		
	pass

rows = 20
w = 500


cube.rows = rows
cube.w = w

main()
