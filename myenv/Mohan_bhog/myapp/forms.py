from django import forms

from .models import ContactMessage,WebsiteUser

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
class PaymentForm(forms.Form):
    product_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    quantity = forms.IntegerField(min_value=1, required=True)
    
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    
    phone = forms.CharField(max_length=15, label="Phone / WhatsApp Number")
    email = forms.EmailField()
    
    address = forms.CharField(widget=forms.Textarea)
    
    payment_mode = forms.ChoiceField(
        choices=[('cod', 'Cash on Delivery'), ('qr', 'QR Code')],
        widget=forms.RadioSelect
    )
    
    payment_screenshot = forms.ImageField(required=False)

class SignupForm(forms.ModelForm):
    class Meta:
        model = WebsiteUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
