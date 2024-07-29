from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, University, LevelOfStudy

def validate_passport_number(value):
    if not value.startswith('ZN') or len(value) != 8:
        raise ValidationError('Passport number must start with "ZN" and be 8 characters long.')

def validate_phone_number(value):
    if not value.startswith('+212') or len(value) != 13:
        raise ValidationError('Phone number must start with "+212" and be 13 characters long.')

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control medium',
                'placeholder': f'Enter {fieldname.capitalize()}'
            })

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    city_of_birth = forms.CharField(required=False)  # Changed to CharField
    province_of_birth = forms.CharField(required=False)  # Changed to CharField
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Profile
        fields = [
            'student_name', 'last_name', 'email', 'phone_number', 'passport_number',
            'date_of_birth', 'bc_number', 'university', 'program_of_study',
            'level_of_study', 'city_of_birth', 'province_of_birth',
            'province_in_morocco', 'postal_code', 'address', 'inscription_year',
            'avatar', 'civil_status', 'gender'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control medium',
                'placeholder': f'Enter {fieldname.replace("_", " ").capitalize()}'
            })

    def clean_passport_number(self):
        passport_number = self.cleaned_data.get('passport_number')
        if passport_number and (not passport_number.startswith('ZN') or len(passport_number) != 8):
            raise ValidationError('Passport number must start with "ZN" and be 8 characters long.')
        return passport_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and (not phone_number.startswith('+212') or len(phone_number) != 13):
            raise ValidationError('Phone number must start with "+212" and be 13 characters long.')
        return phone_number



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_name', 'last_name', 'email', 'date_of_birth', 'passport_number', 'bc_number',
                  'phone_number', 'program_of_study', 'level_of_study', 'university', 'city_of_birth',
                  'province_of_birth', 'province_in_morocco', 'postal_code', 'address',
                  'inscription_year', 'avatar', 'civil_status', 'gender']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_name', 'last_name', 'email', 'phone_number', 'passport_number']
