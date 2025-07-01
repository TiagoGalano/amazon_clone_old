from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Create Account', css_class='btn btn-primary btn-block')
        )

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='btn btn-primary btn-block')
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'country']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # Remove the Submit button from the form helper since we'll add it manually in the template
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            'phone',
            'address',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('zipcode', css_class='form-group col-md-6 mb-0'),
                Column('country', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

# Checkout form example (you'll need to create this based on your Order model)
class CheckoutForm(forms.Form):
    # Billing Information
    billing_name = forms.CharField(max_length=100, required=True)
    billing_email = forms.EmailField(required=True)
    billing_phone = forms.CharField(max_length=20, required=True)
    billing_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    billing_city = forms.CharField(max_length=100, required=True)
    billing_state = forms.CharField(max_length=100, required=True)
    billing_zipcode = forms.CharField(max_length=20, required=True)
    billing_country = forms.CharField(max_length=100, required=True)
    
    # Shipping Information
    same_as_billing = forms.BooleanField(required=False, initial=True, label="Shipping address is the same as billing")
    shipping_name = forms.CharField(max_length=100, required=False)
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    shipping_city = forms.CharField(max_length=100, required=False)
    shipping_state = forms.CharField(max_length=100, required=False)
    shipping_zipcode = forms.CharField(max_length=20, required=False)
    shipping_country = forms.CharField(max_length=100, required=False)
    
    # Payment Information
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            # Billing Information Section
            '<h5><i class="fas fa-credit-card"></i> Billing Information</h5>',
            Row(
                Column('billing_name', css_class='form-group col-md-6 mb-0'),
                Column('billing_email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'billing_phone',
            'billing_address',
            Row(
                Column('billing_city', css_class='form-group col-md-6 mb-0'),
                Column('billing_state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('billing_zipcode', css_class='form-group col-md-6 mb-0'),
                Column('billing_country', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            # Shipping Information Section
            '<hr><h5><i class="fas fa-shipping-fast"></i> Shipping Information</h5>',
            'same_as_billing',
            Row(
                Column('shipping_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'shipping_address',
            Row(
                Column('shipping_city', css_class='form-group col-md-6 mb-0'),
                Column('shipping_state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('shipping_zipcode', css_class='form-group col-md-6 mb-0'),
                Column('shipping_country', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            # Payment Information Section
            '<hr><h5><i class="fas fa-payment"></i> Payment Method</h5>',
            'payment_method',
        )