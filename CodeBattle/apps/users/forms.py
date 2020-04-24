from allauth.account.forms import SignupForm
from allauth.account.forms import forms

class MyCustomSignUpForm(SignupForm):

    # name = forms.CharField(required=True)
    # sirname = forms.CharField(required=True)
    # phone = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        super(MyCustomSignUpForm, self).__init__(*args, **kwargs)
    
        self.fields['name'] = forms.CharField(required=True,label=None)
        self.fields['sirname'] = forms.CharField(required=True,label=None)
        self.fields['phone'] = forms.CharField(required=True,label=None)
        # for fieldname, field in self.fields.items():
        #     field.widget.attrs.update({
        #         'class': 'form--input'
        # })

    def save(self, request):
        user = super(MyCustomSignUpForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.sirname = self.cleaned_data['sirname']
        user.phone = self.cleaned_data['phone']
        user.save()
        
        return user