import pygame
import math
import random

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

def collisionCheck():
	for b in bullet.bulletList:
		for a in asteroid.astList:
			if pygame.Rect.colliderect(b.hbox, a.hbox):
				b.removeself()
				a.removeself()

def degToRad(deg):
	return deg*-.0174533
def redrawWindow(surface):
	surface.fill((0,0,0))
	[ast.move() for ast in asteroid.astList]
	[ast.draw(surface) for ast in asteroid.astList]
	[b.move() for b in bullet.bulletList]
	[b.draw(surface) for b in bullet.bulletList]
	pygame.display.update()
def spawnBullet():
	spd = bullSpd
	mousepos = pygame.mouse.get_pos()
	dy = -bulletSpawnCoords["y"] + mousepos[1]
	dx = -bulletSpawnCoords["x"] + mousepos[0]
	bullet(bulletSpawnCoords["x"], bulletSpawnCoords["y"], math.atan2(dy, dx), spd, 5)
def spawnAsteroid():
	randBegX = random.random() * width
	randEndX = random.random() * width
	randSpeed = round(random.random() * 4 + 2)
	dir = math.atan2(height, -randBegX + randEndX)
	asteroid(randBegX, 100, dir, randSpeed, 25)
def removeOutOfBounds():
	for b in bullet.bulletList:
		if b.y > height:
			b.removeself()
	for a in asteroid.astList:
		if a.y > height:
			a.removeself()
def init():
	pygame.init()
	pygame.font.init()
	global width, height, bulletSpawnCoords, bullSpd, win, totalPoints
	global currentPoints
	currentPoints = 0
	totalPoints = 0
	bullSpd = 20
	height = 700
	width = 1000
	bulletSpawnCoords = {"x": width/2, "y":height};
	win = pygame.display.set_mode((width, height))
def main():
	cooldown = 5
	spawnCoolDown = 30
	while True:
		#Kill Switch
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		mousepos = pygame.mouse.get_pos()
		if pygame.mouse.get_pressed()[0] and cooldown <= 0:
			spawnBullet()
			cooldown = 5
		if cooldown >= 0:
			cooldown -= 1
		if spawnCoolDown <= 0:
			spawnAsteroid()
			spawnCoolDown = 10
		else:
			spawnCoolDown -= 1
		collisionCheck()
		redrawWindow(win)
		pygame.time.delay(50)
init()
main()