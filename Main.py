import pygame
import random
pygame.init()
from Player import Player
from Enemy import Enemy
from droped_arrows import Droped_arrows


class Game():
    def __init__(self):
        pygame.init()
        self.Clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000,900))

        self.player = pygame.sprite.GroupSingle(Player())
        self.enemy = pygame.sprite.Group(Enemy())
        self.droped_arrows = pygame.sprite.Group()
        self.my_font = pygame.font.SysFont("Jacquard 12", 39)
        self.enemy.add(Enemy())
        self.amount_of_enemys = 1
        self.run2 = False
        self.score = 0
        self.best_score = 0

    def collison(self):
        
        for arrwos in self.player.sprite.arrwos:
            if pygame.sprite.spritecollide(arrwos, self.enemy, True):
                arrwos.kill()
                self.amount_of_enemys += 0.125
                self.score += 1
                self.droped_arrows.add(Droped_arrows(arrwos.rect.x,arrwos.rect.y))

                
        for enemy in self.enemy:
            if pygame.sprite.spritecollide(enemy,self.player, False):
                self.run2 = False
                self.enemy.empty()
                self.droped_arrows.empty()
                self.player.sprite.amount_of_arrwos = 10
                self.score = 0
                self.amount_of_enemys = 1
                self.player.sprite.rect.x = 500
                self.player.sprite.rect.y = 450
        for droped_arrows in self.droped_arrows:
            if pygame.sprite.spritecollide(droped_arrows, self.player, False):
                one_or_two= random.randint(1,10)
                how_many_arrwos_you_get = 0
                if one_or_two == 1:
                    how_many_arrwos_you_get = 2
                else:
                    how_many_arrwos_you_get = 1
                self.player.sprite.amount_of_arrwos += how_many_arrwos_you_get
                droped_arrows.kill()
        

        if len(self.enemy.sprites()) < self.amount_of_enemys:
            self.enemy.add(Enemy())

        self.handle_enemy_collisions()


    def handle_enemy_collisions(self):
        enemy_list = list(self.enemy)
        for i in range(len(enemy_list)):
            for j in range(i + 1, len(enemy_list)):
                enemy1 = enemy_list[i]
                enemy2 = enemy_list[j]
                if enemy1.rect.colliderect(enemy2.rect):
                    self.resolve_collision(enemy1, enemy2)

    def resolve_collision(self, enemy1, enemy2):
        overlap_x = min(enemy1.rect.right, enemy2.rect.right) - max(enemy1.rect.left, enemy2.rect.left)
        overlap_y = min(enemy1.rect.bottom, enemy2.rect.bottom) - max(enemy1.rect.top, enemy2.rect.top)

        if overlap_x < overlap_y:
            if enemy1.rect.centerx < enemy2.rect.centerx:
                enemy1.rect.x -= overlap_x // 2
                enemy2.rect.x += overlap_x // 2
            else:
                enemy1.rect.x += overlap_x // 2
                enemy2.rect.x -= overlap_x // 2
        else:
            if enemy1.rect.centery < enemy2.rect.centery:
                enemy1.rect.y -= overlap_y // 2
                enemy2.rect.y += overlap_y // 2
            else:
                enemy1.rect.y += overlap_y // 2
                enemy2.rect.y -= overlap_y // 2
        

    def text(self):
        text_surface = self.my_font.render("arrows "+ str(self.player.sprite.amount_of_arrwos), False, (255, 255, 255))
        text_surface2 = self.my_font.render("Score "+ str(self.score), False, (255, 255, 255))
        self.screen.blit(text_surface, (850,0))
        self.screen.blit(text_surface2, (50,0))


    def start_screen(self):
        if self.best_score < self.score:
            self.best_score = self.score

        text = self.my_font.render("Press E to start", False, (255, 255, 255))
        text2 = self.my_font.render("Best Score "+ str(self.best_score), False, (255, 255, 255))
        text3 = self.my_font.render("Move with WASD and shoot the goblins with SPACE", False, (255, 255, 255))
        self.screen.blit(text, (400,350))
        self.screen.blit(text2, (400,450))
        self.screen.blit(text3, (150,550))

        
    def run(self):
        run = True
        while run:
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.run2 = True
                        

            self.screen.fill((0,153,0))
            self.start_screen()

            if self.run2 == True:
                self.screen.fill((0,153,0))
                self.player.draw(self.screen)
                self.enemy.draw(self.screen)
                self.droped_arrows.draw(self.screen)
                self.player.sprite.arrwos.draw(self.screen)
                player_rect = self.player.sprite.rect  
                self.player.update()
                self.enemy.update(player_rect.x,player_rect.y)
                self.collison()
                self.text()
            
            pygame.display.flip()
            self.Clock.tick(60)

    

        
if __name__ == "__main__":
    
    game = Game()
    game.run()
