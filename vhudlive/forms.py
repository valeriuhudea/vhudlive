from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return User

'''class StorageOwnerForm(forms.ModelForm):
    class Meta:
        model = StorageOwner
        fields = ['storage_name', 'storage_type'] 
    def save(self, *args, **kwargs):
        _choices_list = kwargs.pop('_choices', None)
        super(StorageOwnerForm, self).save(*args, **kwargs)
        if _choices_list is not None:
            # this only works if 'ownership_type' is a CharField... and it will be your error
            self.fields['storage_type'].choices = _choices_list  # I don't remeber if the attribute is 'choice' or 'choices'
            # if 'ownership_type' is a RelationField, you must set queryset and not a list of strings
        #self.fields['storage_name'].widget.attrs.update({'size': '7'})'''

class StorageForm(forms.ModelForm):
     storage_name = forms.CharField(required=True)
     class Meta:
         model = Storage
         fields = ['name', 'type', 'active']   
     def __init__(self, *args, **kwargs):
           self.request = kwargs.pop('request', None)
           return super(StorageForm, self).__init__(*args, **kwargs)
     def save(self, *args, **kwargs):
           kwargs['commit']=False
           obj = super(StorageForm, self).save(*args, **kwargs)
           if self.request:
              obj.user = self.request.user
           obj.save()
           return obj
