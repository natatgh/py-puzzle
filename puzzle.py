import pygame
import random
import sys
import time
import numpy as np

# Inicializando o pygame
pygame.init()

# Configurações iniciais
IMAGE_SIZE = 500
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600  # Mais espaço para interface
MARGIN = 5  # Margem entre as peças

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Cor de comemoração
RED = (255, 0, 0)  # Cor para texto de erro
BUTTON_COLOR = (50, 150, 50)  # Cor dos botões
HOVER_COLOR = (75, 200, 75)   # Cor dos botões ao passar o mouse
BG_COLOR = (30, 30, 30)  # Cor de fundo

# Carregar a imagem do quebra-cabeça
image = pygame.image.load('src/imagem.jpg')  # Substitua pelo caminho correto da imagem
image = pygame.transform.scale(image, (IMAGE_SIZE, IMAGE_SIZE))

# Inicializar a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jogo de Quebra-Cabeça')

# Função para criar um som de onda senoide
def create_sound(frequency, duration, volume=1.0):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    waveform_integers = np.int16(waveform * volume * 32767)
    stereo_waveform = np.column_stack((waveform_integers, waveform_integers))  # Tornar 2D para estéreo
    return pygame.sndarray.make_sound(stereo_waveform)

# Criar sons para movimento e vitória
move_sound = create_sound(440, 0.1)  # Tom de 440 Hz por 0.1 segundo
win_sound = create_sound(880, 0.3)   # Tom de 880 Hz por 0.3 segundo

# Função para desenhar botões com bordas arredondadas
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Função para dividir a imagem em peças e associar um índice correto a cada peça
def divide_image(grid_size):
    pieces = []
    tile_size = IMAGE_SIZE // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            piece = image.subsurface(j * tile_size, i * tile_size, tile_size, tile_size)
            pieces.append((piece, i * grid_size + j))  # Adiciona a peça e seu índice correto
    return pieces

# Embaralhar peças
def shuffle_pieces(pieces):
    blank_piece = pieces.pop()  # Remover a última peça para o espaço em branco
    random.shuffle(pieces)
    pieces.append((None, blank_piece[1]))  # Adiciona uma referência None para o espaço em branco com seu índice
    return pieces

# Verificar se o quebra-cabeça está resolvido
def is_solved(pieces):
    for index, (_, correct_index) in enumerate(pieces):
        if index != correct_index:
            return False
    return True

# Tela de seleção de dificuldade
def select_difficulty():
    font = pygame.font.Font(None, 60)
    easy_text = font.render('Fácil', True, WHITE)
    normal_text = font.render('Normal', True, WHITE)
    hard_text = font.render('Difícil', True, WHITE)
    
    easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    normal_rect = normal_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, 400))

    while True:
        screen.fill(BG_COLOR)
        
        # Desenhar botões com bordas arredondadas e efeito hover
        mouse_pos = pygame.mouse.get_pos()
        
        if easy_rect.collidepoint(mouse_pos):
            draw_rounded_rect(screen, HOVER_COLOR, easy_rect.inflate(40, 20), 10)
        else:
            draw_rounded_rect(screen, BUTTON_COLOR, easy_rect.inflate(40, 20), 10)
        screen.blit(easy_text, easy_rect)
        
        if normal_rect.collidepoint(mouse_pos):
            draw_rounded_rect(screen, HOVER_COLOR, normal_rect.inflate(40, 20), 10)
        else:
            draw_rounded_rect(screen, BUTTON_COLOR, normal_rect.inflate(40, 20), 10)
        screen.blit(normal_text, normal_rect)
        
        if hard_rect.collidepoint(mouse_pos):
            draw_rounded_rect(screen, HOVER_COLOR, hard_rect.inflate(40, 20), 10)
        else:
            draw_rounded_rect(screen, BUTTON_COLOR, hard_rect.inflate(40, 20), 10)
        screen.blit(hard_text, hard_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return 3  # GRID_SIZE para fácil
                elif normal_rect.collidepoint(event.pos):
                    return 4  # GRID_SIZE para normal
                elif hard_rect.collidepoint(event.pos):
                    return 5  # GRID_SIZE para difícil

# Função principal do jogo
def main():
    while True:
        grid_size = select_difficulty()  # Seleção de dificuldade
        play_game(grid_size)

# Função para jogar o jogo de quebra-cabeça
def play_game(grid_size):
    pieces = divide_image(grid_size)
    pieces = shuffle_pieces(pieces)
    blank_pos = len(pieces) - 1  # Posição inicial da peça em branco

    tile_size = IMAGE_SIZE // grid_size
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    text = font.render('Você Ganhou!', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))

    start_time = time.time()  # Tempo inicial
    running = True
    game_won = False
    elapsed_time = 0
    final_time_text = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_won and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if replay_rect.collidepoint(mouse_pos):
                    play_game(grid_size)  # Jogar novamente
                elif menu_rect.collidepoint(mouse_pos):
                    return  # Voltar ao menu inicial

            if not game_won and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // tile_size
                row = y // tile_size
                clicked_pos = row * grid_size + col

                # Verificar se o clique está ao lado da peça em branco
                if (
                    abs(blank_pos - clicked_pos) == 1 and
                    (blank_pos // grid_size == clicked_pos // grid_size)
                ) or (
                    abs(blank_pos - clicked_pos) == grid_size
                ):
                    # Trocar a peça clicada com a peça em branco
                    pieces[blank_pos], pieces[clicked_pos] = pieces[clicked_pos], pieces[blank_pos]
                    blank_pos = clicked_pos
                    move_sound.play()  # Tocar som de movimento

                # Verificar se o quebra-cabeça está resolvido
                if is_solved(pieces):
                    game_won = True
                    elapsed_time = time.time() - start_time  # Tempo final
                    win_sound.play()  # Tocar som de vitória
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    final_time_text = small_font.render(f'Tempo Total: {minutes:02}:{seconds:02}', True, WHITE)

        # Atualizar o tempo decorrido
        if not game_won:
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_text = small_font.render(f'Tempo: {minutes:02}:{seconds:02}', True, WHITE)

        # Desenhar as peças na tela
        screen.fill(BG_COLOR)
        if game_won:
            screen.fill(GREEN)  # Preencher a tela inteira com verde ao ganhar
            screen.blit(text, text_rect)  # Exibir texto de vitória
            if final_time_text:
                final_time_rect = final_time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(final_time_text, final_time_rect)  # Exibir tempo final

            # Botões para jogar novamente e voltar ao menu
            replay_text = small_font.render('Jogar Novamente', True, WHITE)
            menu_text = small_font.render('Voltar ao Menu', True, WHITE)
            replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

            if replay_rect.collidepoint(pygame.mouse.get_pos()):
                draw_rounded_rect(screen, HOVER_COLOR, replay_rect.inflate(20, 10), 10)
            else:
                draw_rounded_rect(screen, BUTTON_COLOR, replay_rect.inflate(20, 10), 10)
            screen.blit(replay_text, replay_rect)

            if menu_rect.collidepoint(pygame.mouse.get_pos()):
                draw_rounded_rect(screen, HOVER_COLOR, menu_rect.inflate(20, 10), 10)
            else:
                draw_rounded_rect(screen, BUTTON_COLOR, menu_rect.inflate(20, 10), 10)
            screen.blit(menu_text, menu_rect)

        else:
            for i in range(grid_size):
                for j in range(grid_size):
                    piece, _ = pieces[i * grid_size + j]
                    if piece is not None:  # Desenha apenas se não for o espaço em branco
                        screen.blit(piece, (j * tile_size, i * tile_size))

            # Exibir o temporizador na parte inferior da tela
            screen.blit(time_text, (10, IMAGE_SIZE + 10))

        pygame.display.flip()

if __name__ == '__main__':
    main()
