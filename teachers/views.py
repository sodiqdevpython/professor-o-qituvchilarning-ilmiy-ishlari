from django.shortcuts import render, redirect
from datetime import datetime
from documents.models import Document
from books.models import Book
from django.views import View
from .forms import DocumentForm, BookForm

class UserDashboard(View):
    def get(self, request):
        user = request.user

        # ✅ Yanvardan boshlab barcha oylarga qarab statistikani olish
        today = datetime.today()
        months = [datetime(today.year, i, 1).strftime('%B') for i in range(1, 13)]  # Yanvardan Dekabrgacha

        document_activity = [
            Document.objects.filter(
                author=user,
                created__year=today.year,
                created__month=i
            ).count()
            for i in range(1, 13)  # 1-yanvardan 12-dekabrgacha olish
        ]

        book_activity = [
            Book.objects.filter(
                author=user,
                created__year=today.year,
                created__month=i
            ).count()
            for i in range(1, 13)
        ]

        # Foydalanuvchi tomonidan qo‘shilgan oxirgi hujjatlar va kitoblar
        latest_documents = Document.objects.filter(author=user).order_by('-created')[:5]
        latest_books = Book.objects.filter(author=user).order_by('-created')[:5]

        context = {
            'months': months,  # ✅ Yanvardan boshlab barcha oylari bor
            'document_activity': document_activity,
            'book_activity': book_activity,
            'latest_documents': latest_documents,
            'latest_books': latest_books,
        }
        return render(request, 'teacher/dashboard.html', context)

class UserDocumentsView(View):
    def get(self, request):
        documents = Document.objects.filter(author=request.user).order_by('-created')
        return render(request, 'teacher/user_documents_list.html', {'documents': documents})

class UserBooksView(View):
    def get(self, request):
        books = Book.objects.filter(author=request.user).order_by('-created')
        return render(request, 'teacher/user_books_list.html', {'books': books})

# Yangi hujjat qo‘shish
class DocumentCreateView(View):
    def get(self, request):
        form = DocumentForm()
        return render(request, 'teacher/document_create.html', {'form': form})

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user  # Foydalanuvchi o‘zini author qiladi
            document.is_confirmed = False  # Har doim tasdiqlanmagan
            document.save()
            return redirect('user_documents')
        return render(request, 'teacher/document_create.html', {'form': form})

# Yangi kitob qo‘shish
class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'teacher/book_create.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user  # Foydalanuvchi o‘zini author qiladi
            book.is_confirmed = False  # Har doim tasdiqlanmagan
            book.save()
            return redirect('user_books')
        return render(request, 'teacher/book_create.html', {'form': form})
