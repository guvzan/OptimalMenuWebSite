import random as r
import copy as c

class Genetic:
    GENOM_LENGTH = 10
    POPULATION_LENGTH = 200
    CROSSING_CHANCE = 90
    MUTATION_CHANCE = 5
    GENERATIONS_NEEDED = 500
    TARGET_CALORIES = 1500
    TARGET_BZU = [20, 40, 20]
    USE_BZU = False

    def use_bzu(self, use_bzu):
        self.USE_BZU = use_bzu

    def set_settings(self, gl, pl, cch, mch, gn, tc, tbzu):
        self.GENOM_LENGTH = gl
        self.POPULATION_LENGTH = pl
        self.CROSSING_CHANCE = cch
        self.MUTATION_CHANCE = mch
        self.GENERATIONS_NEEDED = gn
        self.TARGET_CALORIES = tc
        self.TARGET_BZU = tbzu

        for i in range(3):
            if self.TARGET_BZU[i] == 0:
                self.TARGET_BZU[i] = 1

    def get_settings(self):
        return [
            self.GENOM_LENGTH,
            self.POPULATION_LENGTH,
            self.CROSSING_CHANCE,
            self.MUTATION_CHANCE,
            self.GENERATIONS_NEEDED,
            self.TARGET_CALORIES,
            self.TARGET_BZU
        ]


    class Product:
        def __init__(self, id, name, calories, bzu):
            self.id = id
            self.name = name
            self.calories = calories
            self.bzu = bzu


    all_products = [
        Product(0, 'water', 0, [0, 0, 0]),
        Product(1, 'rice', 100, [1, 2, 1]),
        Product(2, 'borshch', 450, [2, 4, 2]),
        Product(3, 'smetana', 150, [3, 6, 3]),
        Product(4, 'pelmeni', 500, [4, 8, 4]),
        Product(5, 'burger', 600, [5, 10, 5]),
        Product(6, 'pizza', 550, [6, 12, 6]),
        Product(7, 'maslo', 250, [7, 14, 17]),
        Product(8, 'bread', 100, [8, 16, 8]),
        Product(9, 'ketchup', 50, [9, 18, 9]),
        Product(10, 'mayo', 50, [10, 20, 10])
    ]


    class Menu:
        def __init__(self, all_products, genom_length):
            self.GENOM_LENGTH = genom_length
            self.genome = [r.choice(all_products) for _ in range(self.GENOM_LENGTH)]
            self.calories = 0
            self.bzu_points = (0, 0, 0)
            self.fitness_points = 0

        def show_genome(self):
            print(self.count_calories(), end=' ')
            for i in self.genome:
                print(i.name, end=' ')

        def get_genome(self):
            list_ = []
            for i in self.genome:
                list_.append(i.name)
            return list_

        def count_calories(self):
            self.calories = 0
            for i in self.genome:
                self.calories += i.calories
            return self.calories

        def count_bzu(self):
            self.bzu_points = [0, 0, 0]
            for product in self.genome:
                self.bzu_points[0] += product.bilky
                self.bzu_points[1] += product.zhury
                self.bzu_points[2] += product.vuglevody
                round(self.bzu_points[0], 1)
                round(self.bzu_points[1], 1)
                round(self.bzu_points[2], 1)
            return self.bzu_points


    class Population:
        def __init__(self, all_products, genome_length, population_length, crossing_chance, mutation_chance,
                     target_calories, target_bzu, menu_class, use_bzu):
            self.GENOME_LENGTH = genome_length
            self.POPULATION_LENGTH = population_length
            self.CROSSING_CHANCE = crossing_chance
            self.MUTATION_CHANCE = mutation_chance
            self.TARGET_CALORIES = target_calories
            self.TARGET_BZU = target_bzu
            self.Menu = menu_class
            self.use_bzu = use_bzu
            self.menues = [self.Menu(all_products, self.GENOME_LENGTH) for _ in range(self.POPULATION_LENGTH)]
            self.all_products = all_products

        def show_population(self):
            for i in self.menues:
                i.show_genome()
                print()

        def show_best(self, target):
            most_accurate = self.menues[0]
            for i in self.menues:
                if abs(i.count_calories() - target) < abs(most_accurate.count_calories() - target):
                    most_accurate = i
            return most_accurate

        def tournament(self):
            best = []
            for i in range(self.POPULATION_LENGTH):
                m1 = m2 = m3 = 0
                while m1 == m2 or m2 == m3 or m1 == m3:
                    m1, m2, m3 = r.randint(0, self.POPULATION_LENGTH - 1), r.randint(0, self.POPULATION_LENGTH - 1), r.randint(0,
                                                                                                                     self.POPULATION_LENGTH - 1)
                # maximum = max(self.menues[m1], self.menues[m2], self.menues[m3], key=lambda x: x.count_calories()) # Поки що шукаємо максимум
                if self.use_bzu:
                    maximum = self.tournament_rule_2(self.menues[m1], self.menues[m2], self.menues[m3], self.TARGET_CALORIES, self.TARGET_BZU)
                else:
                    maximum = self.tournament_rule_1(self.menues[m1], self.menues[m2], self.menues[m3], self.TARGET_CALORIES)
                best.append(c.deepcopy(maximum))
            self.menues = best

        def tournament_rule_1(self, m1, m2, m3, target):
            most_accurate = m1
            for i in [m2, m3]:
                if abs(i.count_calories() - target) < abs(most_accurate.count_calories() - target):
                    most_accurate = i
            return most_accurate

        def tournament_rule_2(self, m1, m2, m3, target_calories, target_bzu):
            for menu in [m1, m2, m3]:
                c = menu.count_calories()
                b = menu.count_bzu()
                menu.fitness_points = 0
                menu.fitness_points += abs(100 - c * 100 / target_calories)
                for i in range(3):
                    menu.fitness_points += abs(100 - b[i] * 100 / target_bzu[i])
            return min(m1, m2, m3, key=lambda x: x.fitness_points)



        def crossover(self):
            for i in range(0, len(self.menues), 2):
                if r.randint(0, 100) < self.CROSSING_CHANCE:
                    cut = r.randint(0, len(self.menues[i].genome) - 1)
                    a = self.menues[i].genome
                    b = self.menues[i + 1].genome
                    a[cut:], b[cut:] = b[cut:], a[cut:]
                    self.menues[i].genome = a
                    self.menues[i + 1].genome = b

        def mutation(self):
            for i in range(len(self.menues)):
                if r.randint(0, 100) < self.MUTATION_CHANCE:
                    gen_to_mutate = r.randint(0, len(self.menues[0].genome) - 1)
                    self.menues[i].genome[gen_to_mutate] = r.choice(self.all_products)


    def run_simulation(self, products):
        pop = self.Population(products, self.GENOM_LENGTH, self.POPULATION_LENGTH,
                              self.CROSSING_CHANCE, self.MUTATION_CHANCE,
                              self.TARGET_CALORIES, self.TARGET_BZU,
                              self.Menu, self.USE_BZU)  # Стартова популяція
        pop.show_population()
        list_ = []
        for i in range(self.GENERATIONS_NEEDED):
            print(f'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {i + 1} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            pop.tournament()
            pop.crossover()
            pop.mutation()
            # pop.show_population()
            list_.append(pop.show_best(self.TARGET_CALORIES))
        return list_


    def show_unique_results(self, list_):
        unique_list = []
        unique_genome_list = []
        for elem in list_:
            if elem.get_genome() not in unique_genome_list:
                unique_list.append(elem)
                unique_genome_list.append(elem.get_genome())
        return unique_list, [self.GENOM_LENGTH, self.POPULATION_LENGTH, self.CROSSING_CHANCE,
                             self.MUTATION_CHANCE, self.POPULATION_LENGTH,
                             self.TARGET_CALORIES, self.TARGET_BZU]



if __name__ == "__main__":
    results = run_simulation(all_products)
    unique_results = show_unique_results(results)
    # print()
    # for i in unique_results:
    #     print(i.calories, i.get_genome(), round(i.fitness_points, 0))
