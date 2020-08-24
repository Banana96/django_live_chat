from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth

from . import views

urlpatterns = [
    path("", include([
        path("", login_required(views.IndexView.as_view()), name="home"),
        path("room/<int:room_id>/", login_required(views.RoomView.as_view()), name="room"),
    ])),

    path("auth/", include([
        path("login/", auth.LoginView.as_view(template_name="login.html"), name="login"),
        path("logout/", auth.LogoutView.as_view(next_page="/"), name="logout"),
        path("register/", views.RegisterView.as_view(), name="register"),
    ])),
]
