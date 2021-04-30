from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Docitems, Document, editRecord
from django.conf import settings
import csv, os
from django.http import HttpResponse
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    form = CreateUserForm()
    context = {'form': form }
    return render(request, 'accounts/register.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user  = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            # else:
                # messages.info(request, '用户名或密码不正确')
    context = {}
    return render(request, 'accounts/login.html', context)

# @login_required(login_url='login')
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    context = {
        "documents": Document.objects.all(),
        'd_block': 'd-none'
    }
    if request.method == 'POST':
        if 'download' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="filename.csv"'
            writer = csv.writer(response)
            writer.writerow(['label','review','last_edit_time'])
            data = Docitems.objects.filter(document__id=request.POST['selectedFile'])
            for row in data:
                rowobj = [row.label, row.review, row.last_edit_time]
                writer.writerow(rowobj)
            return response 
        if 'upload' in request.POST:
            newdoc = Document.objects.create(file=request.FILES['docfile'], uploader=request.user)
            file = os.path.join(settings.MEDIA_ROOT, 'csv', request.FILES['docfile'].name)
            with open(file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                for record in reader:
                    Docitems.objects.create(document=newdoc, review=record[1])
                    # messages.info(request, '入库成功')
            editRecord.objects.create(file=newdoc, editor=request.user)
        if 'edit' in request.POST:
            selectedDoc = Document.objects.get(id=request.POST['selectedFile'])
            edit_record = editRecord.objects.get(editor=request.user, file=selectedDoc)
            edit_record_row = edit_record.last_edit_row
            if edit_record_row == 0:
                cur_edit = Docitems.objects.filter(document__id=request.POST['selectedFile']).first()
            else:
                cur_edit = Docitems.objects.filter(id=edit_record_row)
            context['cur_edit'] = cur_edit
            context['d_block'] = ""
        if 'previous' in request.POST:
            cur_edit = Docitems.objects.get(id=int(request.POST['docitemsid'])-1)
            context['cur_edit'] = cur_edit
            context['d_block'] = ""
        if 'next' in request.POST:
            nextrow = int(request.POST['docitemsid'])+1
            cur_edit = Docitems.objects.get(id=nextrow)
            context['cur_edit'] = cur_edit
            context['d_block'] = ""
        if 'negative' in request.POST:
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor1=None).update(editor1=request.user.username, label1=-1)
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor2=None).update(editor2=request.user.username, label2=-1)
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor3=None).update(editor3=request.user.username, label3=-1)
            cur_edit = Docitems.objects.get(id=int(request.POST['docitemsid'])+1)
            print("cur_edit is:", cur_edit)
            context['cur_edit'] = cur_edit
            context['d_block'] = ""
        if 'flat' in request.POST:
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor1=None).update(editor1=request.user.username, label1=0)
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor2=None).update(editor2=request.user.username, label2=0)
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor3=None).update(editor3=request.user.username, label3=0)
            cur_edit = Docitems.objects.get(id=int(request.POST['docitemsid'])+1)
            context['cur_edit'] = cur_edit
            context['d_block'] = ""
        if 'positive' in request.POST:
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor1=None).update(editor1=request.user.username, label1=1)
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor2=None).update(editor2=request.user.username, label2=1)
            cur_edit = Docitems.objects.filter(id=request.POST['docitemsid'], editor3=None).update(editor3=request.user.username, label3=1)
            cur_edit = Docitems.objects.get(id=int(request.POST['docitemsid'])+1)
            context['cur_edit'] = cur_edit
            context['d_block'] = ""
    return render(request, 'accounts/index.html', context)
