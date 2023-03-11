print(' Приветствую Вас в игре "Крестики - Нолики"! \n Не буду утомлять Вас правилами, уверен, вы и так их знаете,'
      ' просто следуйте инструкциям ниже.\n Желаю Вам приятной игры ;-)')
box = list('  0 1 2\n0 - - -\n1 - - -\n2 - - -')
step = ""
step_in_box = 0
cells = [10, 12, 14, 18, 20, 22, 26, 28, 30]
repit_and_incorect_entry = []
positions_X = []
positions_0 = []
win_X = []
win_0 = []
def player1_walk():
    if step_in_box in cells:
        box.pop(step_in_box), box.insert(step_in_box, 'X')
        cells.remove(step_in_box), positions_X.append(step_in_box)
    else:
        print('Ячейка занята оппонентом или ее не существует, введите друое значение!')
        repit_and_incorect_entry.append(1)

def player2_walk():
    if step_in_box in cells:
        box.pop(step_in_box), box.insert(step_in_box, '0')
        cells.remove(step_in_box), positions_0.append(step_in_box)
    else:
        print('Ячейка занята оппонентом или ее не существует, введите друое значение!')
        repit_and_incorect_entry.append(1)

def steps():
    global step_in_box
    if step == '00':
        step_in_box = 10
    elif step == '01':
        step_in_box = 12
    elif step == '02':
        step_in_box = 14
    elif step == '10':
        step_in_box = 18
    elif step == '11':
        step_in_box = 20
    elif step == '12':
        step_in_box = 22
    elif step == '20':
        step_in_box = 26
    elif step == '21':
        step_in_box = 28
    elif step == '22':
        step_in_box = 30

def check_win(a,b):
    win_position = [[10, 12, 14], [18, 20, 22], [26, 28, 30], [10, 18, 26],
                    [12, 20, 28], [14, 22, 30], [10, 20, 30], [14, 20, 26]]
    for position in win_position:
        if position[0] in a and position[1] in a and position[2] in a:
            b.append(1)
            break


while True:
    step = input('Ходит X. Введите числовое обозначение клетки (00, 01, 02, 10 ... 22)')
    steps()
    player1_walk()
    if 1 in repit_and_incorect_entry:
        repit_and_incorect_entry.pop()
        step = input('Ходит X. Введите числовое обозначение клетки (00, 01, 02, 10 ... 22)')
        steps()
        player1_walk()
    print(''.join(box))
    print(positions_X)
    check_win(positions_X, win_X)
    print(win_X)
    if 1 in win_X:
        print('Игрок X победил, поздравляю!')
        break
    step = input('Ходит 0. Введите числовое обозначение клетки (00, 01, 02, 10 ... 22)')
    steps()
    player2_walk()
    if 1 in repit_and_incorect_entry:
        repit_and_incorect_entry.pop()
        step = input('Ходит 0. Введите числовое обозначение клетки (00, 01, 02, 10 ... 22)')
        steps()
        player2_walk()
    print(''.join(box))
    print(positions_0)
    check_win(positions_0, win_0)
    print(win_0)
    if 1 in win_0:
        print('Игрок 0 победил, поздравляю!')
        break