import keyboard
from time import sleep
import os
from logging import CRITICAL, getLogger, INFO, basicConfig, StreamHandler, FileHandler, ERROR, DEBUG
import random

logger = getLogger()
console = StreamHandler()
console.setLevel(CRITICAL)
file_handler = FileHandler('logs.log', mode='w')
file_handler.setLevel(DEBUG)
FORMAT = '%(asctime)s :: %(levelname)-8s :: %(message)s :: %(name)s'
basicConfig(level=DEBUG, handlers=[file_handler, console], format=FORMAT)


game_map = []
game_map_size_x = 10
game_map_size_y = 10
matrix_part = []
pos_x = [2]
pos_y = [2]
speed = 0.3
direction = 'Right'
apples_x = [6, 1, 4, 9]
apples_y = [6, 1, 4, 9]

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def detect_buttons(e):
    global direction
    if keyboard.is_pressed('up') and direction != 'Down':
        direction = 'Up'
    elif keyboard.is_pressed('down') and direction != 'Up':
        direction = 'Down'
    elif keyboard.is_pressed('left') and direction != 'Right':
        direction = 'Left'
    elif keyboard.is_pressed('right') and direction != 'Left':
        direction = 'Right'

def create_map():
    global game_map
    game_map = []
    global matrix_part
    for size_y in range(game_map_size_y):
        for size_x in range(0, game_map_size_x):
            matrix_part.append('''#''')
        game_map.append(matrix_part)
        matrix_part = []
    logger.info('map created')

def update_screen():
    cls()
    logger.info('Clear')
    for n in game_map:
        for m in n:
            print(f'{m} ', end='')
        print('')
    print(' ')
    logger.info('start sleep')
    sleep(speed)
    logger.info('stop sleep')

def random_apple():
    while True:
        apple_x = random.randint(1, game_map_size_x)
        apple_y = random.randint(1, game_map_size_y)
        if game_map[apple_y][apple_x] != '@':
            for k in range(0, len(pos_x)):
                if  f'{apple_y} + " " + {apple_y}' == f'{pos_y[k]} + " " + {pos_x[k]}':
                    continue
            apples_x.append(apple_x)
            apples_y.append(apple_y)
            logger.info(f'new apple at pos {apple_x} {apple_y}')
            break
        else:
            logger.info('apple already exist, creating new')

def change_pos():
    global pos_x
    global pos_y
    match direction:
        case 'Up':
            if pos_y[-1] - 1 < 0 or game_map[pos_y[-1] - 1][pos_x[-1]] == '@':
                exit()
            pos_y.append(pos_y[-1] - 1)
            pos_x.append(pos_x[-1])
        case 'Down':
            if pos_y[-1] + 1 > game_map_size_y or game_map[pos_y[-1] + 1][pos_x[-1]] == '@':
                exit()
            pos_y.append(pos_y[-1] + 1)
            pos_x.append(pos_x[-1])
        case 'Right':
            if pos_x[-1] + 1 > game_map_size_x  or game_map[pos_y[-1]][pos_x[-1] + 1] == '@':
                exit()
            pos_x.append(pos_x[-1] + 1)
            pos_y.append(pos_y[-1])
        case 'Left':
            if pos_x[-1] - 1 < 0  or game_map[pos_y[-1]][pos_x[-1] - 1] == '@':
                exit()
            pos_x.append(pos_x[-1] - 1)
            pos_y.append(pos_y[-1])
    logger.info(f'{pos_x}, {pos_y}')
    create_map()
    try:
        for a in range(0, len(apples_x)):
            game_map[apples_y[a]][apples_x[a]] = '0'
        if game_map[pos_y[-1]][pos_x[-1]] != '0':            
            del pos_x[0]
            del pos_y[0]
        else:
            for a in range(0, len(apples_x)):
                if f'{pos_y[-1]} + " " + {pos_x[-1]}' == f'{apples_y[a]} + " " + {apples_x[a]}':
                    logger.info(f'delete apple at pos {apples_y[a]}, {apples_x[a]}')
                    random_apple()
                    del apples_x[a]
                    del apples_y[a]
    except IndexError:
        logger.error('List Index out of range!')
    for n in range(0, len(pos_x)):
        try:
            game_map[pos_y[n]][pos_x[n]] = '@'
        except IndexError:
            logger.error('Index Error')

    logger.info(f'{pos_x}, {pos_y}')
    logger.info(f'{apples_x}, {apples_y}')

def loop():
    logger.info('Loop Started!')
    while True:
        change_pos()
        update_screen()
        

if __name__ == '__main__':
    logger.info('Started')
    create_map()
    keyboard.hook(detect_buttons)
    loop()
