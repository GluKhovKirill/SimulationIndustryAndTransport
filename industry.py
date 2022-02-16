import datetime

# Используется для работы с потоками (в частности, с таймерами, работающими в фоне)
# Не обязательно, поскольку мы реализуем симуляцию с помощью Airflow
import threading


# INDUSTRY
class Pack:
    def __init__(self, material: str, tightness: bool, pack_volume: float, pack_expiration_date: datetime.timedelta):
        """
        :param str material: Материал упаковки
        :param bool tightness: Герметичность не нарушена
        :param float pack_volume: Объем упаковки
        :param datetime.timedelta pack_expiration_date: Срок годности с момента упаковки
        :rtype: None
        """
        self.material = material
        self.tightness = tightness
        self.pack_volume = pack_volume
        self.pack_expiration_duration = pack_expiration_date

        if not isinstance(material, str):
            raise TypeError("material must be a string")
        if not isinstance(tightness, bool):
            raise TypeError("tightness must be boolean")
        if not (isinstance(pack_volume, int) or isinstance(pack_volume, float)):
            raise TypeError("volume must be float or int")
        if not isinstance(pack_expiration_date, datetime.timedelta):
            raise TypeError("pack_expiration_date must be datetime.timedelta")

    def __str__(self):
        description = f'''Material: {self.material}
Tightness: {'yes' if self.tightness else 'no'}
Volume, liters: {self.pack_volume}
Pack exp. date: {self.pack_expiration_duration}'''
        return description

    pass


class Product:
    def __init__(self, product_name: str, product_expiration_date: datetime.timedelta, weight: float,
                 recommended_temperature: float, current_temperature: float, product_volume: float):
        """
        :param str product_name: Название продукта
        :param datetime.timedelta product_expiration_date: Срок годности продукта с момента производства
        :param float weight: Масса нетто
        :param float recommended_temperature: Рекомендуемая температура хранения
        :param float current_temperature: Текущая температура
        :param product_volume: Объем продукта
        :rtype None
        """
        self.product_name = product_name
        self.product_expiration_date = product_expiration_date
        self.weight = weight
        self.recommended_temperature = recommended_temperature
        self.current_temperature = current_temperature
        self.product_volume = product_volume


        if not isinstance(product_name, str):
            raise TypeError("product_name must be string")
        if not isinstance(product_expiration_date, datetime.timedelta):
            raise TypeError("product_expiration_date must be datetime.timedelta")
        if not (isinstance(weight, int) or isinstance(weight, float)):
            raise TypeError("net must be int/float")
        if not (isinstance(recommended_temperature, int) or isinstance(recommended_temperature, float)):
            raise TypeError("recommended_temperature must be float")
        if not (isinstance(current_temperature, int) or isinstance(current_temperature, float)):
            raise TypeError("recommended_temperature must be float")
        if not (isinstance(product_volume, float) or isinstance(product_volume, int)):
            raise TypeError("product_volume must be float or int")

    def __str__(self):
        description = f'''Product name: {self.product_name}
Weight (net), kg: {self.weight}
Recommended temperature: {self.recommended_temperature} C
Current temperature: {self.current_temperature} C
Product exp. date: {self.product_expiration_date}'''
        return description

    pass


class Milk(Product):
    NOT_PASTEURIZED = 'Not pasteurized'

    def __init__(self, heat_treatment: str, fat_percent: float, product_volume: float,
                 product_expiration_date: datetime.timedelta, weight: float, recommended_temperature: float,
                 current_temperature: float):
        """
        :param str heat_treatment: Степень термической обработки
        :param float fat_percent: Жирность молока, в процентах
        :param datetime.timedelta product_expiration_date: Срок хранения с момента производства
        :param float weight: Масса
        :param float recommended_temperature: Рекомендуемая температура хранения
        :param float current_temperature: Текущая температура продукта
        :rtype: None
        """
        super().__init__(product_name='Milk',
                         product_expiration_date=product_expiration_date,
                         weight=weight,
                         recommended_temperature=recommended_temperature,
                         current_temperature=current_temperature,
                         product_volume=product_volume
                         )

        self.heat_treatment = heat_treatment
        self.product_volume = product_volume
        self.fat_percent = fat_percent

        if not isinstance(heat_treatment, str):
            raise TypeError("heat_treatment")
        if not (isinstance(fat_percent, int) or isinstance(fat_percent, float)):
            raise TypeError("fat_percent must be float or integer")

    def __str__(self):
        # Получаем старый шаблон и дописываем новые поля
        description = super().__str__()
        description += f'''\nHeat treatment: {self.heat_treatment}
Product volume: {self.product_volume},
Fat: {self.fat_percent}%'''
        return description

    def __set_pasteurization(self, heat_treatment, expiration_date):
        # "__" - означает, что это приватный (private) метод и его НЕ следует вызывать вне данного класса
        # Присваивание значений
        print(f'Milk successfully pasteurized ({self.heat_treatment} --> {heat_treatment})')
        self.heat_treatment = heat_treatment
        self.product_expiration_date += expiration_date
        print("New expiration_date:", self.product_expiration_date)

    def instant_pasteurization(self):
        # Выполняется только, если молоко еще не было обработано
        if self.heat_treatment == self.NOT_PASTEURIZED:
            # Создаем таймер, который вызовет метод __set_pasteurization через 2 секунды с аргументами, указанными в
            # kwargs
            timer = threading.Timer(interval=2, function=self.__set_pasteurization,
                                    kwargs={'heat_treatment': 'sterilized',
                                            'expiration_date': datetime.timedelta(days=5)})
            timer.start()

    def fast_pasteurization(self):
        # Аналогично с instant_pasteurization
        if self.heat_treatment == self.NOT_PASTEURIZED:
            timer = threading.Timer(interval=10, function=self.__set_pasteurization,
                                    kwargs={'heat_treatment': 'pasteurized',
                                            'expiration_date': datetime.timedelta(days=7)})
            timer.start()

    def long_pasteurization(self):
        # Аналогично с instant_pasteurization
        if self.heat_treatment == self.NOT_PASTEURIZED:
            timer = threading.Timer(interval=20, function=self.__set_pasteurization,
                                    kwargs={'heat_treatment': 'ultra pasteurized',
                                            'expiration_date': datetime.timedelta(days=14)})
            timer.start()


class PackedMilk(Milk, Pack):
    def __init__(self, heat_treatment: str, fat_percent: float, product_volume: float,
                 product_expiration_date: datetime.timedelta, weight: float, recommended_temperature: float,
                 current_temperature: float,
                 material: str, tightness: bool, pack_volume: float, pack_expiration_date: datetime.timedelta
                 ):
        """
        :param str heat_treatment: Степень термической обработки
        :param float fat_percent: Жирность молока, в процентах
        :param float product_volume: Объем
        :param datetime.timedelta product_expiration_date: Срок хранения с момента производства
        :param float weight: Масса
        :param float recommended_temperature: Рекомендуемая температура хранения
        :param float current_temperature: Текущая температура продукта
        :param str material: Материал упаковки
        :param bool tightness: Герметичность не нарушена
        :param float pack_volume: Объем упаковки
        :param datetime.timedelta pack_expiration_date: Срок годности с момента упаковки
        :rtype: None
        """
        Milk.__init__(self,
                      heat_treatment=heat_treatment,
                      fat_percent=fat_percent,
                      product_volume=product_volume,
                      product_expiration_date=product_expiration_date,
                      weight=weight,
                      current_temperature=current_temperature,
                      recommended_temperature=recommended_temperature
                      )

        Pack.__init__(self,
                      material=material,
                      tightness=tightness,
                      pack_volume=pack_volume,
                      pack_expiration_date=pack_expiration_date
                      )

    pass


# -------------------------------
if __name__ == '__main__':
    test_pack = Pack(
        material='glass',
        tightness=True,
        pack_volume=0.5,
        pack_expiration_date=datetime.timedelta(days=5)
    )
    print("\tПример упаковки:\n" + str(test_pack))

    test_product = Product(
        product_name='French fries',
        weight=0.1,
        recommended_temperature=20,
        current_temperature=25,
        product_expiration_date=datetime.timedelta(hours=6),
        product_volume=0.25
    )
    print("\n*****************\n\tПример продукта:\n" + str(test_product))

    milk = Milk(heat_treatment=Milk.NOT_PASTEURIZED,
                fat_percent=20,
                product_volume=50,
                product_expiration_date=datetime.timedelta(days=5),
                weight=20,
                recommended_temperature=3,
                current_temperature=2
                )
    print("\n*****************\n\tПример продукта (молоко):\n" + str(milk))
    milk.instant_pasteurization()
