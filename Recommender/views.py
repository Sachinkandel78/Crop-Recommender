from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# yo line le django ko built-in authentication system ko functions haru import garcha, jasle user authentication, login, logout, etc. ka functionalities provide garcha.
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render(request, "Home.html")
# This function defines a view called home that takes an HTTP request as an argument and renders the 'Home.html' template. When a user visits the home page of the website, this view will be called, and it will return the rendered HTML content of the 'Home.html' template to be displayed in the user's browser.
# yesley k garda cha vaney user le home page ma janey bela Home.html template dekhaune ho.                
def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
# basic form data haru lai POST request bata get garcha, jasle user le signup form ma bhareko data lai retrieve garcha.
        if not name or not phone or not email or not password:
            messages.error(request, "Please fill all required fields.")
 # yedi user ley name phone email rw password kei fill gareyxaina vaney yo msg dekhauxa
            return redirect("signup")

        if len(password) < 8:
            messages.error(request, "Password must contain 8 characters")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Account already exist with same email id")
            return redirect("signup")
        user = User.objects.create_user(username=email,password=password)
        #To insert data in user model
        if " " in name:
            first, last = name.split(" ",1)  #1-> represent name lai ekchoti split gariyo. manam lokesh kannaur Rahul thyo vaney lokesh kannaurRahul jastai vayo kya hai.
        else:
            first, last = name, ""
        user.first_name, user.last_name = first, last
        user.save()
#user=email,password save gariyo.Ani tala UserProfile model jun models.py ma xa tesma lagera add gariyo
        UserProfile.objects.create(user=user,Phone=phone)
        login(request,user)
        messages.success(request, "Account created successfully. Welcome!")
        return redirect("predict")
    #Signup successfull vayesi redirect to predict page malab predict wala page khulxa


    return render(request, "signup.html")
 # This function defines a view called signup_view that takes an HTTP request as an argument and renders the 'signup.html' template. When a user visits the signup page of the website, this view will be called, and it will return the rendered HTML content of the 'signup.html' template to be displayed in the user's browser.

 #Prediction Page url opening 

from .ML.Loader import predict_one, load_bundle
from django.contrib.auth.decorators import login_required

@login_required
def predict_view(request):
    feature_order = load_bundle()["Features_cols"]
    result = None
    last_data = None

    if request.method == "POST":
        data = {}
        try:
            for c in feature_order:
                data[c] = float(request.POST.get(c))   
        except ValueError:
            messages.error(request,"PLease enter valid numeric values")
            return redirect ("predict")
        label = predict_one(data)
        
        Prediction.objects.create(user=request.user,**data,predicted_label=label)
        result = label
        last_data = data
        messages.success(request,f"Recommended Crop:{label}")
        #data-> keywords_arguments unpacking
    return render(request, "predict.html",locals())


def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect("login")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        #Receive data from user using post method . POST — when a user sends/submits data to the server.
        #GET = when the user requests/receives data from the server — no data is being sent.

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request,"Invalid login Credentials")
            return redirect("login")
        login(request,user)
        messages.success(request, "Logged in Successfully. Welcome!")
        return redirect("predict")
    return render(request, "login.html")




@login_required
def user_history_view(request):
    predictions = Prediction.objects.filter(user=request.user)   
    return render(request, "history.html",locals())


from django.shortcuts import get_object_or_404
@login_required
def user_delete_prediction(request,id):
    prediction = get_object_or_404(Prediction, id=id, user=request.user) #Prediction model bata data chaeeyo jasma datako id ani userko name  match hunaparyo
    prediction.delete()
    messages.success(request,"Entry Removed from history")
    return redirect("user_history")

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":  #Naya name rw number liyiyo matlab purano user ley afno name rw number change hanyo tyo data post method ko through get gariyo name rw phone variables ma 
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        # yo "phone","name" kata bata aayeko vanda profile.html page vitrako full name rw phone number section ko name="name" rw name="phone" bata aayeko ho
        if name:
            parts = name.split(" ",1)
            request.user.first_name = parts[0]
            request.user.last_name = parts[1] if len(parts) > 1 else ""
            profile.Phone = phone 
            request.user.save()  # request.user means UserProfile model vitrako user
            profile.save()    #Profile variable vitra pailai ko purano name rw phone number ko data leyko thiyem aba vaney user ley change gareyko naya data lagera save gardiyem
            messages.success(request,"Profile updated.")
    full_name = request.user.get_full_name()
    return render(request, "profile.html",locals())


