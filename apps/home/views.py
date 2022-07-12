
from distutils.command.upload import upload
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import fileupload
from apps.home.backend import *
import time
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect


# Messages

uploadDoneMessage = {}

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def transfer(request):

    if request.method == 'POST':
        name = request.POST.get("RecieverName")
        phone = request.POST.get("Phone")
        email = request.POST.get("email")
        secretpass = request.POST.get("SecretPassword")
        message = request.POST.get("message")
        filepath = request.FILES["UploadFile"]
        fileobj = fileupload(name=name, phone=phone, email=email, password=secretpass,message=message,filepath=filepath)
        # send_email(email, name)
        fileobj.save()
        print("This is My Password", fileobj.password)
        encryptFile(str(fileobj.filepath), secretpass)
        global uploadDoneMessage
        uploadDoneMessage = {"name" : name, "phone": phone, "email":email}
        return redirect("/upload-done")

    context = {'segment': 'tranfer'}

    html_template = loader.get_template('home/file-transfer.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def get_file(request, id):
    # print("This is My Id", id)
    file_obj = get_object_or_404(fileupload, pk=id)
    print("File Object: ", file_obj)

    print("This is my Phone No.: ",file_obj.phone)
    print("This is File Path: ",file_obj.filepath)
    
    decryptFile(str(file_obj.filepath), file_obj.password)
    return render(request,'home/get_file.html') 


@login_required(login_url="/login/")
def upload_done(request):
    global uploadDoneMessage
    if(uploadDoneMessage == {}):
        return redirect("/file-transfer")

    html_template = loader.get_template('home/page-404.html')
    context = uploadDoneMessage
    uploadDoneMessage = {}
    return HttpResponse(html_template.render(context, request))
    





@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
