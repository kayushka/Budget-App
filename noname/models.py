from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models import CASCADE

INCOME_CHOICES = (
    (1, "Pensja"),
    (2, "Pensja partnerki/partnera"),
    (3, "Premia"),
    (4, "Sprzedaż"),
    (5, "Inne")
)

EXPENSES_CHOICES = (
    (1, "Jedzenie dom"),
    (2, "Jedzenie na mieście"),
    (3, "Jedzenie w pracy"),
    (4, "Alkohol"),
    (5, "Czynsz"),
    (6, "Woda"),
    (7, "Prąd"),
    (8, "Gaz"),
    (9, "Ogrzewanie"),
    (10, "Wywóz śmieci"),
    (11, "Naprawy"),
    (12, "Wyposażenie"),
    (13, "Ubezpieczenie"),
    (14, "Paliwo"),
    (15, "Naprawa"),
    (16, "Wyposażenie"),
    (17, "Ubezpieczenie"),
    (18, "Bilety"),
    (19, "Taxi"),
    (20, "Telefon"),
    (21, "Telewizja"),
    (22, "Internet"),
    (23, "Lekarz"),
    (24, "Badania"),
    (25, "Leki"),
    (26, "Ubrania"),
    (27, "Buty"),
    (28, "Kosmetyki"),
    (29, "Chemia domowa"),
    (30, "Fryzjer"),
    (31, "Art. szkolne"),
    (32, "Zajęcia dodatkowe"),
    (33, "Szkoła"),
    (34, "Gry/zabawki"),
    (35, "Opieka nad dziećmi"),
    (36, "Sport"),
    (37, "Kino/teatr"),
    (38, "Koncert"),
    (39, "Książki"),
    (40, "Prezenty"),
    (41, "Oszczędności"),
    (42, "Hotel/turystyka"),
    (43, "Hobby"),
    (44, "Edukacja"),
    (45, "Oprogramowanie"),
    (46, "Inne"),
)


class MyUser(AbstractUser):
    pass


class Income(models.Model):
    amount = models.FloatField()
    category = models.IntegerField(choices=INCOME_CHOICES)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=CASCADE)


class Expenses(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    category = models.IntegerField(choices=EXPENSES_CHOICES)
    user = models.ForeignKey(MyUser, on_delete=CASCADE)
