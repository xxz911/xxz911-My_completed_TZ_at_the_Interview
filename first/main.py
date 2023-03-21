import time
import logging
import configparser


# Логирование
file_log = logging.FileHandler("main_log.log")
console_out = logging.StreamHandler()


# Добавить console_out в handlers для отображения логов в терминале
logging.basicConfig(handlers=(file_log,), level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logging.debug("Это сообщение для отладки программы")
logging.info("Информационное сообщение")
logging.warning('Предупреждение — нужно проверить, всё ли в порядке')
logging.error("Ошибка! Что-то пошло не так")
logging.critical("Критическая ошибка")


# Подключаем файл конфигурации
config = configparser.ConfigParser()
config.read("settings.ini")


class Teapot:
    def __init__(self, water=0):
        # Вызов значений из файла конфигурации
        self.time = int(config["SettingsClass"]["time"])
        self.max_water = float(config["SettingsClass"]["max_water"])

        self.water = water
        self.status = 'Выключен'

    # Метод выбора пользователя
    def get_menu(self):

        logging.info("\nЗапускаем get_menu")

        wrapper = True
        while wrapper:
            try:
                self.get_status()
                x = int(input('Введите номер кнопки: \n1 Запустить чайник?\n2 Залить воду?\n'))
                if x == 1:
                    wrapper = False
                    return self.run()
                elif x == 2:
                    wrapper = False
                    return self.get_water()
                else:
                    raise ValueError
            except ValueError:
                continue

    # Метод для получения статуса чайника с подсказкой о горячих клавишах
    def get_status(self):
        print("\n< Чайник: " + self.status, ">\n< CTRL + Z (Отключить  чайник) /  CTRL + C  (Остановить чайник) >\n")

    def get_water(self):

        logging.info("\nЗапускаем get_water")

        while 1:
            try:
                self.get_status()
                print(f"Колличество воды должно быть от 0 до {self.max_water}")
                water = float(input('Залейте воду: \n'))

                logging.warning("\nЗначение воды 0")

                if 0 <= water <= self.max_water:
                    self.water = water
                    return self.get_menu()
                else:
                    raise ValueError
            except ValueError:
                print(f"Колличество воды должно быть от 0 до {self.max_water}")
                print("Нажмите CTRL + C чтобы отключить чайник\n")

                logging.error("\nОшибка! Введены Неверные данные в water")

                continue

    # Метод запуска чайника
    def run(self):

        logging.info("\nЗапускаем run")

        for sec in range(1, self.time + 1):
            # Защита от запуска без воды
            if self.water == 0:

                logging.warning("\nЗначение воды 0")

                print("\nВ чайнике нет воды, залейте воду!")
                return self.get_menu()
            # Метод работы чайника с водой
            try:
                time.sleep(1)
                total = sec * (100 / self.time)
                total = round(total, 1)
                self.status = "Включен"

                # Смена статуса на последней секунде
                if sec == self.time:
                    self.status = "Закипел и Выключился"

                self.get_status()
                print("Температура воды :" + str(total) + " градусов")
            except KeyboardInterrupt:
                self.status = "Остановлен"

                logging.warning('\nОстановлено кипячение')

                break
        self.get_status()
        return self.get_menu()


# Создание экземпляра класса
MyTeapot = Teapot()

# Поведение экземпляра класса
MyTeapot.get_menu()
MyTeapot.get_water()
