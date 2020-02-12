from os import name
from django.db import models
from .utils import make_unique_slug
from random import choice, randint

# Create your models here.

GEARBOXES = [
    (0, 'отсутствует'),
    (1, 'механика'),
    (2, 'автомат'),
    (3, 'робот'),
    (4, 'вариатор'),
    (5, 'редуктор'),
]

COLORS = [
    'Чёрный',
    'Белый',
    'Зеленый',
    'Красный',
    'Синий',
    'Жёлтый',
    'Фиолетовый',
    'Серебрисный',
    'Серый',
    'Золотистый',

]


class CarMaker(models.Model):
    name = models.CharField(
        verbose_name='Производитель',
        max_length=150
    )
    slug = models.SlugField(
        default='_',
        max_length=150,
        unique=True
    )
    descriptions = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = make_unique_slug(CarMaker, self.name)
        super(CarMaker, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(verbose_name='Модель', max_length=150)
    car_maker = models.ForeignKey(
        CarMaker,
        related_name="car_models",
        on_delete=models.DO_NOTHING,
    )
    slug = models.SlugField(default='_', max_length=150, unique=True)
    descriptions = models.TextField(null=True, blank=True)
    start_production = models.SmallIntegerField(null=True, blank=True)
    end_production = models.SmallIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.car_maker:
                self.slug = make_unique_slug(
                    CarModel, self.car_maker.name + " " + self.name)
            else:
                self.slug = make_unique_slug(CarModel, self.name)
        super(CarModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel,
        related_name="cars",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    color = models.CharField(verbose_name="Цвет", max_length=50)
    year = models.SmallIntegerField(verbose_name="Год выпуска")
    gearbox = models.SmallIntegerField(verbose_name=("КПП"), choices=GEARBOXES)
    descriptions = models.TextField(null=True, blank=True)

    def __str__(self):
        return (self.car_model.name + ' ' + self.color + ' ' + str(self.year))
    
    def cars_factory(self, number_of_car):
        '''
        Генератор случайных автомобилей
        '''
        car_models = CarModel.objects.all()
        for _ in range(number_of_car):
            car_model = choice(car_models)
            car = Car()
            car.car_model = car_model
            car.color = choice(COLORS)
            car.gearbox = choice(GEARBOXES[1:4])[0]
            if not car_model.start_production:
                continue
            if car_model.end_production:
                car.year = randint(car_model.start_production, car_model.end_production)
            else:
                car.year = randint(car_model.start_production, 2020) # Добавить вычисление текущего года
            car.save()
        return f'Создано {number_of_car} авто'