import time
import datetime

from industry import Product
from industry import PackedMilk, Milk


# LOGISTICS
class Transport:
    def __init__(self, speed: float, volume: float, weight: float, temperature: float):
        """
        :param speed: Скорость транспорта
        :param volume: Объем кузова
        :param weight: Максимально возможный вес груза
        :param temperature: Температура в кузове (грузовой части салона)
        :rtype: None
        """
        self.speed = speed
        self.volume = volume
        self.temperature = temperature
        self.weight = weight

        self.products: list[Product] = []

        if not (isinstance(speed, int) or isinstance(speed, float)):
            raise TypeError("speed must be an integer or float")
        if not (isinstance(volume, int) or isinstance(volume, float)):
            raise TypeError("volume must be an integer or float")
        if not (isinstance(temperature, int) or isinstance(temperature, float)):
            raise TypeError("temperature must be an integer or float")
        if not (isinstance(weight, int) or isinstance(weight, float)):
            raise TypeError("weight must be an integer or float")

    def load(self, products) -> bool:
        summary_weight, summary_volume = 0, 0
        for item in products:
            if not issubclass(item.__class__, Product): # Проверяем, что элемент - продукт или его дочерний класс
                raise TypeError("product must be Product or or its child class")
            summary_weight += item.weight
            summary_volume += item.product_volume
            if (summary_weight > self.weight) or (summary_volume > self.volume):
                return False
            time.sleep(1)

        # Уменьшаем макс. возможный вес для данного объекта (1 конкретной машины, в которой уже лежит часть груза)
        self.weight -= summary_weight
        self.volume -= summary_volume
        # Закидываем груз в машину
        self.products += products
        return True

    def transportation(self, distance: float):
        time.sleep(distance / self.speed)

    def unload(self):
        for item in self.products:
            self.weight += item.weight
            self.volume += item.product_volume
            time.sleep(1)

    def __str__(self):
        description = f'''Max Speed: {self.speed}
Free volume: {self.volume}
Free weight: {self.weight}
Temperature: {self.temperature}
Cargo: {len(self.products)} item(s)'''
        return description


class TransportBox:
    def __init__(self, weight, volume, temperature, products):
        self.weight = weight
        self.volume = volume
        self.temperature = temperature
        self.products = products


class Truck3(Transport): pass
class Truck5(Transport): pass
class Truck10(Transport): pass
class Truck20(Transport): pass
class Truck50(Transport): pass
class Truck55(Transport): pass


# -------------------------------
if __name__ == '__main__':
    import random
    milk_crate = []
    for i in range(5):
        milk = PackedMilk(heat_treatment=Milk.NOT_PASTEURIZED,
                          fat_percent=random.choice([10, 20, 30]),
                          product_volume=2,
                          product_expiration_date=datetime.timedelta(days=5),
                          weight=0.8,
                          recommended_temperature=3,
                          current_temperature=2,
                          material='glass',
                          tightness=True,
                          pack_volume=2,
                          pack_expiration_date=datetime.timedelta(days=3)
                          )
        milk_crate.append(milk)

    car_a = Transport(
        speed=10,
        volume=50,
        weight=100,
        temperature=36.6,
    )
    print("\tПример транспорта:"+str(car_a), end='\n\n')

    if car_a.load(milk_crate):
        print("Молоко успешно погружено")
    else:
        print("Возникли проблемы при погрузке")

    print("\n*****************\n\tПример загруженной машины:\n" + str(car_a))
    print("\n*****************\n\tВ кузове лежит (I элемент):\n" + str(car_a.products[0]))

    car_a.transportation(20)
    car_a.unload()
    print("\n*****************\n\tПосле разгрузки:\n" + str(car_a))
    
    # TODO: Округлять float до 3 (n-ного) знака после запятой / рассмотреть использование библиотеки decimal
    # Иначе возможны "неточности" вида: Free weight: 99.99999999999999 вместо 100
