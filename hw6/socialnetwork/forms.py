from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from socialnetwork.models import Profile, Post

class EntryForm(forms.Form) :
    new_post = forms.CharField(max_length=2000, 
                               label='New Post')

class LoginForm(forms.Form) :
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        # Confirms that the two password fields match
        if not user:
            raise forms.ValidationError("Invalid username/password")
        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegisterForm(forms.Form):
    username   = forms.CharField(max_length = 20,
                                 label='Username')
    password  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                 label='Confirm',  
                                 widget = forms.PasswordInput())
    email      = forms.CharField(max_length=50,
                                 label='E-mail',
                                 widget = forms.EmailInput())
    first_name = forms.CharField(max_length=20,
                                 label='First Name')
    last_name  = forms.CharField(max_length=20,
                                 label='Last Name')

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


MAX_UPLOAD_SIZE = 2500000

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'picture', 'user_bio' )
        widgets = {
            'user_bio': forms.Textarea(attrs={'id':'id_bio_input_text', 'rows':'3'}),
            'picture': forms.FileInput(attrs={'id':'id_profile_picture'})
        }
        label = {
            'user_bio': "",
            'picture': "Upload Image"
        }
    
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'text', )
        exclude = ( 'date_time', 'user')
        widgets = {
            'text': forms.Textarea(attrs={'id':'id_post_input_text', 'rows':'4'}),
        }
