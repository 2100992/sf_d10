from slugify import slugify
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import render


def make_unique_slug(model, text):
    slug = slugify(text)
    counter = 0
    str_counter = ''

    while model.objects.filter(slug=slug+str_counter).count():
        print(slug+str_counter)
        counter += 1
        str_counter = str(counter)
    return slug + str_counter


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug_iexact=slug)
        context = {
            self.model.__name__.lower(): obj
        }

        return render(request, self.template, context=context)



def get_pages_list(page, quantity_pages, p_min, p_max):
    '''
    Подготовка ссылок пагинатора
    page - номер текущей страницы
    quantity_pages - кол-во вскладок на страницу
    p_min - первая страница полного массива (чаще всего 1)
    p_max - последняя страница полного массива

    Результат на выходе get_pages_list(14, 5, 1, 120)

    get_pages_list(14, 5, 1, 120) = [
        {'n':'1', 'name':'first'},
        {'n':'11', 'name':'previous'},
        {'n':'12', 'name':''},
        {'n':'13', 'name':''},
        {'n':'14', 'name':'current'},
        {'n':'15', 'name':''},
        {'n':'16', 'name':''},
        {'n':'17', 'name':'next'},
        {'n':'120', 'name':'last'},
        ]


    '''

    # округление в большую сторону
    from math import ceil

    # округление в меньшую сторону
    from math import floor

    # размер полного массива
    len_list = p_max - (p_min - 1)

     # количество сетов
    quantity_set = ceil(len_list/quantity_pages)

    # номер текущего сета
    set_number = ceil(page/quantity_pages)-1

    # 
    current_set = []

    current_set.append({'n': p_min, 'name': 'first'})

    sets_first_page = p_min + (set_number * quantity_pages)
    sets_last_page = sets_first_page + quantity_pages

    if sets_first_page > p_min:
        current_set.append({'n': sets_first_page - 1, 'name': 'previous'})
    else:
        current_set.append({'n': p_min, 'name': 'previous_inactiv'})

    for i in range(sets_first_page, sets_last_page):
        name = ''
        if i > p_max:
            continue
        if i == page:
            name = 'current'
        current_set.append({'n': i, 'name': name})
    
    if sets_last_page < p_max:
        current_set.append({'n': sets_last_page, 'name': 'next'})
    else:
        current_set.append({'n': p_max, 'name': 'next_inactiv'})

    current_set.append({'name': 'last', 'n': p_max})
    return current_set
