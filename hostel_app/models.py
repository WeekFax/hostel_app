from django.db import models


class Type(models.Model):

    name = models.CharField(max_length=1000, verbose_name="Название")

    def __str__(self):
        return self.name


class Hostel(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Название")
    address = models.CharField(max_length=1000, verbose_name="Адрес")

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=100, verbose_name="Номер комнаты")
    count_place = models.IntegerField(verbose_name="Кол-во мест")
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, verbose_name="Общежития")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")

    def __str__(self):
        return '{}, комната №{}'.format(self.hostel.name, self.room_number)


class Student(models.Model):
    first_name = models.CharField(max_length=1000, verbose_name="Фамилия")
    second_name = models.CharField(max_length=1000, verbose_name="Имя")
    third_name = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Отчество")
    group = models.CharField(max_length=1000, verbose_name="Группа")
    room = models.ForeignKey(Room, on_delete=models.SET_DEFAULT, null=True, blank=True, verbose_name="Комната", default='')

    def __str__(self):
        if self.third_name == '':
            return "{} {}".format(self.first_name, self.second_name)
        else:
            return "{} {} {}".format(self.first_name, self.second_name, self.third_name)
