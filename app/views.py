from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q, Count
from .models import CarMaker, CarModel, Car, GEARBOXES
from django.core.paginator import Paginator
from .utils import get_pages_list

# Create your views here.


class Index(View):

    template = 'app/index.html'

    def get(self, request):

        context = {}

        context['title'] = 'Каталог автомобилей'

        # подготовим Q объекты для фильтрации списка
        q_maker = Q()
        q_model = Q()
        q_year = Q()
        q_color = Q()
        q_gearbox = Q()

        # Отслеживаемые поля фильтров
        FIELDS = [
            'reset',
            'maker',
            'model',
            'gearbox',
            'color',
            'year',
            'orderby',
        ]

        # Читаем параметры из GET запроса и сохраняем в сессионный ключ filters_data
        # Если параметра в GET нет, то соотвествующие поле не трогаем
        # иначе меняем это поле
        for field in FIELDS:
            # print(f"\nfield = {field}")
            if request.GET.get(field):
                print(
                    f'\nrequest.GET.getlist({field}) = {request.GET.getlist(field)}')
                request.session[field] = request.GET.getlist(field)
            print(
                f"\nrequest.session['{field}'] = {request.session.get(field)}")

        # Если пришел GET параметр reset с любым значение, сбрасываем filters_data
        if request.session.get('reset'):
            for field in FIELDS:
                request.session[field] = []
                print(
                    f"\nrequest.session['{field}'] = {request.session[field]}")

        # Варианты сортировки результирующего списка
        ORDER_BY = {
            '0': 'car_model__car_maker',
            '1': 'car_model',
            '2': 'year',
            '3': 'color',
            '4': 'gearbox',
        }

        orderby_list = request.session.get('orderby', [])
        if len(orderby_list) > 0:
            order_by = ORDER_BY.get(orderby_list[0], ORDER_BY['0'])
        else:
            order_by = ORDER_BY['0']
        print(order_by)

        # Подготовим Q - объекты в зависимости от filters_data
        for maker in request.session.get('maker', []):
            q_maker = q_maker | Q(car_model__car_maker__slug=maker)

        for model in request.session.get('model', []):
            q_model = q_model | Q(car_model__slug=model)

        for gearbox in request.session.get('gearbox', []):
            q_gearbox = q_gearbox | Q(gearbox=gearbox)

        for year in request.session.get('year', []):
            q_year = q_year | Q(year=year)

        for color in request.session.get('color', []):
            q_color = q_color | Q(color=color)

        # Получаем список автомобилей с учетом Q-фильтрации
        cars = Car.objects.select_related('car_model__car_maker').order_by(
            order_by).filter(q_model & q_maker & q_gearbox & q_year & q_color)

        # Запрос для получения списка моделей после учета фильтров
        # список оторажается в вариантах для вибора в поле input
        models = cars.order_by().select_related('car_maker').values(
            'car_model__name', 'car_model__slug', 'car_model__car_maker__name').distinct()

        # Аналогично для  списка доступных производителей
        makers = cars.order_by().values('car_model__car_maker__name',
                                        'car_model__car_maker__slug').distinct()

        # Аналогично для списка доступных цветов
        colors = cars.order_by().values('color').distinct()

        # Аналогично для списка доступных КПП
        # но так как values дает странный список словарей, метод get_gearbox_display не срабатывает
        # пришлось городить огород
        gearboxes = cars.order_by().values('gearbox').distinct()
        temp = {x[0]: x[1] for x in GEARBOXES}
        gearboxes = {x['gearbox']: temp[x['gearbox']] for x in gearboxes}

        # Аналогично для списка годов
        # Удивительно, но филтрация работает странно
# НУЖНО ПОПРАВИТЬ ФИЛЬТРАЦИЮ
        years = cars.order_by().values('year').distinct()

        # Подготовим пагинатор страницы
        paginator = Paginator(cars, 15)

        # Получим номер страницы пагинатора из get параметров
        page = request.GET.get('page', '1')

        # _____________________________________________________________
        # Очистим результат
        # - Приведем к int
        # - если не вышло, то 1
        # - если привели к int, но не попали в рамки, приводим в рамки
        try:
            page = int(page)
        except:
            page = 1

        if page < 1:
            page = 1
        elif page > paginator.num_pages:
            page = paginator.num_pages
        # _____________________________________________________________

        # подготовим список авто с учетом пагинатора
        context['car_list'] = paginator.get_page(page)
        
        # Подготовим ссылки для переключения страниц пагинатора

        # кол-во вскладок на страницу
        quantity_pages = 5
        pages = get_pages_list(page, quantity_pages, 1, paginator.num_pages)
        context['pages'] = pages

        context['car_model_list'] = models
        context['car_maker_list'] = makers
        context['gearbox_list'] = gearboxes
        context['color_list'] = colors
        context['year_list'] = years

        return render(request, self.template, context=context)

    def post(self, request):
        pass


class CarModelDetailView(View):
    model = CarModel
    template = 'app/car_model_detail.html'

    def get(self, request, slug):
        try:
            obj = self.model.objects.select_related('car_maker').get(slug=slug)
        except:
            raise Http404('No %s matches the given query.' %
                          self.model._meta.object_name)
        # obj = get_object_or_404(self.model, slug_iexact=slug)
        context = {
            self.model.__name__.lower(): obj
        }

        return render(request, self.template, context=context)


class CarMakerDetailView(DetailView):
    template_name = 'app/car_maker_detail.html'
    model = CarMaker


class CarModelListView(ListView):
    model = CarModel
    template_name = 'app/models_list.html'
    context_object_name = 'models'
    paginate_by = 30
    queryset = CarModel.objects.select_related('car_maker').annotate(car_count=Count("cars")).all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


class CarMakerListView(ListView):
    model = CarMaker
    template_name = 'app/makers_list.html'
    context_object_name = 'makers'
    paginate_by = 30
    queryset = CarMaker.objects.annotate(model_count=Count('car_models')).all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context