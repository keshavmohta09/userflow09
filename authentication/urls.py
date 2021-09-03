from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('sign-up/',views.register,name='register'),
    path('sign-in/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('user-details/',views.details,name='user-details'),
    path('delete-user/',views.delete_user,name='delete-user'),
    path('update-details/',views.update_details,name='update-details'),
]
# urlpatterns = []