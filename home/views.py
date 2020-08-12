from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from book.models import Category, Book
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    sliderdata = Book.objects.all()[:2]
    setting = Setting.objects.get(pk=1)
    context = {
        'sliderdata':sliderdata,
        'page':'home',
        'setting': setting,
    }
    return render(request,'index.html',context)

def hakkimizda(request):
     setting = Setting.objects.get(pk=1)
     context = {
         'setting': setting,

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