from random import randint


class BoardException(Exception):
    pass


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Dot) and self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, len_: int, dot_nose, direction: int, health=3):
        self.len_ = len_
        self.dot_nose = dot_nose
        self.direction = direction
        self.health = health

    def dots(self):
        ship_dots = [(self.dot_nose.x, self.dot_nose.y)]
        count = 0
        if self.direction == 0:
            for i in range(self.len_ - 1):
                count += 1
                ship_dots.append((self.dot_nose.x + count, self.dot_nose.y))
        elif self.direction == 1:
            for i in range(self.len_ - 1):
                count += 1
                ship_dots.append((self.dot_nose.x, self.dot_nose.y + count))
        return ship_dots


class Board:
    def __init__(self, hid=True):
        self.map_ = [["O"] * 6 for _ in range(6)]
        self.map_hid = [["."] * 6 for _ in range(6)]
        self.list_ships = []
        self.hid = hid
        self.quantity_lives_ships = 11
        self.busy = []
        self.shots = []

    def funk_insert(self, x, y, past: str):
        try:
            if self.map_[x][y] != "■":
                self.map_[x].pop(y)
                self.map_[x].insert(y, past)
            else:
                pass
        except IndexError as e:
            pass

    def funk_contur(self, dot, a):
        self.funk_insert(abs(dot[a][0] - 1), abs(dot[a][1] - 1), ".")
        self.funk_insert(abs(dot[a][0] - 1), dot[a][1] + 1, ".")
        self.funk_insert(abs(dot[a][0] - 1), dot[a][1], ".")
        self.funk_insert(dot[a][0] + 1, abs(dot[a][1] - 1), ".")
        self.funk_insert(dot[a][0], abs(dot[a][1] - 1), ".")
        self.funk_insert(dot[a][0], dot[a][1] + 1, ".")
        self.funk_insert(dot[a][0] + 1, dot[a][1] + 1, ".")
        self.funk_insert(dot[a][0] + 1, dot[a][1], ".")

    def add_ship(self, ship):
        for i in ship:
            self.funk_insert(i[0], i[1], "■")
        self.list_ships.append(ship)

    def contour(self, dot):
        self.funk_contur(dot, 0)
        self.funk_contur(dot, -1)

    def enter_hid(self):
        count = 1
        if self.hid == True:
            print("Доска игрока:")
            print("  [|1|, |2|, |3|, |4|, |5|, |6|]")
            for i in self.map_:
                print(count, i)
                count += 1
        else:
            print("Доска компьютера:")
            print("  [|1|, |2|, |3|, |4|, |5|, |6|]")
            for i in self.map_hid:
                print(count, i)
                count += 1

    def out(self, dot):
        if dot.x in range(6) and dot.y in range(6):
            return True
        return False

    def func_shot(self, dot, map_):
        if ((dot.x, dot.y) in self.shots) or (dot.x > 5 or dot.y > 5):
            raise BoardUsedException("Вы уже стреляли")
        if '■' in self.map_[dot.x][dot.y]:
            map_[dot.x].pop(dot.y)
            map_[dot.x].insert(dot.y, "X")
            self.busy.append((dot.x, dot.y))
            self.shots.append((dot.x, dot.y))
        else:
            map_[dot.x].pop(dot.y)
            map_[dot.x].insert(dot.y, "T")
            self.shots.append((dot.x, dot.y))

    def shot(self, dot):
        if self.hid:
            self.func_shot(dot, self.map_)
        else:
            self.func_shot(dot, self.map_hid)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
        self.wound = False
        self.dead = False
        self.quantity_dead = 0

    def check_ships(self, dot):
        for i in self.enemy.list_ships:
            if (dot.x, dot.y) in i:
                i.remove((dot.x, dot.y))
                if len(i) != 0:
                    self.wound = True
                    return self.wound
                else:
                    self.dead = True
                    self.quantity_dead += 1
                    return self.dead

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                self.check_ships(target)
                if self.quantity_dead == 7:
                    break
                elif self.wound:
                    print("Есть пробитие! У вас еще один ход!")
                    print(self.enemy.enter_hid())
                    self.wound = False
                    continue
                elif self.dead:
                    print("Противник убит! У вас еще один ход.")
                    print(self.enemy.enter_hid())
                    self.dead = False
                    continue
                return repeat
            except BoardUsedException:
                print("Вы уже стреляли в эту клетку, либо пытаетесь выстрелить за пределы игрового поля.")
                print("______________________Пожалуйста, введите значение заново________________________")


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f" Ход компьютера: {d.x + 1}, {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        self.begin = 0
        self.count_len = 0
        self.count_contur = 0
        board_user = self.random_board(hid=True)
        board_ai = self.random_board(hid=False)
        self.user = User(board_user, board_ai)
        self.ai = AI(board_ai, board_user)

    def rand_b_func(self, rng, max_v, len_, r_b, rand_board):
        for i in range(rng):
            if self.begin == 1:
                break
            while True:
                self.count_contur = 0
                count_ = 0
                count_contur = 0
                direction = randint(0, 1)
                if direction == 0:
                    dot_1 = Dot(randint(0, max_v), randint(0, 5))
                else:
                    dot_1 = Dot(randint(0, 5), randint(0, max_v))
                if r_b[dot_1.x][dot_1.y] == "■" or r_b[dot_1.x][dot_1.y] == ".":
                    continue
                ship_ = Ship(len_, dot_1, direction)
                if r_b[ship_.dots()[-1][0]][ship_.dots()[-1][1]] == "■" or \
                        r_b[ship_.dots()[-1][0]][ship_.dots()[-1][1]] == ".":
                    continue
                # Код идущий ниже предназначен для того, чтобы не дать циклу уйти в бесконечность, в случае если
                # пустые места на игровом поле закончатся, когда еще не все корабли будт расставлены. Изначально
                # была задумка поймать момент, когда в списке r_b не останется значений "0", но по какой-то
                # причине интерпритатор не видел в этом списке "0". Даже в первых итерациях. Поэтому был выбран
                # вариант со значением ".". Если тот, кто будет читать этот код сможет пролить свет на эту
                # анамалию, прошу дать мне знать, я много времени потратил безуспешно, пытаясь разобраться с этим.

                rand_board.contour(ship_.dots())
                rand_board.add_ship(ship_.dots())

                for x in r_b:
                    count_ += x.count("■")
                for j in r_b:
                    count_contur += j.count(".")
                if count_contur > 25:
                    self.begin = 1
                    return None
                break

    def random_board(self, hid):
        rand_board = Board(hid)
        while True:
            self.rand_b_func(1, 3, 3, rand_board.map_, rand_board)
            self.rand_b_func(2, 4, 2, rand_board.map_, rand_board)
            self.rand_b_func(4, 5, 1, rand_board.map_, rand_board)

            for i in rand_board.map_:
                self.count_len += i.count("■")
            if self.count_len != 11 or self.begin == 1:
                self.count_len = 0
                self.begin = 0
                rand_board.map_ = [["O"] * 6 for _ in range(6)]
                continue
            else:
                self.count_len = 0
                rand_board.enter_hid()
                return rand_board

    def greet(self):
        print('Приветствую Вас в игре "морской бой"!')
        print("Разумеется с правилами игры вы уже знакомы=)")
        print("Для того чтобы сделать ход,")
        print("Вам нужно ввести в консоль координаты точки,")
        print("две цифры от 1 до 6 через пробел, например 1 3")

    def loop(self):
        self.greet()
        while True:
            print("-" * 35)
            print(self.ai.board.enter_hid())
            self.user.move()
            print(self.ai.board.enter_hid())
            if self.user.quantity_dead == 7:
                print("__________УРА___________")
                print("______Вы выиграли______!")
                print("______Поздравляю!_______")
                break
            self.ai.move()
            print(self.user.board.enter_hid())
            if self.ai.quantity_dead == 7:
                print("_________О нет!__________")
                print("______Вы проиграли______!")
                print("_______Мне жаль:(________")
                break
            print("-" * 35)


g = Game()
g.loop()