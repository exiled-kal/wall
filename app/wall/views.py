from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Comment, Message
import bcrypt


def index(request):
    return render(request, "wall/index.html")


def create(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect("/")
    elif request.method == "POST":
        new_user = User.objects.create(fname=request.POST['fname'],
                                        lname=request.POST['lname'],
                                        email=request.POST['email'],
                                        pw=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode())
        request.session['id'] = new_user.id
        return redirect("/show")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect("/")
    elif request.method == "POST":
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        return redirect("/show")


def show(request):
    if 'id' in request.session:
        messages = Message.objects.all().order_by('-id')
        comments = Comments.objects.all()
        thi_user = User.objects.get(id=request.session['id'])
        context = {
            'messages': messages,
            'comments': comments,
            'user': this_user
        }
        return render(request, "wall/wall.html", context)
    else:
        return redirect('/')


def message(request):
    Message.objects.create(user=User.objects.get(id=request.session['id']), content=request.POST['content'])
    return redirect('/show')

def comment(request):
    Comment.objects.create(message=Message.objects.get(id=request.POST['messageid']), user=User.objects.get(id=request.session['id']), content=request.POST['content'])
    return redirect('/')


def destroy(request):
    del request.session['id']
    return redirect['/']
