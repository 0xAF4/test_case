from djmoney.models.fields import MoneyField
from django.db import models


class Job_title(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Должность')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['title']

class Employee(models.Model):
    first_name = models.CharField(max_length=35, verbose_name='Имя')
    second_name = models.CharField(max_length=35, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=35, verbose_name='Отчество')

    Job_title = models.ForeignKey(to='Job_title', on_delete=models.SET_NULL, null=True, verbose_name='Должность')
    hired = models.DateField(auto_now=False, verbose_name='Нанят')
    salary = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11, verbose_name='Зарплата')
    chief = models.ForeignKey(to='Employee', verbose_name='Начальник', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    password = models.CharField(max_length=32, verbose_name='Пароль (MD5)')
    auth_token = models.CharField(max_length=256, verbose_name='Авторизационный токен', null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.second_name + ' ' + self.middle_name

    def salaryfunc(self):
        return str(self.salary.amount) + ' ' + self.salary_currency

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        ordering = ['first_name']
