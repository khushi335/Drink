from django.urls import path
from .views import index,about,contact,log_in,register,log_out,change_password,location
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",index,name="index"),
    path("about/",about,name="about"),
    path("contact/",contact,name="contact"),
    path("location/",location,name="location"),
    
    ##auth part
    path("log_in/",log_in,name="log_in"),
    path("register/",register,name="register"),
    path("log_out/",log_out,name="log_out"),
    path("change_password/",change_password,name="change_password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"), name='password_reset_complete'),

]