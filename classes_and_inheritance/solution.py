import csv
import os
import doctest

car_types = frozenset(("car", "truck", "spec_machine"))
image_extensions = frozenset((".jpg", ".jpeg", ".png", ".gif"))

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        assert(len(brand) > 0)
        assert(len(photo_file_name) > 0)
        assert(os.path.splitext(photo_file_name)[-1] in image_extensions)
        self.brand = brand
        self.carrying = float(carrying)
        self.photo_file_name = photo_file_name

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]

class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        self.car_type = "car"
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        assert(self.passenger_seats_count > 0)

class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        self.car_type = "truck"
        super().__init__(brand, photo_file_name, carrying)
        try:
            self.body_length, self.body_width, self.body_height = map(float, body_whl.split("x"))
        except:
            self.body_length, self.body_width, self.body_height = 0, 0, 0        

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        self.car_type = "spec_machine"
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        assert(len(self.extra) > 0)


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra = row
                assert(car_type in car_types)
                if car_type == "car":
                    car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
                elif car_type == "truck":
                    car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
                elif car_type == "spec_machine":
                    car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))
                else:
                    assert(False)
            except Exception as e:
                continue

    return car_list


def run_tests():
    """
    >>> car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
    >>> print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count, sep='\\n')
    car
    Bugatti Veyron
    bugatti.png
    0.312
    2

    >>> truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
    >>> print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length, truck.body_width, truck.body_height, sep='\\n')
    truck
    Nissan
    nissan.jpeg
    3.92
    2.09
    1.87


    >>> spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
    >>> print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying, spec_machine.photo_file_name, spec_machine.extra, sep='\\n')
    spec_machine
    Komatsu-D355
    93.0
    d355.jpg
    pipelayer specs


    >>> spec_machine.get_photo_file_ext()
    '.jpg'

    >>> cars = get_car_list('cars.csv')
    >>> len(cars)
    4
    >>> for car in cars:
    ...     print(type(car))
    <class '__main__.Car'>
    <class '__main__.Truck'>
    <class '__main__.Truck'>
    <class '__main__.Car'>
    >>> cars[0].passenger_seats_count
    4
    >>> cars[1].get_body_volume()
    60.0
    """
    return


if __name__ == "__main__":
    doctest.testmod()

