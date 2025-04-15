from django import forms
from documents.models import Document
from books.models import Book

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'type', 'file', 'url', 'image', 'more_info']
        labels = {
            'name': 'Hujjat nomi',
            'type': 'Hujjat turi',
            'file': 'Fayl (PDF, Word, Excel)',
            'url': 'Tashqi Havola',
            'image': 'Muqova rasmi',
            'more_info': 'Qo‘shimcha ma‘lumot',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'more_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'type', 'file', 'image', 'more_info']
        labels = {
            'name': 'Kitob nomi',
            'type': 'Kitob turi',
            'file': 'Fayl (PDF, Word, Excel)',
            'image': 'Muqova rasmi',
            'more_info': 'Qo‘shimcha ma‘lumot',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'more_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
