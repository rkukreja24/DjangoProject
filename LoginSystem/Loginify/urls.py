from django.urls import path,include
from . import views

urlpatterns = [
    path('print-h/',views.print_hello, name="print-hello" ),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('get_all_users/', views.get_all_users, name="get_all_users"),
    path('one_user/<str:email>', views.one_user, name="one_user"),
    path('update_user/<str:email>', views.update_user, name="update_user"),
    path('delete_user/<str:email>', views.delete_user, name="delete_user"),
]