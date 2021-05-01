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
# from .text_processing import delete_stopwords, sentence_analyse, test
# from .text_processing import  test
from django.http import JsonResponse
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
        'process_submit_display': 'd-none',
        'process_alert': '',
        'process_alert_display': 'd-none',
        'edit_alert_display': 'd-none'
    }
    if request.method == 'POST':
        if any(x in request.POST for x in ['previous', 'negative', 'flat', 'positive', 'next']):
            first = Docitems.objects.filter(document__id=request.session['selectedDocID']).first().id
            last = Docitems.objects.filter(document__id=request.session['selectedDocID']).last().id
            print('first is  str:', isinstance(request.POST['docitemid'], int))
            print('first is  str:', isinstance(request.POST['docitemid'], str))
            print('first is  str:', request.POST['docitemid'])
            if int(request.POST['docitemid']) == first and 'previous' in request.POST:
                context['process_alert'] = '已经是第一条'
                context['process_submit_display'] = 'd-block'
                context['process_alert_display'] = 'd-block'
                context['cur_edit'] = Docitems.objects.get(id=int(request.POST['docitemid']))
                return render(request, 'accounts/index.html', context)
                
            if int(request.POST['docitemid']) == last and any(x in request.POST for x in ['negative', 'flat', 'positive', 'next']):
                context['process_alert'] = '已经是最后一条'
                context['process_submit_display'] = 'd-block'
                context['process_alert_display'] = 'd-block'
                context['cur_edit'] = Docitems.objects.get(id=int(request.POST['docitemid']))
                return render(request, 'accounts/index.html', context)
        if 'download' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="filename.csv"'
            writer = csv.writer(response)
            writer.writerow(['calculabel','review','last_edit_time','label1', 'label2', 'label3'])
            data = Docitems.objects.filter(document__id=request.POST['selectedFile'])
            for row in data:
                rowobj = [row.calculabel(), row.review, row.last_edit_time, row.label1, row.label2, row.label3]
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
            request.session['selectedDocID'] = request.POST['selectedFile']
            selectedDoc = Document.objects.get(id=request.POST['selectedFile'])
            edit_record = editRecord.objects.get(editor=request.user, file=selectedDoc)
            edit_record_row = edit_record.last_edit_row
            if edit_record_row == 0:
                cur_edit = Docitems.objects.filter(document__id=request.POST['selectedFile']).first()
                # if cur_edit.editor1 != None and cur_edit.editor2 != None and cur_edit.editor3 != None:
                #     context['edit_alert_display'] = 'd-block'
                #     return render(request, 'accounts/index.html', context)
            else:
                cur_edit = Docitems.objects.get(id=edit_record_row)
                print('cccccccccccccur-edit is:  ', cur_edit)
            context['cur_edit'] = cur_edit
            context['process_submit_display'] = ""
        if 'previous' in request.POST:
            cur_edit = Docitems.objects.get(id=int(request.POST['docitemid'])-1)
            context['cur_edit'] = cur_edit
            context['process_submit_display'] = ""
            editRecord.objects.filter(editor=request.user, file=request.session['selectedDocID']).update(last_edit_row=int(request.POST['docitemid'])-1)
        if 'next' in request.POST:
            nextrow = int(request.POST['docitemid'])+1
            cur_edit = Docitems.objects.get(id=nextrow)
            context['cur_edit'] = cur_edit
            context['process_submit_display'] = ""
            editRecord.objects.filter(editor=request.user, file=request.session['selectedDocID']).update(last_edit_row=nextrow)
        if any(x in request.POST for x in ['negative', 'flat', 'positive']):
            print('docitems id is:  ', request.POST['docitemid'])
            print('session is :  ', request.session['selectedDocID'])
            if 'negative' in request.POST:
                value = -1
            if 'flat' in request.POST:
                value = 0
            if 'positive' in request.POST:
                value = 1
            if Docitems.objects.get(id=request.POST['docitemid']).editor1 == (None or request.user.username):
                cur_edit = Docitems.objects.filter(id=request.POST['docitemid'], editor1=(None or request.user.username)).update(editor1=request.user.username, label1=value)
            elif Docitems.objects.get(id=request.POST['docitemid']).editor2 == (None or request.user.username):
                cur_edit = Docitems.objects.filter(id=request.POST['docitemid'], editor2=(None or request.user.username)).update(editor2=request.user.username, label2=value)
            elif Docitems.objects.get(id=request.POST['docitemid']).editor3 == (None or request.user.username):
                cur_edit = Docitems.objects.filter(id=request.POST['docitemid'], editor3=(None or request.user.username)).update(editor3=request.user.username, label3=value)
            cur_edit = Docitems.objects.get(id=int(request.POST['docitemid'])+1)
            context['cur_edit'] = cur_edit
            context['process_submit_display'] = ""
            editRecord.objects.filter(editor=request.user, file=request.session['selectedDocID']).update(last_edit_row=int(request.POST['docitemid'])+1)
    return render(request, 'accounts/index.html', context)

def analyse(request):
    context = {
        "documents": Document.objects.all(),
        'process_submit_display': 'd-none',
        'process_alert': ''
    }
    # context['analyzedText'] = sentence_analyse(request.POST['analyzeText'])
    # context['analyzedText'] = sentence_analyse('hello world, let"s talk about others')
    # return JsonResponse(request, context)
    if request.method == 'POST':
        # context['analyzedText'] = test('hello world, let"s talk about others')
        context['analyzedText'] = 'hello world, let"s talk about others'

    return render(request, 'accounts/index.html', context)
