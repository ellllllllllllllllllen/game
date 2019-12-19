
import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Burning forest')

pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.3)


icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

fire_img = [pygame.image.load('0.png'), pygame.image.load('1.png'), pygame.image.load('2.png')]
fire_options = [67, 444, 32, 410, 46, 420]

stone_img = [pygame.image.load('stone1.png'), pygame.image.load('stone2.png')]
cloud_img = [pygame.image.load('cloud1.png'), pygame.image.load('cloud2.png')]

player_img = [pygame.image.load('player0.png'), pygame.image.load('player1.png'), pygame.image.load('player2.png'), pygame.image.load('player3.png'), pygame.image.load('player4.png')]

health_img = pygame.image.load('heart.png')
health_img = pygame.transform.scale(health_img, (30, 26))
heart_img = pygame.image.load('heart.png')
heart_img = pygame.transform.scale(heart_img, (30, 26))
img_counter = 0

health = 2

class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width

        self.speed = speed
        self.image = image
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            
            self.x -= self.speed
            return True
        else:
            #self.x = display_width + 100 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (255, 188, 182)
        self.active_color = (255, 188, 182)
        
    def draw(self, x, y, message, action = None, font_size = 30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                #pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

       # print_text(message, x + 10, y + 10)
        print_text(message = message, x = x + 10, y = y + 10, font_size = font_size)

usr_width = 40
usr_height = 90
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

fire_width = 20
fire_height = 70
fire_x = display_width -50
fire_y = display_height - fire_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30


scores = 0
max_scores = 0
max_above = 0

def show_menu():
    menu_bckgr = pygame.image.load('main.png')

    start_btn = Button(260, 60)
    quit_btn = Button(120, 60)
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(menu_bckgr, (0, 0))
        start_btn.draw(130, 500, 'Start game', start_game, 40)
        quit_btn.draw(530, 500, 'Quit', quit, 40)
        pygame.display.update()
        clock.tick(60)
def start_game():
    global scores, make_jump, jump_counter, usr_y, health

    while game_cycle():
        cores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100
        health = 2

above_fire = False

def game_cycle():
    global make_jump

    pygame.mixer.music.play(-1)

    game = True

    fire_arr = []
    create_fire_arr(fire_arr)

    land = pygame.image.load('land11.png')

    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, health_img, 4)

    button = Button(100, 50)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        if keys[pygame.K_ESCAPE]:
            pause()



        if make_jump:
            jump()

        
        count_scores(fire_arr)

        display.blit(land, (0, 0))

        print_text('Scores: ' + str(scores), 580, 10)
        #button.draw(20, 100, 'wow')
        
        draw_array(fire_arr)

        move_objects(stone, cloud)


        draw_player()

        if check_collision(fire_arr):
            #pygame.mixer.music.stop()
            #if not check_health():
            game = False

        heart.move()
        hearts_plus(heart)

        show_health()

        pygame.display.update()
        clock.tick(80)

    return game_over()

def jump():
    global usr_y, make_jump, jump_counter
    if jump_counter >= - 30:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False

def create_fire_arr(array):
    choice = random.randrange(0, 3)
    img = fire_img[choice]
    width = fire_options[choice * 2]
    height = fire_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = fire_img[choice]
    width = fire_options[choice * 2]
    height = fire_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = fire_img[choice]
    width = fire_options[choice * 2]
    height = fire_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)
    return  radius


def draw_array(array):
    for fire in array:
        check = fire.move()
        if not check:
            objects_return(array, fire)
            #radius = find_radius(array)

            #choice = random.randrange(0, 3)
            #img = fire_img[choice]
            #width = fire_options[choice * 2]
            #height = fire_options[choice * 2 + 1]

            #fire.return_self(radius, height, width, img)

def objects_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = fire_img[choice]
    width = fire_options[choice * 2]
    height = fire_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)

def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4 )
    cloud = Object(display_width, 80, 70, img_of_cloud, 2 )

    return stone, cloud

def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), 10, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), 100, img_of_cloud)

def draw_player():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(player_img[img_counter // 5], (usr_x, usr_y))
    img_counter += 1

def print_text(message, x, y, font_color = (84, 1, 50), font_type = '18046.ttf', font_size = 36):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

def pause():
    paused = True

    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press enter to continue', 90, 100)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()

def check_collision(barriers):
    for barrier in barriers:

        if barrier.y == 444:    #little fire
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width - 10:
                    if check_health():
                        objects_return(barriers, barrier)
                        return False
                    else:
                        return True

            elif jump_counter >= 0:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():
                            objects_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                       if check_health():
                            objects_return(barriers, barrier)
                            return False
                       else:
                            return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 10 <= barrier.x + barrier.width:
                    if check_health():
                        objects_return(barriers, barrier)
                        return False
                    else:
                        return True

            elif jump_counter == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                        if check_health():
                            objects_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter >= -1:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():
                            objects_return(barriers, barrier)
                            return False
                        else:
                            return True

                else:
                    if usr_y + usr_height - 10 >= barrier.y:
                        if barrier.x <= usr_x + 5 <= barrier.x + barrier.width:
                            if check_health():
                                objects_return(barriers, barrier)
                                return False
                            else:
                                return True


        '''if usr_y + usr_height >= barrier.y:
            if barrier.x <= usr_x <= barrier.x + barrier.width:
                return True
            elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                return True'''
    return False
def count_scores(barriers):
    global scores, max_above
    above_fire = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_fire += 1
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:   
                    above_fire += 1

        max_above = max(max_above, above_fire)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores
    stoped = True
    while stoped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over!', 290, 100)
        print_text('\nPress enter to play again. Esc to exit', 15, 150)
        print_text('Max scores: ' + str(max_scores), 250, 250)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)

def show_health():
    global health
    show = 0
    x = 20
    while show != health:
        display.blit(health_img, (x, 20))
        x += 40
        show += 1

def check_health():
    global health
    health -= 1
    if health == 0:
        #game_over()
        return False
    else:
        return True

def hearts_plus(heart):
    global health, usr_x, usr_y, usr_width, usr_height
    if usr_x <= heart.x <= usr_x + usr_width:
        if usr_y <= heart.y <= usr_y + usr_height:
            if health < 5:
                health += 1
            radius = display_width + random.randrange(500, 1700)
            heart.return_self(radius, heart.y, heart.width, heart_img)


show_menu()


pygame.quit()
quit()