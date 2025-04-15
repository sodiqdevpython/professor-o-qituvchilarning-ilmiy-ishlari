from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from users.models import Faculty, User
from documents.models import Document, DocumentType
from django.utils import timezone
from books.models import Book
from datetime import date, timedelta
from utils.choices import UserTypeChoices
import calendar
from django.urls import reverse
from users.forms import UserForm, UserUpdateForm, LoginForm
from django.contrib import messages
from documents.models import Requirements
from django.db.models import Q
from django.contrib.auth import authenticate, login
import io
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.defaulttags import register

@register.filter
def get(dictionary, key):
    """Template ichida dict dan element olish"""
    return dictionary.get(key, "-")

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('admin_dashboard')
        return render(request, 'users/login.html')

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            get_data = form.cleaned_data
            user = authenticate(request, username=get_data['username'], password=get_data['password'])
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashoard')
            else:
                error_message = "ID raqam yoki parol xato !"

                context = {
                    'form': form,
                    'error_message': error_message
                }
                return render(request, 'login.html', context)
        else:
            error_message = "Ma'lumotlar to'liq va to'g'ri kiritilishi shart!"
            return render(request, 'login.html', {'form': form, 'error_message': error_message})

class DashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_superuser:
            return redirect('user_dashoard')
        # Fakultet bo‘yicha foydalanuvchilar statistikasi
        faculties = Faculty.objects.annotate(user_count=Count('user'))

        # Hujjatlar statistikasi (oylar bo‘yicha)
        today = date.today()
        months = [(today.replace(day=1) - timedelta(days=30 * i)) for i in range(11, -1, -1)]
        document_monthly_stats = [
            Document.objects.filter(
                created__year=month.year, created__month=month.month
            ).count()
            for month in months
        ]

        # Hujjat turlari statistikasi
        document_types_data = {
            "labels": [doc_type.name for doc_type in DocumentType.objects.all()],
            "data": [
                Document.objects.filter(type=doc_type).count()
                for doc_type in DocumentType.objects.all()
            ],
        }

        # Kitoblar statistikasi (oylar bo‘yicha)
        book_monthly_stats = [
            Book.objects.filter(
                created__year=month.year, created__month=month.month
            ).count()
            for month in months
        ]

        # Oxirgi harakatlar (oxirgi 10 ta hujjat va kitob)
        last_documents = Document.objects.select_related('author').order_by('-created')[:5]
        last_books = Book.objects.select_related('author').order_by('-created')[:5]

        # Oylik nomlarni O‘zbek tiliga o‘tkazish
        uzbek_months = [
            "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
            "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
        ]
        month_labels = [f"{uzbek_months[month.month - 1]} {month.year}" for month in months]

        context = {
            "faculties": faculties,
            "document_monthly_stats": document_monthly_stats,
            "document_types_data": document_types_data,
            "book_monthly_stats": book_monthly_stats,
            "month_labels": month_labels,
            "last_documents": last_documents,
            "last_books": last_books,
        }

        return render(request, "users/dashboard.html", context)

def users_list(request):
    # Foydalanuvchi turi va fakultet bo‘yicha filtrlar
    user_type = request.GET.get('user_type')
    faculty_id = request.GET.get('faculty_id')

    users = User.objects.all().order_by('id') 

    if user_type:
        users = users.filter(type=user_type)
    if faculty_id:
        users = users.filter(faculty_id=faculty_id)

    # Fakultetlar ro‘yxati filtrlash uchun
    faculties = Faculty.objects.all()

    # Paginator (20 talik bo‘lib chiqadi)
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user_types': UserTypeChoices.choices,
        'faculties': faculties,
        'selected_user_type': user_type,
        'selected_faculty_id': faculty_id
    }
    return render(request, 'users/user_list.html', context)

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchi muvaffaqiyatli qo‘shildi!")
            return redirect(reverse('users_list'))
        else:
            messages.error(request, "Foydalanuvchi qo‘shishda xatolik yuz berdi.")
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'users/add_user.html', context)


def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    
    # 1) REQUIREMENTS – foydalanuvchiga bog‘liq barcha
    requirements = Requirements.objects.filter(user=user_obj)

    # 2) Yil bo‘yicha filtrlash (chart uchun)
    current_year = timezone.now().year
    selected_year = request.GET.get('req_year')
    if selected_year:
        try:
            selected_year = int(selected_year)
        except ValueError:
            selected_year = current_year
    else:
        selected_year = current_year

    # Yil bo‘yicha filterlangan requirements
    requirements_qs = requirements.filter(created__year=selected_year)

    # Diagramma ma’lumotlarini shakllantirish
    chart_labels = []
    chart_reja_data = []
    chart_amalda_data = []
    for req in requirements_qs.select_related('document_type', 'document_type__subtitle'):
        label = req.document_type.name
        if req.document_type.subtitle:
            label += f" ({req.document_type.subtitle.name})"
        chart_labels.append(label)
        chart_reja_data.append(req.numbers)   # Reja
        chart_amalda_data.append(req.in_use)  # Amalda

    # Tanlash mumkin bo‘lgan yillar ro‘yxati (hozircha 5 yillik)
    years_list = list(range(current_year - 4, current_year + 1))

    # 3) DOCUMENTS – tur (type) bo‘yicha filtrlash (GET param 'doc_type')
    documents = Document.objects.filter(author=user_obj)
    document_types = DocumentType.objects.all()
    selected_type = request.GET.get('doc_type')
    if selected_type:
        documents = documents.filter(type__id=selected_type)

    # 4) BOOKS – foydalanuvchining qo‘shgan kitoblari
    books = Book.objects.filter(author=user_obj)

    # 5) TIMELINE – Document.history.model orqali
    DocumentHistory = Document.history.model
    history_records = (
        DocumentHistory.objects
        .filter(author=user_obj)
        .order_by('-history_date')
    )

    # 6) FAOLLIK – so'nggi 6 oyda qancha document qo‘shganini ko‘rsatish (line chart)
    now = timezone.now()
    faollik_months = []
    faollik_counts = []
    for i in range(6):
        target_month = now.month - i
        target_year = now.year
        while target_month <= 0:
            target_month += 12
            target_year -= 1

        monthly_count = Document.objects.filter(
            author=user_obj,
            created__year=target_year,
            created__month=target_month
        ).count()

        month_name = calendar.month_abbr[target_month]  # "Jan", "Feb", ...
        faollik_months.append(f"{month_name} {target_year}")
        faollik_counts.append(monthly_count)

    # Eskidan yangiga qarab yurish uchun reverse
    faollik_months.reverse()
    faollik_counts.reverse()

    # 7) Kontekst
    context = {
        'user_profile': user_obj,
        'requirements': requirements,          # Jadvalda ko‘rsatish uchun umumiy
        'documents': documents,
        'document_types': document_types,
        'selected_type': selected_type,
        'books': books,
        'timeline_records': history_records,
        'faollik_months': faollik_months,
        'faollik_counts': faollik_counts,

        # Requirements chart ma’lumotlari
        'req_chart_labels': chart_labels,
        'req_chart_reja': chart_reja_data,
        'req_chart_amalda': chart_amalda_data,
        'req_years_list': years_list,
        'req_selected_year': selected_year,
    }
    return render(request, 'users/user-detail.html', context)


def user_update(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchi ma'lumotlari muvaffaqiyatli yangilandi!")
            return redirect('user_detail', pk=user_obj.pk)  # user_detail yoki boshqa URL'ga qaytarish
        else:
            messages.error(request, "Xatolik yuz berdi. Form ma'lumotlarini tekshiring.")
    else:
        form = UserUpdateForm(instance=user_obj)

    context = {
        'form': form,
        'user_obj': user_obj,
    }
    return render(request, 'users/user_update.html', context)


def scientific_works(request):
    # Filtrlar
    faculty = request.GET.get('faculty')
    doc_type = request.GET.get('document_type')
    search_query = request.GET.get('q', '')

    documents = Document.objects.all().order_by('-created')

    if faculty:
        documents = documents.filter(author__faculty__name=faculty)
    if doc_type:
        documents = documents.filter(type__name=doc_type)
    if search_query:
        documents = documents.filter(
            Q(name__icontains=search_query) |
            Q(author__first_name__icontains=search_query) |
            Q(author__last_name__icontains=search_query)
        )

    # Paginatsiya
    paginator = Paginator(documents, 20)  # Har bir sahifada 20 ta
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fakultetlar va hujjat turlari uchun ro‘yxat
    faculties = Faculty.objects.all()
    document_types = DocumentType.objects.all()

    context = {
        'page_obj': page_obj,
        'faculties': faculties,
        'document_types': document_types,
    }
    return render(request, 'documents/scientific_works.html', context)

def books(request):
    # Filtrlar
    book_type = request.GET.get('book_type')
    search_query = request.GET.get('q', '')

    books = Book.objects.all().order_by('-created')

    if book_type:
        books = books.filter(type__name__icontains=book_type)
    if search_query:
        books = books.filter(
            Q(name__icontains=search_query) |
            Q(author__first_name__icontains=search_query) |
            Q(author__last_name__icontains=search_query)
        )

    # Paginatsiya
    paginator = Paginator(books, 20)  # Har bir sahifada 20 ta
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'book_types': Book.objects.values_list('type__name', flat=True).distinct(),
    }
    return render(request, 'books/books.html', context)


def performance_table(request):
    # Fakultet va hujjat turlarini olish
    faculties = Faculty.objects.all()
    document_types = DocumentType.objects.all()

    # Foydalanuvchi filtrlarini olish
    selected_faculty = request.GET.get('faculty', None)
    selected_doc_type = request.GET.get('document_type', None)

    # Filtrlangan ma'lumotlarni olish
    filters = {}
    if selected_faculty:
        filters['user__faculty_id'] = selected_faculty
    if selected_doc_type:
        filters['document_type_id'] = selected_doc_type

    requirements = Requirements.objects.filter(**filters)

    # Foydalanuvchilar va ularning hujjatlari bo'yicha hisob-kitoblar
    users = requirements.values('user__first_name', 'user__last_name').distinct()
    data = []
    total = {}

    for user in users:
        user_data = {
            'id': user['user__first_name'],
            'name': f"{user['user__first_name']} {user['user__last_name']}",
        }

        for req in requirements.filter(user__first_name=user['user__first_name']):
            doc_type = req.document_type.name
            user_data[f"{doc_type}_plan"] = req.numbers
            user_data[f"{doc_type}_actual"] = req.in_use

            # Jami uchun hisoblash
            total[f"{doc_type}_plan"] = total.get(f"{doc_type}_plan", 0) + req.numbers
            total[f"{doc_type}_actual"] = total.get(f"{doc_type}_actual", 0) + req.in_use

        data.append(user_data)

    context = {
        'data': data,
        'total': total,
        'faculties': faculties,
        'document_types': document_types,
        'selected_faculty': selected_faculty,
        'selected_doc_type': selected_doc_type,
    }
    return render(request, 'users/performance_table.html', context)


def performance_download(request, format):
    faculties = Faculty.objects.all()
    selected_faculty = request.GET.get('faculty', None)

    if selected_faculty:
        requirements = Requirements.objects.filter(user__faculty_id=selected_faculty)
    else:
        requirements = Requirements.objects.all()

    users = requirements.values('user__first_name', 'user__last_name').distinct()
    data = []
    total = {}

    for user in users:
        user_data = {
            'name': f"{user['user__first_name']} {user['user__last_name']}",
        }
        for req in requirements.filter(user__first_name=user['user__first_name']):
            doc_type = req.document_type.name
            user_data[f"{doc_type}_plan"] = req.numbers
            user_data[f"{doc_type}_actual"] = req.in_use

            total[f"{doc_type}_plan"] = total.get(f"{doc_type}_plan", 0) + req.numbers
            total[f"{doc_type}_actual"] = total.get(f"{doc_type}_actual", 0) + req.in_use

        data.append(user_data)

    context = {
        'data': data,
        'faculties': faculties,
        'selected_faculty': selected_faculty,
        'total': total,
    }

    if format == "html":
        html_content = render_to_string("users/performance_table.html", context)
        response = HttpResponse(html_content, content_type="text/html")
        response["Content-Disposition"] = 'attachment; filename="performance.html"'
        return response

    elif format == "pdf":
        html_content = render_to_string("users/performance_table.html", context)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("UTF-8")), result)
        if pdf.err:
            return HttpResponse("PDF yaratishda xatolik yuz berdi", content_type="text/plain")
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="performance.pdf"'
        return response

    elif format == "docx":
        doc = Document()
        doc.add_heading("Shaxsiy ish rejalari", level=1)

        table = doc.add_table(rows=1, cols=len(data[0]) if data else 3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "F.I.SH."
        col_index = 1
        for key in total.keys():
            hdr_cells[col_index].text = key.replace("_plan", " (Reja)").replace("_actual", " (Amalda)")
            col_index += 1

        for row in data:
            row_cells = table.add_row().cells
            row_cells[0].text = row["name"]
            col_index = 1
            for key in total.keys():
                row_cells[col_index].text = str(row.get(key, "-"))
                col_index += 1

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response["Content-Disposition"] = 'attachment; filename="performance.docx"'
        doc.save(response)
        return response

    return HttpResponse("Noto‘g‘ri format", content_type="text/plain")