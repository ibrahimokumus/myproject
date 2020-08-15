from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import Category, Book
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    category = Category.objects.all()
    sliderdata = Book.objects.all()[:2]
    setting = Setting.objects.get(pk=1)
    lastbooks = Book.objects.all().order_by('-id')[:9]
    randombooks = Book.objects.all().order_by('?')[:6]
    randombooks2 = Book.objects.all()[:6]
    context = {
        'sliderdata':sliderdata,
        'page':'home',
        'setting': setting,
        'category': category,
        'lastbooks': lastbooks,
        'randombooks': randombooks,
        'randombooks2': randombooks2,
    }
    return render(request,'index.html',context)

def hakkimizda(request):
     category = Category.objects.all()
     setting = Setting.objects.get(pk=1)
     context = {
         'setting': setting,
         'page': hakkimizda,
         'category': category,
     }
     return render(request,'hakkimizda.html',context)

def iletisim(request):
    category = Category.objects.all()
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz..")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'category': category, 'form': form}
    return render(request, 'iletisim.html', context)

def category_books(request,id,slug):
    category = Category.objects.all()
    books = Book.objects.filter(category_id=id)
    context = {'books': books,
               'category': category
               }
    return render(request,'book.html',context)


def books(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    books = Book.objects.all()
    context = {'setting': setting, 'category': category,  'books': books}
    return render(request, 'book.html', context)


