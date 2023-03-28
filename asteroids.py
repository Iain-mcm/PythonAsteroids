import pygame
import math
import random
from enum import *

class asteroid(object):
	astList = []
	def __init__(self, x, y, d, vel, radius, hp=1):
		self.x = x
		self.y = y
		self.dir = d
		self.vel = vel
		self.radius = radius
		self.hp = hp
		self.initialHp = hp
		self.hbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius * 2, self.radius * 2)
		asteroid.astList.append(self)
	def removeself(self):
		asteroid.astList.remove(self)
	def move(self):
		dx = round(self.vel*math.cos(self.dir))
		dy = round(self.vel*math.sin(self.dir))
		self.x += dx
		self.y += dy
		self.hbox.move_ip(dx, dy)
	def draw(self, surface):
		pygame.draw.circle(surface, (100, 100, 100), (self.x, self.y), self.radius)
class bullet(object):
	bulletList = []
	def __init__(self, x, y, d, vel, radius, dmg=1):
		self.x = x
		self.y = y
		self.dir = d
		self.vel = vel
		self.radius = radius
		self.dmg = dmg
		self.hbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius * 2, self.radius * 2)
		bullet.bulletList.append(self)
	def removeself(self):
		bullet.bulletList.remove(self)
	def move(self):
		dx = round(self.vel*math.cos(self.dir))
		dy = round(self.vel*math.sin(self.dir))
		self.hbox.move_ip(dx, dy)
		self.x += dx
		self.y += dy
	def draw(self, surface):
		pygame.draw.circle(surface, (100, 10, 10), (self.x, self.y), self.radius)
class turret(object):
	turList = []
	def __init__(self, x, y, spd):
		self.x = x
		self.y = y
		self.spd = spd
		turret.turList.append(self)
	def move(self, direction):
		self.x += self.spd*direction
	def draw(self, surface):
		width = 20
		pygame.draw.rect(surface, (0, 0, 100), pygame.Rect(self.x - width/2, self.y-width/2, width, width))
class Direction(IntEnum):
	LEFT = -1
	RIGHT = 1
def collisionCheck():
	for b in bullet.bulletList:
		for a in asteroid.astList:
			if pygame.Rect.colliderect(b.hbox, a.hbox):
				b.removeself()
				a.removeself()
				del b
				del a
				break
def degToRad(deg):
	return deg*-.0174533
def redrawWindow(surface):
	surface.fill((0,0,0))
	[ast.move() for ast in asteroid.astList]
	[ast.draw(surface) for ast in asteroid.astList]
	[b.move() for b in bullet.bulletList]
	[b.draw(surface) for b in bullet.bulletList]
	[t.draw(surface) for t in turret.turList]
	pygame.display.update()
def spawnBullet(spawnX, spawnY):
	spd = bullSpd
	mousepos = pygame.mouse.get_pos()
	dy = -spawnY + mousepos[1]
	dx = -spawnX + mousepos[0]
	bullet(spawnX, spawnY, math.atan2(dy, dx), spd, 5)
def spawnAsteroid():
	randBegX = random.random() * width
	randEndX = random.random() * width
	randSpeed = round(random.random() * 4 + 2)
	dir = math.atan2(height, -randBegX + randEndX)
	asteroid(randBegX, 100, dir, randSpeed, 25)
def removeOutOfBounds():
	for b in bullet.bulletList:
		if b.y < 0:
			b.removeself()
			del b
			break
	for a in asteroid.astList:
		if a.y > height:
			a.removeself()
			del a
			break
def init():
	pygame.init()
	pygame.font.init()
	pygame.key.set_repeat(5, 5)
	global width, height, bulletSpawnCoords, bullSpd, totalPoints
	global currentPoints
	currentPoints = 0
	totalPoints = 0
	bullSpd = 20
	height = 500
	width = 800
	bulletSpawnCoords = {"x": width/2, "y":height};
def main():
	win = pygame.display.set_mode((width, height))
	t = turret(width/2, height, 5)
	cooldown = 5
	spawnCoolDown = 30
	while True:
		#Kill Switch
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		#Shooting:
		mousepos = pygame.mouse.get_pos()
		if pygame.mouse.get_pressed()[0] and cooldown <= 0:
			spawnBullet(t.x, t.y)
			cooldown = 5
		if cooldown >= 0:
			cooldown -= 1
		#Taking input: 
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			t.move(Direction.LEFT)
			print(Direction.LEFT)
		if keys[pygame.K_d]:
			t.move(Direction.RIGHT)
			print(Direction.RIGHT)
		#Spawning: 
		if spawnCoolDown <= 0:
			spawnAsteroid()
			spawnCoolDown = 10
		else:
			spawnCoolDown -= 1
		#Collision Detection:
		collisionCheck()
		removeOutOfBounds()
		#Redraw and waiting:
		redrawWindow(win)
		pygame.time.delay(50)
init()
main()