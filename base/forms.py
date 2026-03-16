from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']
        # for remove the host and participants from all
    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']