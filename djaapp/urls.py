from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view-book/', views.view_book, name='view_book'),
    path('add-book/', views.add_book, name='add_book'),
    path('upd_book/<int:id>', views.updaet_book, name='updaet_book'),
    path('del_book/<int:id>', views.delete_book, name='delete_book'),
    path('reg-user/', views.reg_user, name='reg_user'),
    path('login-user/', views.login_user, name='login_user'),
    path('logout-user/', views.logout_user, name='logout_user'),
    path('add-to-cart/<int:book_id>', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:book_id>', views.remove_from_cart, name='remove_from_cart'),

    path('buy/<int:book_id>/', views.buy_now, name='buy_now'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),



]