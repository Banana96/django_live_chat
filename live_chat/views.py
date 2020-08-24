from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import generic

from live_chat.models import Room


class IndexView(generic.TemplateView):
    template_name = "home.html"


class RegisterView(generic.FormView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class RoomView(generic.DetailView):
    template_name = "room.html"
    queryset = Room.objects.all()
    pk_url_kwarg = "room_id"
