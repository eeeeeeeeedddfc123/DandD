from random import randint, choice

weapons = ['sword', 'mace', 'club', 'claymore', 'bow', 'crossbow', 'minigun', 'gun', 'staff', 'wand', 'scepter',
           'magic_rocket']
types_of_armors = ['Light', 'Medium', 'Heavy']
weapon_data = {'Warrior': {'sword': {'dmg': randint(1, 8),
                                     'dist': 1},
                           'mace': {'dmg': randint(1, 6),
                                    'dist': 2},
                           'club': {'dmg': randint(1, 8),
                                    'dist': 1},
                           'claymore': {'dmg': 2 * randint(1, 6),
                                        'dist': 2}},
               'Shooter': {'bow': {'dmg': randint(1, 6),
                                   'dist': 20},
                           'crossbow': {'dmg': randint(1, 10),
                                        'dist': 25},
                           'minigun': {'dmg': randint(1, 4) * randint(1, 4),
                                       'dist': 15},
                           'gun': {'dmg': randint(1, 8),
                                   'dist': 22}},
               'Wizard': {'staff': {'dmg': randint(1, 8),
                                    'dist': 25},
                          'wand': {'dmg': randint(1, 4) + 1,
                                   'dist': 40},
                          'scepter': {'dmg': randint(1, 8),
                                      'dist': 15},
                          'magic_rocket': {'dmg': randint(1, 8) * randint(1, 2),
                                           'dist': 20}}}

armor_data = {'Light': {'leather': 11,
                        'riveted leather': 12},
              'Medium': {'rawhide': 12,
                         'scaly': 14,
                         'breastplate': 14},
              'Heavy': {'annelid': 14,
                        'chainmail': 16,
                        'lamellar': 17}}


class Human:
    def __init__(self, hp, mana, speed, dmg, armor_type, armor, mod, inv, money):
        self.max_hp = hp
        self.hp = hp
        self.mana = mana
        self.speed = speed
        self.dmg = dmg
        self.armor = armor_data[armor_type][armor]
        self.mod = mod
        self.money = money
        self.weapon = None
        self.act_time = 0
        self.distance = 0
        self.inventory = inv
        self.charge = 0
        self.level = 1
        self.xp = 0

    def __str__(self):
        return f'Человек. \n' \
               f'Здоровье: {self.hp}. \n' \
               f'Скорость: {self.speed} км/ч. \n' \
               f'Урон: {self.dmg}. \n' \
               f'Класс брони: {self.armor}. \n' \
               f'Модификатор испытаний: {self.mod}. \n' \
               f'Баланс: {self.money} серебряных монет. \n' \
               f'Оружие: {self.weapon}. \n' \
               f'Расстояние: {self.distance} \n' \
               f'Инвентарь: {self.inventory}.'

    def wear_armor(self, armor_type, armor):
        if self.armor == None and armor_data[armor_type][armor] in self.inventory:
            self.armor = armor_data[armor_type][armor]
            print(f'Вы экипировали {armor} типа {armor_type}')
        else:
            print(f'Вы не можете экипировать {armor}, так как на вас надета другая броня')

    def remove_armor(self):
        if self.armor == None:
            print('Вам нечего снимать')
        else:
            self.inventory.append(self.armor)
            self.armor = None
            print('Вы сняли броню')

    def remove_weapon(self):
        if self.weapon == None:
            print('Вам нечего убирать')
        else:
            self.dmg -= self.weapon['dmg']
            self.weapon = None
            print('Вы убрали оружие')

    def walk(self, time):
        if self.act_time + time <= 16:
            a = randint(0, 2)
            self.distance += self.speed * time
            self.act_time += time
            print(f'Вы прошли {self.speed * time} километров')
            if a == 1:
                print('Вы нашли сундук. \n'
                      'Открыть его?')
                if input() == 'Да':
                    pass
            elif a == 2:
                print('Вы увидели врага. \n'
                      'Атаковать его?')
                if input() == 'Да':
                    rival = Human(randint(10, 20), 15, randint(15, 30), weapon_data[choice(weapons)]['dmg'], 'Light',
                                  'riveted leather', 3, [], randint(10, 5000))
                    while self.hp > 0 and rival.hp > 0:
                        self.udar(rival)
                        rival.udar(self)
                    if self.hp <= 0:
                        print('Вас победили')
                    else:
                        print('Вы победили')
                        self.money += rival.money
        else:
            print('Сначала нужно отдохнуть')

    def rest(self, rest_time):
        if 1 <= rest_time < 8:
            self.hp += randint(1, 8)
            self.act_time -= 6
            print('Вы провели короткий отдых')
        elif rest_time >= 8:
            if 'dry ration' in self.inventory:
                self.hp = self.max_hp
                self.act_time = 0
                print('Вы провели долгий отдых')
                self.inventory.remove('dry ration')
            else:
                self.act_time -= 10
                if self.hp < self.max_hp:
                    self.hp = self.max_hp


    def heal_potion(self):
        if 'heal potion' in self.inventory:
            a = (randint(1, 4) * 2) + 2
            if self.hp + a >= self.max_hp:
                self.hp = self.max_hp
            else:
                self.hp += a
            self.inventory.remove('heal potion')

    def udar(self, other):
        if abs(self.distance - other.distance) <= self.weapon['dist']:
            if armor_data[other.armor] <= randint(1, 20) + self.mod:
                if self.charge != 1:
                    other.hp -= round(self.weapon['dmg'] * (self.charge + 1))
                    if other.hp <= 0:
                        self.xp += 50
                else:
                    other.hp -= self.weapon['dmg']

    def take_cover(self, st_ukr):
        self.charge = st_ukr


class Warrior(Human):
    def __init__(self, hp, mana, speed, dmg, armor_type, armor, mod, inv, money):
        super().__init__(hp, mana, speed, dmg, armor_type, armor, mod, inv, money)

    def wear_weapon(self, weapon):
        if weapon in weapon_data['Warrior'] and self.weapon == None:
            if weapon == 'sword':
                self.dmg += weapon_data['Warrior']['sword']['dmg']
            elif weapon == 'mace':
                self.dmg += weapon_data['Warrior']['mace']['dmg']
            elif weapon == 'club':
                self.dmg += weapon_data['Warrior']['club']['dmg']
            elif weapon == 'claymore':
                self.dmg += weapon_data['Warrior']['claymore']['dmg']
            print(f'Вы экипировали {weapon}')
        else:
            print(f'Вы не можете экипировать {weapon}')


pers1 = Warrior(13, 15, 20, 10, 'Light', 'leather', 3, [], 100)

# print('Здравствуйте. Вот список доступных команд: \n'
#       'wear_armor({Тип брони}, {Броня}), \n'
#       'remove_armor(), \n'
#       'wear_weapon({Оружие}), \n'
#       'remove_weapon(), \n'
#       'walk')
