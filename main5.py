from pygame import *

# parent class for sprites
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (wight, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

# game scene
back = (50, 50, 50)
win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
window.fill(back)

# flags
game = True
finish = False
start_game = False
clock = time.Clock()
FPS = 60

# creating ball and paddles
racket1 = Player('board.png', 30, 200, 5, 20, 100)
racket2 = Player('board.png', win_width - 50, 200, 5, 20, 100)
ball = GameSprite('ball.png', win_width // 2 - 25, win_height // 2 - 25, 5, 50, 50)

# game font and score
font.init()
font = font.Font(None, 50)
player1_winner = font.render('Player 1 Winner!', True, (0, 255, 0))
player2_winner = font.render('Player 2 Winner!', True, (0, 255, 0))
play_again_text = font.render('Play Again', True, (255, 255, 255))

player1_score = 0
player2_score = 0
max_score = 5

# ball speed
speed_x = 4
speed_y = 4

# button settings
button_rect = Rect(win_width // 2 - 100, win_height // 2 + 50, 200, 50)

# Function to display the score
def display_score():
    score_text = font.render(f"{player1_score} - {player2_score}", True, (255, 255, 255))
    window.blit(score_text, (win_width // 2 - 30, 10))

# Function to display the Play Again button
def display_button():
    draw.rect(window, (0, 0, 0), button_rect)
    window.blit(play_again_text, (button_rect.x + 20, button_rect.y + 10))

# Function to reset the game
def reset_game():
    global player1_score, player2_score, finish, start_game
    player1_score = 0
    player2_score = 0
    finish = False
    start_game = False
    ball.rect.x, ball.rect.y = win_width // 2 - 25, win_height // 2 - 25

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and finish:
            if button_rect.collidepoint(e.pos):
                reset_game()

    if not finish:
        window.fill(back)
        
        racket1.update_l()
        racket2.update_r()
        
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Ball collision with top and bottom walls
        if ball.rect.y <= 0 or ball.rect.y >= win_height - ball.rect.height:
            speed_y *= -1

        # Ball collision with paddles
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        # Ball goes out of bounds
        if ball.rect.x < 0:
            player2_score += 1
            ball.rect.x, ball.rect.y = win_width // 2 - 25, win_height // 2 - 25

        if ball.rect.x > win_width:
            player1_score += 1
            ball.rect.x, ball.rect.y = win_width // 2 - 25, win_height // 2 - 25

        # Check for winning condition
        if player1_score >= max_score:
            finish = True
            window.fill(back)
            window.blit(player1_winner, (win_width // 2 - 150, win_height // 2 - 40))
            display_button()

        if player2_score >= max_score:
            finish = True
            window.fill(back)
            window.blit(player2_winner, (win_width // 2 - 150, win_height // 2 - 40))
            display_button()

        racket1.reset()
        racket2.reset()
        ball.reset()
        display_score()
    
    elif finish:
        display_button()

    display.update()
    clock.tick(FPS)
