# Importe o módulo pygame
import pygame

# Importe random para números aleatórios
import random

# Importe pygame.locals para fácil acesso as coordenadas chaves
# Atualizado para atender os padrões flake8 e black
from pygame.locals import (
    RLEACCEL,
    K_UP,               # Tecla para cima
    K_DOWN,             # Tecla para baixo
    K_LEFT,             # Tecla para esquerda
    K_RIGHT,            # Tecla para direita
    K_ESCAPE,           # Tecla de escape
    KEYDOWN,            # Qualquer tecla pressionada
    QUIT,               # Tecla de fechar janela
)

# Defina constantes para largura e a altura da tela
SCREEN_WIDTH = 800          # Esta define a largura
SCREEN_HEIGHT = 600         # Esta define a altura

# Defina o objeto jogador extendendo a classe pygame.sprite.Sprite
# A surface desenhada na tela agora vai ser um atributo de 'jogador'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./Images/jet.png").convert()    # define a área do objeto jogador como superfície surf
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)     # define a cor do fundo dessa área
        self.rect = self.surf.get_rect()   # salva essa informação na variável rect

    # Mova o sprite com base nas teclas pressionadas pelo usuário
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Mantenha o jogador na tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# A superfície que você desenha na tela agora é um atributo de 'Enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./Images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Mova o sprite com base na velocidade
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Configuração de sons.
pygame.mixer.init()

# Reproduza música de fundo
pygame.mixer.music.load("./Music/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Carregue todos os arquivos de som
move_up_sound = pygame.mixer.Sound("./Music/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("./Music/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("./Music/Collision.ogg")

# Inicialize o pygame
pygame.init()

# Crie o objeto da tela
# O tamanho da tela é definido pelas constantes SCREEN_WIDTH e SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Defina o objeto 'cloud' com pygame.sprite.Sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("./Images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # A posição inicial é gerada aleatoriamente
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Mova a 'Cloud' com base em uma velocidade constante
    # Remova a 'Cloud' quando ela passar pela borda esquerda da tela
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Crie um evento personalizado para adicionar um novo inimigo
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Variável para manter o loop do jogo
running = True

# Instanciar o jogador. Até aqui, isso é apenas um retângulo.
player = Player()

# Crie grupos para conter sprites inimigos e todos os sprites
# - inimigos são usados ​​para detecção de colisão e atualizações de posição
# - all_sprites é usado para renderização
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Configure o relógio para uma taxa de quadros definida
clock = pygame.time.Clock()

# Loop principal
while running:
    # Veja cada evento na fila de eventos
    for event in pygame.event.get():
        # O jogador pressionou alguma tecla?
        if event.type == KEYDOWN:
            # Foi a tecla ESCAPE? Se sim, para o loop.
            if event.type == K_ESCAPE:
                running = False
        # O jogador clicou o botão de fechar a janela? Se sim, pare o loop.
        elif event.type == QUIT:
            running = False
        
        # Adicionar um novo inimigo?
        elif event.type == ADDENEMY:

            # Crie o novo inimigo e adicione-o aos grupos de sprites
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

            # Adicionar uma nova 'Cloud'?
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Use o conjunto de teclas pressionadas e verifique a entrada do usuário
    pressed_keys = pygame.key.get_pressed()

    # Atualize o sprite do jogador com base nas teclas pressionadas
    player.update(pressed_keys)

    # Atualize a posição dos inimigos e nuvens
    enemies.update()
    clouds.update()

    # Preencha a cor de fundo com o tom de céu
    screen.fill((135, 206, 250))

    # Desenhe todos os sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Verifique se algum inimigo colidiu com o jogador
    if pygame.sprite.spritecollideany(player, enemies):
     # Nesse caso, remova o player e interrompa o loop
        player.kill()
        running = False

    # Atualize o display
    pygame.display.flip()
 
    # Certifique-se de que o programa mantenha uma taxa de 55 quadros por segundo
    clock.tick(55)

    # Verifique se algum inimigo colidiu com o jogador
    if pygame.sprite.spritecollideany(player, enemies):
    # Se sim, remova o player
        player.kill()

        # Pare qualquer som de movimento e reproduza o som de colisão
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()

        # Pare o Loop
        running = False

        # Encerrando o mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()