from django.shortcuts import render, get_object_or_404
from .models import Document
from django.views import View
from books.models import Book
from datetime import datetime, timedelta

class DashboardView(View):
	def get(self, request):
		return render(request, 'base.html')
	
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    author = document.author

    # Muallifga tegishli boshqa ilmiy ishlar va kitoblar
    other_documents = Document.objects.filter(author=author).exclude(pk=pk)
    other_books = Book.objects.filter(author=author)

    # Faollik (oxirgi 6 oy bo‘yicha)
    today = datetime.today()
    months = [(today - timedelta(days=30 * i)).strftime('%B %Y') for i in range(6)][::-1]
    activity_data = [
        Document.objects.filter(
            author=author,
            created__year=(today - timedelta(days=30 * i)).year,
            created__month=(today - timedelta(days=30 * i)).month
        ).count()
        for i in range(6)
    ]

    context = {
        'document': document,
        'author': author,
        'other_documents': other_documents,
        'other_books': other_books,
        'months': months,
        'activity_data': activity_data,
    }
    return render(request, 'documents/document_detail.html', context)