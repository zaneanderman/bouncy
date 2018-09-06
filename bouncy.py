import pygame
import random
from time import sleep
obstaclespeed=400
crazy=False
direction=1
def main():
	height = 750
	width = 800
	start = False
	f = open("highscore.txt","r+")
	highscore=f.read()
	global obstaclespeed
	global crazy
	player = pygame.image.load("player.png")
	invincible_player = pygame.image.load("invincible_player.png")
	playerect = player.get_rect()
	top_spike = pygame.image.load("spike1.png")
	bottom_spike = pygame.image.load("spike2.png")
	top_spike.set_colorkey((255,255,255))
	bottom_spike.set_colorkey((255,255,255))
	screen = pygame.display.set_mode((width,height))
	pointvalue=1
	invincible=0
	coinimage=pygame.image.load("Coin.png")
	starimage=pygame.image.load("star.png")
	obstacleimage=pygame.image.load("obstacle.png")
	obstacleimage.set_colorkey((255,255,255))
	pygame.init()
	pygame.mixer.quit()
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	q=0
	y=height/2
	x=width/2
	stuff = []
	points=0
	button=pygame.image.load("button.png")
	pygame.event.set_allowed(pygame.QUIT)
	while not start:
		keys = pygame.key.get_pressed()
		mouse=pygame.mouse.get_pressed()
		mousepos=pygame.mouse.get_pos()
		pygame.event.pump()
		screen.fill((0, 0, 255))
		spawnrate = 201
		obstaclespawnrate=spawnrate
		coinspawnrate=spawnrate
		starspawnrate=spawnrate*30
		screen.blit(button, (350, 350))
		screen.blit(button, (500, 350))
		screen.blit(button, (350, 400))
		screen.blit(button, (500, 400))
		textsurface=myfont.render("hard", False, (0, 0, 0))
		screen.blit(textsurface, (500, 350))
		textsurface=myfont.render("easy", False, (0, 0, 0))
		screen.blit(textsurface, (350, 400))
		textsurface=myfont.render("normal", False, (0, 0, 0))
		screen.blit(textsurface, (350, 350))
		textsurface=myfont.render("crazy", False, (0, 0, 0))
		screen.blit(textsurface, (500, 400))
		pygame.display.flip()
		if mouse[0] and mousepos[0]>=350 and mousepos[0]<=400 and mousepos[1]>=350 and mousepos[1]<=380:
			start = True
		elif mouse[0] and mousepos[0]>=500 and mousepos[0]<=550 and mousepos[1]>=350 and mousepos[1]<=380:
			start = True
			spawnrate/=2
		elif mouse[0] and mousepos[0]>=350 and mousepos[0]<=400 and mousepos[1]>=400 and mousepos[1]<=430:
			start = True
			spawnrate*=2
		elif mouse[0] and mousepos[0]>=500 and mousepos[0]<=550 and mousepos[1]>=400 and mousepos[1]<=430:
			start = True
			crazy = True
	pasticks=pygame.time.get_ticks()
	while start:
		screen.fill((255, 0, 0))
		playerect.center=(x, y)
		textsurface = myfont.render('points:%s'%points, False, (0, 0, 0))
		screen.blit(textsurface,(20,20))
		tickdifference=pygame.time.get_ticks()-pasticks
		pygame.time.wait((20-tickdifference))
		pasticks=pygame.time.get_ticks()
		if random.randint(0,int(coinspawnrate)) == 1:
			stuff.append(objects(width-40, random.randint(30, height-30), "coin", coinimage, random.randint(-3, 3)))
		if random.randint(0,int(obstaclespawnrate)) == 1:
			stuff.append(objects(width-40, random.randint(30, height-30), "obstacle", obstacleimage, random.randint(-3, 3)))
		if random.randint(0,int(starspawnrate)) == 1:
			stuff.append(objects(width-40, random.randint(30, height-30), "star", starimage, random.randint(-3, 3)))
		keepstuff=[]
		if invincible<=100:
			screen.blit(player, playerect)
		else:
			screen.blit(invincible_player, playerect)
		if not invincible == 0:
			invincible-=1
		for thing in stuff:
			if intersects(thing, {'x':x,'y':y,'width':player.get_width(),'height':player.get_height()}):
				if thing.otype=="coin":
					points+=pointvalue
				elif thing.otype=="obstacle" and not invincible:
					print("you died!")
					print("you had %s points"%points)
					if float(highscore)<points:
						f.truncate(0)
						f.write("%s"%points)
						highscore=points
					print("the highscore is %s"%highscore)
					exit()
				elif thing.otype=="star":
					invincible=1000
			elif x>=-10:
				keepstuff.append(thing)
			thing.draw(screen)
		stuff=keepstuff
		for i in range(53):
			screen.blit(top_spike, (i*15, 0))
		for j in range(53):
			screen.blit(bottom_spike, (j*15, height-20))
		if pygame.event.poll().type==pygame.QUIT:
			print("you left")
			print("you had %s points"%points)
			exit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			obstaclespeed = 4
			coinspawnrate=101
			obstaclespawnrate=spawnrate/2
			starspawnrate=3000
			pointvalue=1.5
		else:
			obstaclespeed=2
			coinspawnrate=201
			obstaclespawnrate=spawnrate
			starspawnrate=6000
			pointvalue=1
		if keys[pygame.K_LEFT]:
			obstaclespeed = 1
			coinspawnrate*=2
			obstaclespawnrate*=2
			starspawnrate*=2
			pointvalue=0.5
		if keys[pygame.K_UP]:
			y-=6
		else:
			y+=6
		if y <= 35 or y>=height-36:
			print("you died")
			print("you had %s points"%points)
			if float(highscore)<points:
				f.truncate(0)
				f.write("%s"%points)
				highscore=points
			print("the highscore is %s"%highscore)
			exit()
		pygame.display.flip()
class objects():
	def __init__(self, x, y, otype, image, direction):
		self.image=image
		self.direction=direction
		self.rect=self.image.get_rect()
		self.x=x
		self.r=self.image.get_height()/2
		self.y=y
		self.otype=otype
	def draw(self,screen):
		self.rect.center=(self.x, self.y)
		screen.blit(self.image, self.rect)
		self.x-=obstaclespeed
		if crazy:
			self.y+=self.direction
			if self.y >= 730 or self.y <=20:
				self.direction = -self.direction

def intersects(circle, rect):
	dx = abs(circle.x - rect['x'])
	dy = abs(circle.y - rect['y'])

	if (dx > (rect['width']/2 + circle.r)): return False 
	if (dy > (rect['height']/2 + circle.r)): return False 

	if (dx <= (rect['width']/2)): return True  
	if (dy <= (rect['height']/2)): return True 

	cornerDistance_sq = (dx - rect['width']/2)**2 +(dy - rect['height']/2)**2

	return (cornerDistance_sq <= (circle.r**2))


main()