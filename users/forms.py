from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User

from catalog.forms import CustomFormMixin, MyCleanForm


class UserRegisterForm(CustomFormMixin, MyCleanForm, UserCreationForm):
    # Наследуемся от специальной формы UserCreationForm из модуля auth
    class Meta:
        model = User
        # Указываем новую кастомную модель
        fields = ('email', 'password1', 'password2')
        # Меняем поля, так как исходная форма UserCreationForm
        # ссылается на поле username


class UserProfileForm(CustomFormMixin, MyCleanForm, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone_number',
                  'country', 'first_name', 'last_name'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


