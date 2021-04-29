import json

ANIMAL = {
    'lion': {'diet': 'predator', 'min_area': 12}, 'panthera': {'diet': 'predator', 'min_area': 12},
    'lynx': {'diet': 'predator', 'min_area': 10}, 'crocodile': {'diet': 'predator', 'min_area': 8},
    'cheetah': {'diet': 'predator', 'min_area': 10}, 'bear': {'diet': 'predator', 'min_area': 7},
    'monkey': {'diet': 'herbivorous', 'min_area': 2}, 'deer': {'diet': 'herbivorous', 'min_area': 9},
    'rabbit': {'diet': 'herbivorous', 'min_area': 1}, 'horse': {'diet': 'herbivorous', 'min_area': 12},
    'roe': {'diet': 'herbivorous', 'min_area': 5}, 'raccoon': {'diet': 'herbivorous', 'min_area': 1},
}


class Animal:
    """
    class Animal for initialize animal objects and add to list
    """
    animals = []

    def __init__(self, name, diet, min_area):
        self.name = name
        self.diet = diet
        self.min_area = min_area
        Animal.animals.append(self)


class Aviary:
    """
    class Aviary
    one aviary == one copy class Aviary
    method get_aviary_area calculated minimal area for animal in aviary

    """

    def __init__(self):
        self.animals = []

    def get_aviary_area(self):
        area = sum(i.min_area for i in self.animals)
        return area

    def __repr__(self):
        return f'{self.animals}'


class Zoo:
    animals = {}
    MAX_AREA = 3400

    def __new__(cls):
        """
        Making class Zoo a singleton
        so that we have a single copy
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Zoo, cls).__new__(cls)
        return cls.instance

    def add_animal(self, animal):
        """
        Add animal to aviary with the same type
        Like, lion to lion, monkey to monkey

        """
        if animal.name not in self.animals.keys():
            new_aviary = Aviary()
            self.animals[animal.name] = new_aviary
            new_aviary.animals.append(animal)
        else:
            self.animals[animal.name].animals.append(animal)

    def add_animal_from_json(self, file):
        """
        Import data from json
        In begin we initialize animal in class Animal
        after we add to aviary
        """
        with open(file) as f:
            animals = json.load(f)
            for i in animals:
                for j in i['animals']:
                    get_animals([j] * i['animals'][j])
                    if i['aviary_name'] not in self.animals.keys():
                        new_aviary = Aviary()
                        self.animals[i['aviary_name']] = new_aviary

                    self.animals[i['aviary_name']].animals.extend(Animal.animals[-i['animals'][j]:])

    def add_animal_to_other_animal(self, animal, aviary):
        """
        Add animal to aviary with animal another type
        And we get message if they have different diet
        """
        av_animal = self.animals[aviary].animals

        if av_animal[0].diet != animal.diet:
            food, not_food = animal.name if animal.diet == 'herbivorous' else aviary, \
                             aviary if av_animal[0].diet == 'predator' else animal.name
            choose = input(f'Do you really want to feed the {food} to the {not_food}:: y/n\n')

            if choose == 'n':
                return print('Nice job!\n')

            if choose == 'y':
                return print(f'The {not_food} ate the {food}\n')
            else:
                print('Please choose only "y" or "n\n')
                self.add_animal_to_other_animal(animal, aviary)

        av_animal.append(animal)

    @staticmethod
    def delete_animal(animal):
        """
        Delete selected animal from our zoo
        """
        try:
            get_animal = Zoo.animals[animal]
        except KeyError:
            return print(f'Sorry, we don\'t have the {animal.capitalize()}\n')

        if len(get_animal.animals) <= 1:
            del get_animal
        else:
            Zoo.animals[animal].animals.pop()

    def check_area(self):
        """
        Check about area
        Do we have area?
        We get message if area was ended
        Or if the area remains less than 100, we get a message
        """
        area = sum(self.animals[i].get_aviary_area() for i in self.animals)

        if area >= self.MAX_AREA:
            try:
                raise AreaError(f'\n\n{"???" * 10}\nThe area is over\n\n{"???" * 10}\n')
            except AreaError as e:
                return print(str(e))
        if (self.MAX_AREA - area) < 100:
            print('***' * 10, '\n')
            print('Area almost ended, do something\n')
            print('***' * 10, '\n')

    def view_all_aviary(self):
        """
        Print all aviary
        """
        for j, i in enumerate(self.animals.keys()):
            print(f'{j + 1}. {i}')  # Get number of aviary and whose aviary is this

        return [i for i in self.animals]

    def what_animal_in_aviary(self, animal):
        """
        Check what animal in selected aviary
        """
        w_animal_inside = [i.name for i in self.animals[animal].animals]
        animal_inside = ''

        for i in set(w_animal_inside):
            animal_inside += f'{i.capitalize()}: {w_animal_inside.count(i)} '

        return animal_inside.rstrip()

    @staticmethod
    def get_total_animals():
        return sum(len(Zoo.animals[i].animals) for i in Zoo.animals)

    def __str__(self):
        """
        Info about zoo
        Total animal, aviary, minimal area for animal, how much and which animal an aviary
        """
        animals = self.animals
        area = 0
        n = 0
        total_animals = self.get_total_animals()

        info = '\n\n' + '===' * 20 + '\n'
        info += f'Total of animals: {total_animals}\n'
        info += f'Total of aviary: {len(animals)}\n'

        for i in animals.keys():
            n += 1
            info += f'---{n}. {self.what_animal_in_aviary(i)}.' \
                    f' Total animals in aviary: {len(animals[i].animals)}. ' \
                    f'Minimal area: {animals[i].get_aviary_area()}\n'
            area += animals[i].get_aviary_area()

        info += f'Total minimal area: {area}, free spaces: {self.MAX_AREA - area}'
        info += '\n' + '===' * 20 + '\n\n'
        return info


class AreaError(Exception):  # Custom error about area, we get message if area ended
    def __init__(self, msg):
        self.msgs = msg


def get_animals(arr):
    return [Animal(i, **ANIMAL[i]) for i in arr]  # Get animals and initialize in class Animal


def check_animal(arr):
    """
    Check can we get animal
    if animal in ANIMAL dict, we can add to our zoo
    else - can't
    """
    valid_data = []
    invalid_data = []
    help_ = ', '.join([i for i in ANIMAL.keys()])

    for i in arr:
        if ANIMAL.get(i) is not None:
            valid_data.append(i)
        else:
            invalid_data.append(i)
    if invalid_data:
        print(f'Sorry, incorrect animal(s), {", ".join(invalid_data)}\n We can get only that animals {help_}\n')

    if not valid_data:
        return False
    else:
        get_animals(valid_data)


def zoo_to_json(animals):
    """
    Export our zoo to json file
    walk through the aviaries and write to a file
    """
    n = 0
    d_json = []

    for i in animals.keys():
        n += 1
        animal_dict = {
            'id': n,
            'aviary_name': i,
            'animals': {}
        }
        inside_animals = [x.name for x in animals[i].animals]
        for j in set(inside_animals):
            animal_dict['animals'].setdefault(j, inside_animals.count(i))

        d_json.append(animal_dict)
    with open('animals.json', 'w') as f:
        return json.dump(d_json, f, indent=4)


def delete_animal(animal):
    return Zoo.delete_animal(animal)  # Delete selected animal


def user_input():
    """
    Options for user input
    Automatically sort by type
    Manually distribution to the selected aviary
    Delete selected animal
    Info about zoo
    Import and Export data
    """
    try:
        user_inp = input('Hello, please choose option:\n'
                         '1: Add animal(s), automatically sort by type\n'
                         '2: Delete animal\n'
                         '3: Info about zoo\n'
                         '4. Choose an aviary for settling, manual distribution to the selected aviary\n'
                         '5. Export data to json\n'
                         '6. Import data from json\n')

        if user_inp == '1':
            return get_animals(input('Write animals whit separate ", ": ').lower().split(', '))
        if user_inp == '2':
            name = input('Please enter the name animal, for example "lion":').lower()
            return delete_animal(name)
        if user_inp == '3':
            return print(Zoo())

        if user_inp == '4':
            choose_aviary = Zoo().view_all_aviary()
            get_id = int(input('Please choose id_aviary:'))
            check = check_animal(input('Which animal do you want for settling:').split(', '))

            if check is not False:
                Zoo().add_animal_to_other_animal(Animal.animals[-1], choose_aviary[get_id - 1])
                Animal.animals.pop()
        if user_inp == '5':
            return zoo_to_json(Zoo.animals)
        if user_inp == '6':
            file = input('Path to file, for example animals.json:')
            Zoo().add_animal_from_json(file)
        else:
            print('Wrong option, try again\n')
            user_input()
    except KeyboardInterrupt:
        print('Finished')
        exit()


def main():
    while True:
        user_input()
        animal_obj = Animal.animals
        n = Zoo.get_total_animals()

        for i in animal_obj[n:]:
            Zoo().add_animal(i)

        Zoo().check_area()


if __name__ == '__main__':
    main()
