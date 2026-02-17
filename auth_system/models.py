from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    IS_USER = 'user'
    IS_MODER = 'moderator'
    IS_ADMIN = 'admin'

    ROLE_CHOICES = [
        (IS_USER, 'Пользователь'),
        (IS_MODER, 'Модератор'),
        (IS_ADMIN, 'Админ')
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default=IS_USER)
    info = models.TextField(max_length=500, blank = True)
    birth_date = models.DateField(null = True, blank=True)
    profile_pic = models.ImageField(upload_to = 'profile_pic', blank = True, null = True,default='profile_pic/default.jpg')


    def is_moder(self):
        return self.role == self.IS_MODER or self.is_staff
    def is_admin(self):
        return self.role == self.IS_ADMIN or self.is_superuser