from django import forms
from users.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Parolni kiriting"
        }),
        label=("Parol"),
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'tel_number', 'type', 'username',
            'faculty', 'profile_image'
        ]
        labels = {
            'first_name': ('Ism'),
            'last_name': ('Familiya'),
            'tel_number': ('Telefon raqami'),
            'username': ('ID raqam'),
            'type': ('Foydalanuvchi turi'),
            'faculty': ('Fakultet'),
            'is_active': ('Faol holat'),
            'profile_image': ('Profil rasmi'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ismni kiriting"
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "ID raqam"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Familiyani kiriting"
            }),
            'tel_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Telefon raqamini kiriting"
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data['password'])  # Parolni o‘rnatish
        if commit:
            user.save()
        return user
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'tel_number', 'faculty', 'type', 'profile_image']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ismni kiriting"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Familiyani kiriting"
            }),
            'tel_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Telefon raqamini kiriting"
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control-file'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Qo'shimcha dekor yoki label'larni ham shu yerda sozlashingiz mumkin
        self.fields['first_name'].label = "Ism"
        self.fields['last_name'].label = "Familiya"
        self.fields['tel_number'].label = "Telefon"
        self.fields['faculty'].label = "Fakultet"
        self.fields['type'].label = "Foydalanuvchi roli"
        self.fields['profile_image'].label = "Profil rasmi"


class LoginForm(forms.Form):
    username = forms.CharField(max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)