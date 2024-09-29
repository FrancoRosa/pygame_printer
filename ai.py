import pygame 
import sys 


# initializing the constructor 
pygame.init() 

# sizes
width=1280
height=720
res = (width,height) 

# opens up a window 
screen = pygame.display.set_mode(res) 

# colors
white = (255,255,255) 
gray = (170,170,170) 
dark = (100,100,100) 
light_blue = (173,216,230) 

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 

# rendering a text written in 
# this font 
text = smallfont.render('Print!', True, white) 
screen.fill(light_blue) 

bw = 100
bh = 40    
bx = width/2 - bw/2
by = height - bh/2 -100

# superimposing the text onto our button 

image = pygame.image.load('sample_image.png') 
while True: 
	mouse = pygame.mouse.get_pos() 
	# changes to lighter shade 
	if bx <= mouse[0] <= bx+bw and by <= mouse[1] <= by+bh: 
		pygame.draw.rect(screen,gray,[bx,by,bw,bh]) 
		
	else: 
		pygame.draw.rect(screen,dark,[bx,by,bw,bh]) 
	
	screen.blit(text , (bx + 15, by + 10)) 
	pygame.display.update()
 
	for ev in pygame.event.get(): 
		if ev.type == pygame.QUIT: 
			pygame.quit() 
			
		if ev.type == pygame.MOUSEBUTTONDOWN: 
			if bx <= mouse[0] <= bx+bw and by <= mouse[1] <= by+bh: 
				pygame.quit() 