from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Order
from .forms import BookForm, CustomUserCreationForm, loginform
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(requst):
    return render(requst, 'home.html')

@login_required
def view_book(request):
    books=Book.objects.all()
    return render(request, 'book.html', {'book':books})

@login_required
def add_book(request):
    book=BookForm(request.POST or None, request.FILES or None)
    if book.is_valid():
        book.save()
        return redirect('view_book')
    return render(request, 'add_book.html', {'book':book})


@login_required
def updaet_book(request, id):
    book=Book.objects.get(id=id)
    book=BookForm(request.POST or None, request.FILES or None, instance=book)
    if book.is_valid():
        book.save()
        return redirect('view_book')
    return render(request, 'add_book.html', {'book':book})

@login_required
def delete_book(request, id):
    book=Book.objects.get(id=id)
    if request.method=='POST':
        book.delete()
        return redirect('view_book')
    return render(request, 'confirm_delete.html', {'book':book})


def reg_user(request):
    form=CustomUserCreationForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save()
        return redirect('login_user')
    return render(request, 'reg_user.html', {'form':form})


def login_user(request):
    form=loginform(request, data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.get_user()
        login(request, user)
        return redirect('view_book')
    return render(request, 'login.html', {'form':form})

def logout_user(request):
    logout(request)
    return redirect('login_user')

def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item, created = Order.objects.get_or_create(book=book, user=request.user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    cart_items = Order.objects.filter(user=request.user)
    totel_price = 0
    for item in cart_items:
        totel_price += item.book.price * item.quantity
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'totel_price': totel_price})

def remove_from_cart(request, book_id):
    book=Book.objects.get(id=book_id)
    cart_item=Order.objects.get(book=book, user=request.user)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

def buy_now(request, book_id):
    cart_items = Order.objects.filter(user=request.user, book_id=book_id)
    if not cart_items.exists():
        return redirect('view_cart')
    book=get_object_or_404(Book, id=book_id)

    total_quantity = sum(item.quantity for item in cart_items)

    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'inr',
                    'product_data':{
                        'name':book.name,
                    },
                    'unit_amount': int(float(book.price) * 100),

                },
                'quantity':total_quantity,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    return redirect(session.url)    

def payment_success(request):
    return render(request, 'success.html')

def payment_cancel(request):
    return render(request, 'cancel.html')