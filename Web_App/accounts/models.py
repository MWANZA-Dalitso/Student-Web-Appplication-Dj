from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from .utils import get_academic_years
from .choices import GENDER_CHOICES, CIVIL_STATUS_CHOICES

def validate_passport_number(value):
    if not value.startswith('ZN') or len(value) != 8:
        raise ValidationError('Passport number must start with "ZN" and be 8 characters long.')

def validate_phone_number(value):
    if not value.startswith('+212') or len(value) != 13:
        raise ValidationError('Phone number must start with "+212" and be 13 characters long.')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    date_of_birth = models.DateField(default=timezone.now)
    passport_number = models.CharField(max_length=8, blank=True, validators=[validate_passport_number])
    bc_number = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=13, blank=True, validators=[validate_phone_number])
    program_of_study = models.CharField(max_length=100, blank=True)
    level_of_study = models.ForeignKey('LevelOfStudy', on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True, blank=True)
    city_of_birth = models.CharField(max_length=100, blank=True)  # Changed to CharField
    province_of_birth = models.CharField(max_length=100, blank=True)  # Changed to CharField
    province_in_morocco = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    inscription_year = models.CharField(max_length=9, choices=get_academic_years(), blank=True)
    avatar = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class LevelOfStudy(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Removed CityOfBirth model
