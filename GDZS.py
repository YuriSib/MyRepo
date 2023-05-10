import time


class TeamStart:
    def __init__(self, *pressure: int, team=[]): # Разобраться, как обойтись без атрибута team
        self.team = team
        if 2 <= len(pressure) <= 6:
            self.pressure = pressure

    def list_pressure(self):
        self.team.extend(self.pressure)
        return self.team

    def p_min(self):
        self.team_min = min(self.team)
        return self.team_min


class TeamMiddle(TeamStart):
    def __init__(self, *pressure: int, quantity=0, time_way=0, team=[]):
        self.team = team
        self.time_way = time_way
        self.quantity = quantity
        if len(pressure) == self.quantity:
            self.pressure = pressure


class SmokeArea:
    def __init__(self, difficult=False, time_enter: int=0, max_drop_p=0, max_drop_p_2=0, time: int=0, t_w = 0,
                 exit_p_2=0, t_w_2=0, a_t=0):
        self.time_enter = time_enter
        self.difficult = difficult
        self.max_drop_p = max_drop_p
        self.max_drop_p_2 = max_drop_p_2
        self.time = time
        self.time_enter = time_enter
        self.t_w = t_w
        self.exit_p_2 = exit_p_2
        self.t_w_2 = t_w_2
        self.a_t = a_t

    def max_drop_pressure(self, p_min): # Максимальное падение давления
        self.max_drop_p = 0
        if self.difficult:
            self.max_drop_p = int((p_min - 10) / 3)
        else:
            self.max_drop_p = int((p_min - 10) / 2.5)
        return f"Максимальное падение давления, при котором звену необходимо выходить " \
               f"из НДС равно - {self.max_drop_p} атм."

    def exit_pressure(self, p_min):  # давление, при котором звену необходимо выходить из НДС,
        exit_p = p_min - self.max_drop_p #если очаг не будет найден
        return f"Если очаг не будет найден, то давление, при котором звену необходимо выходить из НДС - {exit_p} атм."

    def exit_time(self):   # Время с момента включения до подачи команды на выход, очаг не был найден
        self.time = int((self.max_drop_p * 7) / 44) // 1
        return f"Если очаг не будет найден, то команду на выход нужно подавать через {self.time} мин. после включения"

    def enter_time(self): # Время включения в СИЗОД (в реальном времени, с момента ввода давления)
        self.time_enter = time.localtime(time.time())
        return f"Время включения в СИЗОД (Твкл) - {self.time_enter.tm_hour}:{self.time_enter.tm_min}"

    def func_hour_min(self, min): # Метод для прибавления к минутам в формате 12:59
        if min < 60:
            return f"{self.time_enter.tm_hour}:{min}"
        else:
            next_hour = min - 60
            return f"{self.time_enter.tm_hour + 1}:{next_hour}"

    def exit_command_time(self): # Команда на выход
        e_c_t = self.time_enter.tm_min + self.time
        self.func_hour_min(e_c_t)
        return f"Если очаг не будет найден, то в {self.func_hour_min(e_c_t)} необходимо подать команду на выход (Твых)!"

    def time_return(self): # Ожидаемое время возвращения
        t_r = self.time_enter.tm_min + self.t_w
        self.func_hour_min(t_r)
        return f"Ожидаемое время возвращения(Твозвр) - {self.func_hour_min(t_r)}"

    def time_work(self, p_min): # Общее время работы звена
        self.t_w = int((((p_min - 10) * 7) / 44) // 1)
        return f"Общее время работы звена (Pобщ) - {self.t_w} минуты"

    def max_drop_pressure_2(self, p_start, p_middle): #максимальное падение давления, если очаг найден
        zip_object = zip(p_start, p_middle)
        sub_list = []
        for p_start_i, p_middle_i in zip_object:
            sub_list.append(p_start_i - p_middle_i)
        self.max_drop_p_2 = max(list(sub_list))
        return f"Максимальное падение давления в звене составило(Рмах.пад) - {self.max_drop_p_2} атм."

    def exit_pressure_2(self): #Давление, при котором звену необходимо выходить
        self.exit_p_2 = int(self.max_drop_p_2 + (self.max_drop_p_2 / 2) + 10)
        return f"Давление при котором звену необходимо выходить на свежий воздух(Рк.вых) - {self.exit_p_2} атм."

    def time_work_2(self, p_min_2):
        self.t_w_2 = int((((p_min_2 - self.exit_p_2) * 7) / 44) // 1)
        return f"Время работы звена у очага (Точ) - {self.t_w_2} мин."

    def arrival_time(self, time_way):
        self.a_t = self.time_enter.tm_min + time_way
        self.func_hour_min(self.a_t)
        return f"Время прибытия звена к очагу - {self.func_hour_min(self.a_t)}"

    def time_exit(self):
        t_e = self.a_t + self.t_w_2
        self.func_hour_min(t_e)
        return f"Время подачи постовым команды на возвращение - {self.func_hour_min(t_e)}"

while True:
    faermans_quantity = int(input("Введите количество газодымозащитников от 2-х до 6-ти"))
    if faermans_quantity >= 2 and faermans_quantity <= 6:
        break
    else:
        print(f"Значение должно быть в диапазоне от 2-х до 6-ти!")
        continue

def s_p(namber):
    pressure = int(input(f"Введите давление газодымозащитника № {namber} при включении"))
    return pressure
if faermans_quantity == 2:
    t_s = TeamStart(s_p(1), s_p(2))
elif faermans_quantity == 3:
    t_s = TeamStart(s_p(1), s_p(2), s_p(3))
elif faermans_quantity == 4:
    t_s = TeamStart(s_p(1), s_p(2), s_p(3), s_p(4))
elif faermans_quantity == 5:
    t_s = TeamStart(s_p(1), s_p(2), s_p(3), s_p(4), s_p(5))
elif faermans_quantity == 6:
    t_s = TeamStart(s_p(1), s_p(2), s_p(3), s_p(4), s_p(5), s_p(6))

# t_s = TeamStart(275, 280, 280)

t_s.list_pressure()
print(t_s.team)

t_s.p_min()
min_p = t_s.team_min
print(f"Минимальное давление при включении(Рмин) - {min_p} атм.")

s = SmokeArea()
print(s.enter_time())
print("____________")
print(f"Если очаг не будет найден, постовому опираться на слеющие рассчеты:")
print(s.max_drop_pressure(min_p))
print(s.exit_pressure(min_p))
print(s.exit_time())
print(s.exit_command_time())
print(s.time_work(min_p))
print(s.time_return())
print("_____________")


def s_p_2(namber):
    pressure = int(input(f"Введите давление газодымозащитника № {namber}, на момент прибытия звена к очагу"))
    return pressure

time_way = int(input("Введите время, затраченное звеном на путь к очагу(в минутах)"))

if faermans_quantity == 2:
    t_m = TeamMiddle(s_p_2(1), s_p_2(2), quantity=faermans_quantity, time_way=time_way)
elif faermans_quantity == 3:
    t_m = TeamMiddle(s_p_2(1), s_p_2(2), s_p_2(3), quantity=faermans_quantity, time_way=time_way)
elif faermans_quantity == 4:
    t_m = TeamMiddle(s_p_2(1), s_p_2(2), s_p_2(3), s_p_2(4), quantity=faermans_quantity, time_way=time_way)
elif faermans_quantity == 5:
    t_m = TeamMiddle(s_p_2(1), s_p_2(2), s_p_2(3), s_p_2(4), s_p_2(5), quantity=faermans_quantity, time_way=time_way)
elif faermans_quantity == 6:
    t_m = TeamMiddle(s_p_2(1), s_p_2(2), s_p_2(3), s_p_2(4), s_p_2(5), s_p_2(6),
                     quantity=faermans_quantity, time_way=time_way)

# t_m = TeamMiddle(225, 220, quantity=2, time_way=10)
t_m.list_pressure()
print(t_m.team)
t_m.p_min()
min_p_m = t_m.team_min
print(f"Минимальное давление возле очага(Роч) - {min_p_m} атм.")
print(s.max_drop_pressure_2(t_m.team, t_m.team))
print(s.exit_pressure_2())
print(s.time_work_2(min_p_m))
print(s.arrival_time(t_m.time_way))
print(s.time_exit())

