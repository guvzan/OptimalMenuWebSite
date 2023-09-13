from django.shortcuts import render, redirect

from .genetic import Genetic
from .models import Product, ApprovedMenu



def main_page(request):
    """
    Головна сторінка.
    Є кнопка запуску алгоритму.
    """
    return render(request, 'calculator/index.html')


def get_results(request):
    """
    Сторінка, що відображає
    результати пошуку оптимального меню.
    """
    gen = Genetic()
    gen.set_settings(10, 50, 90, 0, 15, 1000, [100, 100, 100])
    if request.method == "POST":
        my_dict = {}
        if 'use_bzu' in request.POST.keys():
            gen.use_bzu(True)
            my_dict['use_bzu'] = True
        else:
            my_dict['use_bzu'] = False
        my_dict['genom_l'] = int(request.POST['genom_l'])
        my_dict['pop_l'] = int(request.POST['pop_l'])
        my_dict['gener_l'] = int(request.POST['gener_l'])
        my_dict['target_c'] = int(request.POST['target_c'])
        my_dict['target_b'] = request.POST['target_b']
        my_dict = validate_gen_settings(my_dict)

        gen.set_settings(
            my_dict['genom_l'],
            my_dict['pop_l'],
            90,
            0,
            my_dict['gener_l'],
            my_dict['target_c'],
            my_dict['target_b']
        )

    menues, settings = get_menues(gen)
    calories = [int(menu[0]) for menu in menues]
    str_calories = [str(i) for i in calories]
    bzu = [menu[1] for menu in menues]
    for i in range(len(bzu)):
        for j in range(len(bzu[0])):
            bzu[i][j] = int(bzu[i][j])
    str_bzu = [''.join(str(i)) for i in bzu]
    genome = [menu[2] for menu in menues]
    str_genome = [''.join(str(i)) for i in genome]
    zipped = zip(calories, bzu, genome, str_calories, str_bzu, str_genome)

    header_string = ''
    if gen.USE_BZU == True:
        header_string = f'Результати для {settings[-2]} калорій та {settings[-1][0]}, {settings[-1][1]}, {settings[-1][2]} БЖВ'
    else:
        header_string = f'Результати для {settings[-2]} калорій'

    context = {
        'zipped': zipped,
        'menues': menues,
        'calories': settings[-2],
        'bzu': settings[-1],
        'header_string': header_string
    }
    return render(request, 'calculator/results.html', context)

def get_products():
    all_products = Product.objects.all()
    return all_products

def get_menues(gen):
    results = gen.run_simulation(get_products())
    unique_results, settings = gen.show_unique_results(results)
    return [(menu.calories, menu.count_bzu(), menu.get_genome()) for menu in unique_results], settings

def validate_gen_settings(dict_):
    if int(dict_['genom_l']) < 5 or int(dict_['genom_l']) > 50:
        dict_['genom_l'] = 15
    if int(dict_['pop_l']) < 5 or int(dict_['pop_l']) > 250:
        dict_['pop_l'] = 100
    if int(dict_['gener_l']) < 10 or int(dict_['gener_l']) > 1000:
        dict_['gener_l'] = 50
    if int(dict_['target_c']) < 1:
        dict_['target_c'] = 1
    if dict_['use_bzu'] == True:
        try:
            bzu = dict_['target_b'].split()
            if len(bzu) == 3:
                for i in range(3):
                    bzu[i] = int(bzu[i])
                dict_['target_b'] = bzu
            else:
                dict_['target_b'] = [90, 60, 250]
        except:
            dict_['target_b'] = [90, 60, 250]
    else:
        dict_['target_b'] = [90, 60, 250]
    return dict_

def add_products_from_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if 'blank' in lines[i]:
                continue
            line = lines[i].split('@')
            product = Product(
                name = line[0],
                calories = line[1],
                bilky = line[2],
                zhury = line[4],
                vuglevody = line[3]
            )
            product.save()



def add_approved_menu(request, calories, bzu, genome):
    new_record = ApprovedMenu(calories=calories, bzu=bzu, menu=genome)
    new_record.save()
    return redirect('calculator:approved_menues')

def show_approved_menues(request):
    menues = ApprovedMenu.objects.all().order_by('calories')
    context = {
        'menues': menues,
    }
    return render(request, 'calculator/approved_menues.html', context)
