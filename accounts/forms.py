from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Myuser,Userprofile


class RegisterForm(forms.ModelForm):
    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder':'Password'}
        )
    )
    confirm_password=forms.charField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'Confirm Password'}
        )
    )
    class Meta:
        model= Myuser
        fields=['first_name','last_name','email','phone']

    def __init__(self, *args, **kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'placeholder':'First Name'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'placeholder':'Last Name'}
        )
        self.fields['email'].widget.attrs.update(
            {'placeholder':'Email'}
        )
        self.fields['phone'].widget.attrs.update(
            {'placeholder':'Phone'}
        )
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class':'form-control'}
            )
    def clean(self):
        cleaned_data=super(RegisterForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if confirm_password != password:
            raise forms.ValidationError(
                "passwords doesnot match"
            )
        
class UserProfileForm(forms.ModelForm):
    profile_image= forms.ImageField(required=False,error_messages={'invalid':{
        "image files only"
    }},widget=forms.FileInput)

    class Meta:
        model =Userprofile
        fields=['address_line_1','address_line_2','ptofile_image','city','state','country']

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class':'form-control'}
            )


class UserForm(forms.ModelForm):

    class Meta:
        model= Myuser
        fields=['first_name','last_name','phone']

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class':'form-control'}
            )