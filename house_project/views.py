from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpRequest
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt


from .models import House, User, House_image

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

@login_required(login_url="user_login")
def index(request):
    houses = House.objects.all()
    house_images = House_image.objects.all()

    return render(request, 'index.html', {'houses': houses, 'house_images': house_images})



def user_registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure username is not empty
        if not username:
            return render(request, "user_registration.html", {
                "message": "Username must not be empty."
            })
        
        if not email:
            return render(request, "user_registration.html", {
                "message": "Email must not be empty."
            })

        
        checkbox_value = request.POST.get("checkbox", False)
        # Convert the value to a boolean
        checkbox_value = True if checkbox_value == "on" else False

        # Ensure password matches confirmation
        password = request.POST["password"]
        if not password:
            return render(request, "user_registration.html", {
                "message": "Password must not be empty."
            })
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user_registration.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, is_House_owner=checkbox_value)
        except IntegrityError:
            return render(request, "user_registration.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "user_registration.html")
    

def user_login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user_login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "user_login.html")


@login_required(login_url="user_login")
def user_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("welcome"))


    
@login_required(login_url="user_login")
def house_registration(request):
    if request.method == "POST":
        data = request.POST
        if not data.get('name') and not data.get('address') and not data.get('city') and not data.get('state') and not data.get('country') and not data.get('description') and not data.get('rent') and not request.FILES.getlist('images'):
            message = 'All fields are required'
            return render(request, 'house_registration.html', {'message': message})
        else:

            if len(request.FILES.getlist('images')) == 0:
                return render(request, 'house_registration.html', {'message': 'Please upload at least one image'})
            else:
                name = data.get('name')
                address = data.get('address')
                city = data.get('city')
                state = data.get('state')
                country = data.get('country')
                description = data.get('description')
                house_host = User.objects.get(username=request.user)
                rent = data.get('rent')
                images = request.FILES.getlist('images')

                house = House.objects.create(
                    name=name,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    description=description,
                    house_host=house_host,
                    rent=rent
                )
                for image in images:
                    House_image.objects.create(
                        house=house,
                        image=image
                    )
                if not request.user.is_House_owner:
                    request.user.is_House_owner = True
                    request.user.save()

                return HttpResponseRedirect(reverse("index"))
                
    return render(request, 'house_registration.html')


@login_required(login_url="user_login")
def house(request, id):

    houses = House.objects.get(id=id)
    images = House_image.objects.filter(house=houses)
    return render(request, "house.html", {"house": houses, "images": images})

@login_required(login_url="user_login")
def edit_house(request, id):
    message = None
    if request.method == "POST":
        data = request.POST

        if not data.get('name') and not data.get('address') and not data.get('city') and not data.get('state') and not data.get('country') and not data.get('description') and not data.get('rent') and not request.FILES.getlist('images'):
            message = 'All fields are required'
            return render(request, 'house_registration.html', {'message': message})
        else:

            if len(request.FILES.getlist('images')) == 0:
                return render(request, 'house_registration.html', {'message': 'Please upload at least one image'})
            else:
                name = data.get('name')
                address = data.get('address')
                city = data.get('city')
                state = data.get('state')
                country = data.get('country')
                description = data.get('description')
                house_host = User.objects.get(username=request.user)
                rent = data.get('rent')
                images = request.FILES.getlist('images')

                house = House.objects.get(id=id)
                house.name = name
                house.address = address
                house.city = city
                house.state = state
                house.country = country
                house.description = description
                house.house_host = house_host
                house.rent = rent
                house.save()

                for image in images:
                    House_image.objects.create(
                        house=house,
                        image=image
                    )
                return render(request, 'index.html')
                

    house = House.objects.get(id=id)
   
    return render(request, "edit_house.html", {"house": house})


@login_required(login_url="user_login")
def rent_house(request, id):
    
    house = House.objects.get(id=id)
    
    try:
        if house.is_rented == True:
            house.is_rented = False
            house.guest = None
            house.save()
            return HttpResponseRedirect(reverse("house", args=(id,)))
        else:
            house.is_rented = True
            house.guest = request.user
            house.save()
            return HttpResponseRedirect(reverse("house", args=(id,)))
    except Exception as e:
        return HttpResponseRedirect(reverse("house", args=(id,)))
        
        