from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
     
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     del self.fields['password2']