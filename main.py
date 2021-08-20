import pygame
from pygame.locals import *
import time
from random import randint

class Snake:
    def __init__(self,surface):
        self.length=1
        self.score=0
        self.border = pygame.image.load(".resources/border.png").convert()
        self.background = pygame.image.load(".resources/background_image.jpg").convert()
        self.apple = pygame.image.load(".resources/apple.png").convert()
        self.head = pygame.image.load(".resources/head.png").convert()
        self.body = pygame.image.load(".resources/body.png").convert()
        self.x=[240]
        self.y=[240]
        self.generate_apple()
        self.notallowed=[(K_DOWN,K_UP),(K_UP,K_DOWN),(K_LEFT,K_RIGHT),(K_RIGHT,K_LEFT)]
        self.surface=surface
        self.direction="self.y[0]-=40"
        self.move=K_UP
        self.directions={
            K_UP:"self.y[0]-=40",
            K_DOWN:"self.y[0]+=40",
            K_RIGHT:"self.x[0]+=40",
            K_LEFT:"self.x[0]-=40",
        }
        
    def inside(self,a,b,m):
        return (a,b) in [(self.x[i], self.y[i]) for i in range(m,self.length)]

    def generate_apple(self):
        while True:
            self.apple_x=randint(1,20)*40
            self.apple_y=randint(1,12)*40
            if not self.inside(self.apple_x,self.apple_y,0):
                break

    def draw(self):
        font= pygame.font.SysFont('arial',30)
        self.surface.fill((255,255,255))
        self.surface.blit(self.border,(0,0))
        self.surface.blit(self.background,(40,40))
        self.surface.blit(self.apple,(self.apple_x,self.apple_y))
        self.surface.blit(self.head,(self.x[0],self.y[0]))
        for i in range(1,self.length):
                self.surface.blit(self.body,(self.x[i],self.y[i]))
        score = font.render(f"Score: {self.score}", True, (200,200,200))
        self.surface.blit(score,(40,40))
        pygame.display.flip()

    def movement(self,move):
        if not((self.move,move) in self.notallowed):
            self.direction=self.directions[move]
        self.move=move
    
    def walk(self):
        new_block_x=self.x[self.length-1]
        new_block_y=self.y[self.length-1]
        for i in range(self.length-1,0,-1):
            self.y[i]=self.y[i-1]
            self.x[i]=self.x[i-1]
        exec(self.direction)
        if self.inside(self.x[0],self.y[0],1) or (self.x[0]<40 or self.x[0]>800) or (self.y[0]<40 or self.y[0]>480) :
            sound=pygame.mixer.Sound(".resources/Lego yoda death sound.mp3")
            pygame.mixer.Sound.play(sound)
            return True
        self.draw()
        if (self.x[0],self.y[0])==(self.apple_x,self.apple_y):
            sound=pygame.mixer.Sound(".resources/Noice Sound Effect.mp3")
            pygame.mixer.Sound.play(sound)
            self.generate_apple()
            self.x.append(new_block_x)
            self.y.append(new_block_y)
            self.length+=1
            self.score+=1
        return False

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((880,560))
        self.surface.fill((255,255,255))
        self.snake = Snake(self.surface)
        pygame.display.set_caption("Alpha's Retro Snake")
        pygame.display.set_icon(self.snake.apple)

        self.snake.draw()
        

    def show_score(self):
        game_over=pygame.image.load(".resources/gameover.jpg").convert()
        self.surface.blit(game_over,(40,40))
        font= pygame.font.SysFont('arial',30)
        score = font.render(f"The game has ended and your score is: {self.snake.score}", True, (200,200,200))
        request= font.render(f"Press Enter to play again or Escape to Quit",True,(200,200,200))
        self.snake.surface.blit(score,(150,300))
        self.snake.surface.blit(request,(150,350))
        pygame.display.flip()


    
    def run(self):
        running=True
        pause=False
        while running:
            for event in pygame.event.get():
                key=K_UP
                if event.type == KEYDOWN:
                    key=event.key
                    if event.key in (K_DOWN,K_UP,K_RIGHT,K_LEFT):
                        self.snake.movement(event.key)
                        break
                    elif event.key == K_ESCAPE:
                        running=False
                if event.type == QUIT:
                    running=False
            if not pause:
                pause=self.snake.walk()
            else:
                self.show_score()
                if key==K_RETURN or key==K_d:
                    game=Game()
                    game.run()
                    quit()
            time.sleep(0.1)




if __name__ == "__main__":
    game=Game()
    sound=pygame.mixer.Sound(".resources\PINK GUY - SMD.mp3")
    pygame.mixer.Sound.play(sound,-1)
    game.run()


            