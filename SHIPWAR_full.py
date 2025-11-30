

import random


# ФУНКЦИИ ДЛЯ ПОЛЯ


def fill_pole(pole, size_i, size_j):
    
    for _ in range(size_i):
        pole.append(['[_]'] * size_j)


def show_pole(pole, size_i, size_j):
    
    for i in range(size_i):
        for j in range(size_j):
            print(pole[i][j], ' ', end='')
        print('')
    print()



def calculate_ships(size_i, size_j):
   

    area = size_i * size_j


    default_ships = {4: 1, 3: 2, 2: 3, 1: 4}
    default_total_cells = 20  

    
    if size_i == 10 and size_j == 10:
        return default_ships.copy()


    target_cells = int(area * 0.20)

   
    max_cells = area // 4
    target_cells = min(target_cells, max_cells)

    
    target_cells = max(target_cells, 4)

    scale = target_cells / default_total_cells

    ships_limit = {}
    for size, base in default_ships.items():
        count = int(round(base * scale))

       
        if count < 1 and area >= size:
            count = 1

        ships_limit[size] = count

    
    def total_cells(sl):
        return sum(k * v for k, v in sl.items())

    while total_cells(ships_limit) > target_cells:
        for size in sorted(ships_limit.keys(), reverse=True):
            if ships_limit[size] > 0:
                ships_limit[size] -= 1
                break

    return ships_limit


# ПРОВЕРКА ДОСТУПНОСТИ КЛЕТОК


def is_free_around(pole, i, j):
    
    size_i = len(pole)
    size_j = len(pole[0])

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            ni, nj = i + di, j + dj
            if 0 <= ni < size_i and 0 <= nj < size_j:
                if pole[ni][nj] != '[_]':
                    return False
    return True


#ПРОВЕРКА

def can_place_any_ship(pole, ships_limit):
    
    size_i = len(pole)
    size_j = len(pole[0])

    for ship_size, count in ships_limit.items():
        if count <= 0:
            continue

        # Проверка горизонтального размещения
        for i in range(size_i):
            for j in range(size_j - ship_size + 1):
                if all(is_free_around(pole, i, j + step) for step in range(ship_size)):
                    return True

        # Проверка вертикального размещения
        for i in range(size_i - ship_size + 1):
            for j in range(size_j):
                if all(is_free_around(pole, i + step, j) for step in range(ship_size)):
                    return True

    return False


# СЛУЧАЙНОЕ РАЗМЕЩЕНИЕ КОРАБЛЕЙ


def rand_fill_ships(pole, size_i, size_j, symbol_empty, symbol_ship):
    
    
    ships_limit = calculate_ships(size_i, size_j)

    print("\nТребуемый набор кораблей:", ships_limit)

    for ship_size in sorted(ships_limit.keys(), reverse=True):
        required = ships_limit[ship_size]
        placed = 0
        attempts = 0

        while placed < required and attempts < 1000:
            attempts += 1

            direction = random.choice(["H", "V"])
            i = random.randint(0, size_i - 1)
            j = random.randint(0, size_j - 1)

            if direction == "H":
                if j + ship_size > size_j:
                    continue
                free = all(is_free_around(pole, i, j + step) for step in range(ship_size))

            else:
                if i + ship_size > size_i:
                    continue
                free = all(is_free_around(pole, i + step, j) for step in range(ship_size))

            if not free:
                continue

           
            if direction == "H":
                for step in range(ship_size):
                    pole[i][j + step] = symbol_ship
            else:
                for step in range(ship_size):
                    pole[i + step][j] = symbol_ship

            placed += 1

            if not can_place_any_ship(pole, ships_limit):
                break

        

        ships_limit[ship_size] = placed


# РУЧНАЯ УСТАНОВКА КОРАБЛЕЙ

def hand_fill_ships(pole_user, size_i, size_j, symbol_ship, symbol_empty):
    ships_limit = calculate_ships(size_i, size_j)
    placed_ships = []
    total_ships_left = sum(ships_limit.values())

    while total_ships_left > 0:
        show_pole(pole_user, size_i, size_j)
        print("\nУстановка кораблей:")
        for sz in sorted(ships_limit.keys()):
            print(f"{sz} — осталось {ships_limit[sz]}")
        print("U — отмена последнего, 0 — закончить")

        ship_size_in = input("Размер: ").strip()

        if ship_size_in.upper() == "U":
            if placed_ships:
                last = placed_ships.pop()
                for ci, cj in last['cells']:
                    pole_user[ci][cj] = symbol_empty
                ships_limit[last['size']] += 1
                total_ships_left += 1
            continue

        if ship_size_in == "0":
            break

        if not ship_size_in.isdigit():
            print("Введите число!")
            continue

        ship_size = int(ship_size_in)

        if ship_size not in ships_limit or ships_limit[ship_size] <= 0:
            print("Нет таких кораблей!")
            continue

        i_in = input("i: ").strip()
        j_in = input("j: ").strip()

        if not (i_in.isdigit() and j_in.isdigit()):
            print("Введите числа!")
            continue

        i, j = int(i_in) - 1, int(j_in) - 1

        if not (0 <= i < size_i and 0 <= j < size_j):
            print("Вне поля!")
            continue

        direction = input("H/V: ").strip().upper()
        if direction not in ("H", "V"):
            print("Введите H или V!")
            continue

        if direction == "H" and j + ship_size > size_j:
            print("Не помещается")
            continue

        if direction == "V" and i + ship_size > size_i:
            print("Не помещается")
            continue

        cells = [(i, j + s) if direction == "H" else (i + s, j) for s in range(ship_size)]

        if any(not is_free_around(pole_user, ci, cj) for ci, cj in cells):
            print("Клетки заняты или рядом корабль")
            continue

        for ci, cj in cells:
            pole_user[ci][cj] = symbol_ship

        ships_limit[ship_size] -= 1
        total_ships_left -= 1
        placed_ships.append({'size': ship_size, 'cells': cells})

        print("Корабль установлен!")




def choice(pole_user, size_i, size_j, symbol_ship, symbol_empty):
    while True:
        X = input("Ручная расстановка? (да/нет): ").strip().lower()
        if X == "да":
            hand_fill_ships(pole_user, size_i, size_j, symbol_ship, symbol_empty)
            break
        elif X == "нет":
            rand_fill_ships(pole_user, size_i, size_j, symbol_empty, symbol_ship)
            break



# БОЙ


def user_fight(pole_user, pole_bot, size_i, size_j, symbol_ship, symbol_damage, symbol_empty, symbol_miss, X):
    while True:
        user_i = input("Введите i (А — сохранить, П — выход): ").strip()

        if user_i.upper() == "А":
            save_game(pole_user, pole_bot, X)
            print("Игра сохранена.")
            continue

        if user_i.upper() == "П":
            exit()

        user_j = input("Введите j: ").strip()

        if not (user_i.isdigit() and user_j.isdigit()):
            print("Введите числа!")
            continue

        i, j = int(user_i) - 1, int(user_j) - 1

        if not (0 <= i < size_i and 0 <= j < size_j):
            print("Вне поля!")
            continue

        if pole_bot[i][j] == symbol_ship:
            pole_bot[i][j] = symbol_damage
            print("Попадание!")
            show_pole(pole_bot, size_i, size_j)
            continue

        elif pole_bot[i][j] == symbol_empty:
            pole_bot[i][j] = symbol_miss
            print("Мимо!")
            break

        else:
            print("Сюда уже стреляли.")
            continue


def bot_fight(pole, size_i, size_j, symbol_ship, symbol_damage, symbol_empty, symbol_miss):
    while True:
        i = random.randint(0, size_i - 1)
        j = random.randint(0, size_j - 1)

        if pole[i][j] == symbol_ship:
            pole[i][j] = symbol_damage
            print("Бот попал!")
        elif pole[i][j] == symbol_empty:
            pole[i][j] = symbol_miss
            print("Бот промахнулся\n")
            break

# ПРОВЕРКА НА ПОБЕДУ

 
def win(pole_user, pole_bot, size_i, size_j, symbol_ship):
    user_alive = any(symbol_ship in row for row in pole_user)
    bot_alive = any(symbol_ship in row for row in pole_bot)

    if not user_alive:
        return "BOT"
    if not bot_alive:
        return "USER"
    return None



# СОХРАНЕНИЕ / ЗАГРУЗКА


def save_game(pole_user, pole_bot, X):
    with open("Save.txt", "w") as f:
        f.write(f"{X}\n")
        for row in pole_user:
            f.write(" ".join(row) + "\n")
        for row in pole_bot:
            f.write(" ".join(row) + "\n")


def load_game():
    with open("Save.txt", "r") as f:
        lines = [line.rstrip("\n") for line in f]

    X = int(lines[0])
    size = (len(lines) - 1) // 2

    pole_user = [lines[i].split() for i in range(1, size + 1)]
    pole_bot = [lines[i].split() for i in range(size + 1, len(lines))]

    return X, pole_user, pole_bot, size, size



# ОСНОВНОЙ КОД


size_i = int(input("Высота поля: "))
size_j = int(input("Ширина поля: "))

pole_user = []
pole_bot = []

fill_pole(pole_user, size_i, size_j)
fill_pole(pole_bot, size_i, size_j)

symbol_ship = '[#]'
symbol_damage = '[%]'
symbol_empty = '[_]'
symbol_miss = '[@]'

if input("Загрузить игру? (да/нет): ").strip().lower() == "да":
    X, pole_user, pole_bot, size_i, size_j = load_game()
else:
    choice(pole_user, size_i, size_j, symbol_ship, symbol_empty)
    rand_fill_ships(pole_bot, size_i, size_j, symbol_empty, symbol_ship)
    X = 1

while True:
    print("\nВаше поле:")
    show_pole(pole_user, size_i, size_j)
    print("Поле бота:")
    show_pole(pole_bot, size_i, size_j)

    user_fight(pole_user, pole_bot, size_i, size_j, symbol_ship, symbol_damage, symbol_empty, symbol_miss, X)
    bot_fight(pole_user, size_i, size_j, symbol_ship, symbol_damage, symbol_empty, symbol_miss)

    winner = win(pole_user, pole_bot, size_i, size_j, symbol_ship)

    save_game(pole_user, pole_bot, X)
    X += 1

    if winner == "USER":
        print("Вы победили!")
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"Игрок победил за {X} ходов.\n")
        break

    elif winner == "BOT":
        print("Бот победил!")
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"Бот победил за {X} ходов.\n")
        break
