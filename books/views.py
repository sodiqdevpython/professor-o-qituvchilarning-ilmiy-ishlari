from django.shortcuts import render, get_object_or_404
from books.models import Book
from documents.models import Document

# Create your views here.
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    author = book.author

    # Muallifning boshqa kitoblari
    other_books = Book.objects.filter(author=author).exclude(pk=pk)

    # Muallifning boshqa ilmiy ishlari
    other_documents = Document.objects.filter(author=author)

    context = {
        'book': book,
        'author': author,
        'other_books': other_books,
        'other_documents': other_documents,
    }
    return render(request, 'books/book_detail.html', context)