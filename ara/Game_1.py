import pygame
import random

win_width = 800
win_height = 640
pygame.init()  # инициализирую pygame
win = pygame.display.set_mode((win_width, win_height)) # Окно игры

# Загрузка .png спрайтов для игры и музыки
player = pygame.image.load('D:\\JustMonika\\_Game\\ara\\cat_right.png') 
icon = pygame.image.load('D:\\JustMonika\\_Game\\ara\\icon_1.png')
pygame.mixer.music.load('D:\\JustMonika\\_Game\\ara\\music.mp3')
pygame.mixer.music.set_volume(0.5)

# health = pygame.transform.scale(image, (30,30)) ИЗМЕНЕНИЕ РАЗМЕРОВ КАРТИНКИ
# Окно игры
pygame.display.set_icon(icon)
pygame.display.set_caption("Бегущие на месте 30 кг сала")
clock = pygame.time.Clock()
# Хар-ка игрока
usr_widht = 120
usr_height = 88
usr_x = 140
usr_y = win_height - usr_height - 35
make_jump = False
jump_count = 15
scores = 0
max_scores = 0



# --------------------------
# Класс отвечающий за кактусы
class Cactus:
	def __init__ (self, x, y, width, height, speed): 
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.speed = speed

	def move(self): # Движение кактуса
		if self.x >= -self.width: # Когда кактус ещё НЕ вышел за пределы экрана
			pygame.draw.rect(win,(0,155,0),(self.x,self.y,self.width,self.height))
			self.x -= self.speed
			return True
		else: # Если кактус вышел за пределы экрана
			self.x = win_width + self.width	+ random.randrange(0,60) # х принимает значение всего экрана и себе(чтобы не было видно, как он появляется из воздуха) + элемент случайности
			return False
	def return_self(self, radius):
		self.x = radius

def create_cactus_arr(array_cactus): # Создание списка кактусов на основе класса
	array_cactus.append(Cactus(win_width+700, win_height-95, 20, 60, 8))
	array_cactus.append(Cactus(win_width+200, win_height-95, 20, 60, 8))
	array_cactus.append(Cactus(win_width+440, win_height-125, 25, 90, 8))
	return array_cactus

def find_radius(array_cactus): # ваще хз как это работает 
	maximum = max(array_cactus[0].x, array_cactus[1].x,array_cactus[2].x)

	if maximum < win_width:
		radius = win_width
		if radius - maximum < 50:
			radius += 150
	else:
		radius = maximum
	choise = random.randrange(0,5)
	if choise == 0:
		radius += random.randrange(10,15)
	else:
		radius += random.randrange(200,350)
	return radius

def draw_array_cactus(array_cactus): # Рисует кактусы
	for cactus in array_cactus:
		check = cactus.move()
		if not check:
			radius = find_radius(array_cactus)
			cactus.return_self(radius)
# ------------------------------
# Класс отвечающий за создание кнопок
class Button:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.inactive_color = (13,162,58)
		self.active_color = (23,204,58)

	def draw(self, x, y, message, font_size = 30, action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if x < mouse[0] < x +self.width:
			if y < mouse[1] < y +self.height:
				pygame.draw.rect(win, self.inactive_color, (x,y, self.width, self.height))
				if click[0] == 1 and action is not None:
					action()
			else:
				pygame.draw.rect(win, self.active_color, (x,y, self.width, self.height))		
		else:
			pygame.draw.rect(win, self.active_color, (x,y, self.width, self.height))
		print_text(message = message, x = x+10, y = y+10, font_size = font_size)


# Отрисовка всех объектов в окне
def drawWindow(array_cactus): 
	global scores
	win.fill((42,121,255)) # Заливка всего экрана  RGB
	pygame.draw.rect(win,(205,155,0),(0,win_height-35,win_width,win_height))
	pygame.draw.circle(win,(255,207,72),(10,10),(50))
	pygame.draw.rect(win,(255,255,255),(100,50,100,40))
	pygame.draw.rect(win,(255,255,255),(350,150,150,100))
	pygame.draw.rect(win,(255,255,255),(700,20,90,50))
	scores += 1
	print_text('Scores:' + str(scores), 600, 20)
	button.draw(20, 100, 'Click', 15, prikol)


	win.blit(player, (usr_x,usr_y)) # Отрисовка картинки 
	draw_array_cactus(array_cactus)
	pygame.display.update() # Смена старого кадра на новый






def jump(): # Прыжок игрока
	global usr_y, jump_count, make_jump	
	if jump_count >= 0:
		usr_y = usr_y - (jump_count ** 2)/9
		jump_count -= 1
	elif jump_count >= -15:
		usr_y = usr_y + (jump_count ** 2)/9
		jump_count -= 1
	else:
		make_jump = False
		jump_count = 15


def check_collision(barriers):
	for barrier in barriers:
		
		# Простая и добрая система поиска коллисион с объектами
		if usr_y + usr_height >= barrier.y:
			if barrier.x <= usr_x <= barrier.x + barrier.width:
				return True
			elif barrier.x <= usr_x + usr_widht <= barrier.x + barrier.width:
				return True

		''' ОЧЕНЬ СЛОЖНАЯ И НЕ РАБОЧАЯ УНЙЯХ
		if barrier.height == 60:
			if not make_jump:
				if barrier.x <= usr_x + usr_widht - 6 <= barrier.x + barrier.width:
					return True
			elif jump_count >= 0:
				if usr_y + usr_height <= barrier.y:
					if barrier.x >= usr_x + usr_widht - 20 >= barrier.x + barrier.width:
						return True
			else:
				if usr_y + usr_height - 5 <= barrier.y:
					if barrier.x >= usr_x + usr_widht - 20 >= barrier.x + barrier.width:
						return True
		else:
			if not make_jump:
				if barrier.x <= usr_x + usr_widht - 6 <= barrier.x + barrier.width:
					return True
			elif jump_count >= 0:
				if usr_y + usr_height <= barrier.y:
					if barrier.x >= usr_x + usr_widht - 20 >= barrier.x + barrier.width:
						return True
			else:
				if usr_y + usr_height - 5 <= barrier.y:
					if barrier.x >= usr_x + usr_widht - 20 >= barrier.x + barrier.width:
						return True'''
			

		
	return False

def pause():
	paused = True

	pygame.mixer.music.pause()
	while paused:
		for event in pygame.event.get(): # Выход из игры
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		print_text('Paused, ENTER to continue',200, 350)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			paused = False
		pygame.display.update()
		clock.tick(15)
	pygame.mixer.music.unpause()

def game_over():
	global max_scores, scores
	stopped = True
	if max_scores < scores:
		max_scores = scores
	while stopped:
		for event in pygame.event.get(): # Выход из игры
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		print_text('Game over. Press ENTER to restart, ESCAPE to exit',50, 350)
		print_text('Max scores: ' + str(max_scores),50, 390)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			scores = 0
			return True
		if keys[pygame.K_ESCAPE]:
			scores = 0
			return False
		pygame.display.update()
		clock.tick(15)

def run_game(): # Игра
	game = True
	global make_jump


	pygame.mixer.music.play(-1)

	array_cactus = []
	create_cactus_arr(array_cactus)


	while game:
		drawWindow(array_cactus)
		clock.tick(30)


		for event in pygame.event.get(): # Выход из игры
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		keys = pygame.key.get_pressed() # Считывать все клавишы во время цикла
		if keys[pygame.K_SPACE]:
			make_jump = True
		if keys[pygame.K_ESCAPE]:
				pause()
		if make_jump:
			jump() 
		if check_collision(array_cactus):
			pygame.mixer.music.pause()
			game = False
	return game_over()

def show_menu():
	show = True
	start_button = Button(300, 70)
	while show:
		clock.tick(60)
		for event in pygame.event.get(): # Выход из игры
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		win.fill((255,255,255))
		start_button.draw(200, 200, 'Start game', 50 , main_game)
		pygame.display.update()

def print_text(message, x, y, font_color = (0,0,0), font_type = 'D:\\JustMonika\\_Game\\ara\\langue.ttf', font_size = 30):
	font_type = pygame.font.Font(font_type, font_size)
	text = font_type.render(message, True, font_color)
	win.blit(text, (x, y))

def main_game():
	global make_jump, jump_count, usr_y

	while run_game():
		make_jump = False
		jump_count = 15
		usr_y = win_height - usr_height - 35




button = Button(100,50)


def prikol():
	global usr_y
	usr_y -= 10




show_menu()
pygame.quit()
quit()



