from datetime import timedelta
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from .models import User
from profiles.models import Profile
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect("user-details")
    else:
        return redirect("login")

def register(request):
    data = request.POST
    if data:
        name = data.get('name').strip()
        email = data.get('email').strip()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        address = data.get('address').strip()
        if not all([name,email,address]):
            return HttpResponse("<h3>All fields are required.</h3>")
        if password!=confirm_password:
            return render(request, 'register.html', {'pass_validation':'Password does not match.'})
        
        if User.objects.filter(Q(username=email)|Q(email=email)).exists():
            return render(request, 'register.html', {'email_validation':'Username or Email id already exist.'})

        first_name = name.split(" ",1)[0]
        last_name = None
        try:
            last_name = name.split(" ",1)[1]
        except IndexError:
            pass
        success , user = User.objects.create_user(email=email,username=email,password=password,first_name=first_name,last_name=last_name)
        if success:
            Profile.objects.create(user=user,address=address)
        else:
            return HttpResponse('<h3>{user}</h3>'.format(user=user))
        
        return redirect("login")
    return render(request,'register.html')

def login(request):
    data = request.POST
    if data:
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            request.session['HTTP_AUTHORIZATION'] =  user.token
            return redirect('user-details')
        else:
            return render(request,'login.html',{'login_validation':'Incorrect username or password.'})
    else:
        return render(request,'login.html')
    
@login_required(login_url="login")
def details(request):
    try:
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        name = first_name+' '+last_name
        profile = user.profile
        return render(request,'details.html',{'address':profile.address,'name':name})
    except:
        return render(request,'details.html')
    
       
def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url="login")
def delete_user(request):
    try:
        user_id = request.user.id
        user = User.objects.get(email=request.user.email)
        user.delete()
        detail = Profile.objects.get(user=user_id)
        detail.delete()
    except:
        pass
    return redirect("login")

@login_required(login_url="login")
def update_details(request):
    user = request.user
    if request.POST:
        data = request.POST
        name = data.get('name').strip()
        email = data.get('email').strip()
        address = data.get('address').strip()
        if name=='' or email=='' or address=='':
            return HttpResponse("<h3>All fields are required.</h3>")
        user = User.objects.get(email=request.user.email)
        user.email = email
        split_name = name.split(' ',1)
        user.first_name = split_name[0]
        if len(split_name)>1:
            user.last_name = split_name[1]
        else:
            user.last_name = ''
        profile =user.profile
        profile.address = address
        profile.save()
        user.save()
        return redirect("user-details")
    name = user.first_name + ' ' + user.last_name
    email = user.email
    password = user.password
    address = Profile.objects.get(user=user.id).address
    return render(request,'update_details.html',{'name':name,'email':email,'password':password,'address':address})