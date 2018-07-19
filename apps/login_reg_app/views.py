from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'login_reg_app/index.html')

def register(request):
    # validate our input through modelmanager
    result = User.objects.validate_registration(request.POST)
    if len(result) > 0:
        for key in result.keys():
            print(result[key])
            messages.error(request, result[key])
        return redirect('/')
    else:
        # If valid, bcrypt must hash the password
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hashed_pw)
        user = User.objects.create(name = request.POST['name'], password = hashed_pw, email = request.POST['email'])
        # after creating a new user, automatically log them in
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        print(dict(request.session))
        return redirect('/success')
    

def login(request):
    return render(request, 'login_reg_app/login_form.html')

def process_login(request):
    # validate login through views.py
    # 1. search for a user with the email entered
    user = User.objects.filter(email = request.POST['email'])
    if len(user) == 0:
        messages.error(request, 'No user with that email exists')
        return redirect('/login')
    else:
        user = user.first() # or user = user[0]
    # 2. Check the passwords using bcrypt
    password_valid = bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())
    if password_valid:
        # add them to session
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        return redirect('/success')
    else:
        messages.error(request, 'Invalid information, please try again')
        return redirect('/login')



def success(request):
    # in order to show detailed logged in user information
    the_user = User.objects.get(id = request.session['user_id'])
    all_products = Product.objects.annotate(total_purchases = Sum('purchased_product__quantity'))
    context = {
        'user': the_user,
        'products': all_products
    }
    return render(request, 'login_reg_app/success.html', context)

def buy_product(request, product_id):
    # we need:
    # the product we are purchasing
    the_product = Product.objects.get(id=product_id)
    # the current logged in user
    the_user = User.objects.get(id=request.session['user_id'])
    Purchase.objects.create(
        product = the_product,
        buyer = the_user,
        quantity = int(request.POST['quantity'])
    )
    
    print(Purchase.objects.all().values())
    return redirect('/checkout')

def checkout(request):
    my_purchases = Purchase.objects.filter(buyer = User.objects.get(id=request.session['user_id']))
    my_sum = 0
    my_items_bought = 0
    for purchase in my_purchases.all():
        my_sum += purchase.product.price * purchase.quantity
        my_items_bought += purchase.quantity
    context = {
        'total_spent': my_sum,
        'total_items': my_items_bought
    }
    return render(request, 'login_reg_app/checkout.html', context)