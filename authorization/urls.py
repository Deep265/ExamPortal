from django.urls import path
from . import views
app_name='authorization'

urlpatterns = [
    path('signup/',views.SignUp,name='signup'),
    path('login/',views.LoginUser,name='login'),
    path('logout/',views.LogoutUser,name='logout'),
    path('test/student/',views.student_register,name='student'),
]