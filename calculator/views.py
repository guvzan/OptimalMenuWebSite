from django.shortcuts import render

from .genetic import Genetic
from .models import Product


def main_page(request):
    context = {
        'products': get_products(),
        'menues': get_menues()
    }
    return render(request, 'calculator/index.html', context)

def get_products():
    all_products = Product.objects.all()
    return all_products

    GENOM_LENGTH = 10
    POPULATION_LENGTH = 200
    CROSSING_CHANCE = 90
    MUTATION_CHANCE = 5
    GENERATIONS_NEEDED = 500
    TARGET_CALORIES = 1500
    TARGET_BZU = [20, 40, 20]

def get_menues():
    gen = Genetic()
    gen.set_settings(5, 16, 90, 5, 100, 1000, [100, 0, 2])
    results = gen.run_simulation(get_products())
    unique_results = gen.show_unique_results(results)
    return [(menu.calories, menu.count_bzu(), menu.get_genome()) for menu in unique_results]
