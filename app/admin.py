from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.CarMaker)
class CarMakerAdmin(admin.ModelAdmin):
    # fields = ('name', 'descriptions')
    exclude = ('slug',)

@admin.register(models.CarModel)
class CarModelAdmin(admin.ModelAdmin):
    # fields = ('name', 'car_maker', 'descriptions')
    exclude = ('slug',)

@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    fields = ('car_model', ('color', 'year', 'gearbox'), ('descriptions'))