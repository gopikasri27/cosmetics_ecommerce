from django import forms


class CheckoutForm(forms.Form):

    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Full Name",
            "id": "id_full_name",
            "autocomplete": "name",
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email Address",
            "id": "id_email",
            "autocomplete": "email",
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "placeholder": "Mobile Number",
            "id": "id_phone",
            "autocomplete": "tel",
            "pattern": "[0-9+\\-\\s]{6,15}",
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "House No, Street, Area",
            "rows": 3,
            "id": "id_address",
            "autocomplete": "street-address",
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "City",
            "id": "id_city",
            "autocomplete": "address-level2",
        })
    )

    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "State",
            "id": "id_state",
            "autocomplete": "address-level1",
        })
    )

    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "placeholder": "PIN Code",
            "id": "id_pincode",
            "autocomplete": "postal-code",
            "pattern": "[0-9]{6}",
        })
    )

    payment_method = forms.ChoiceField(
        choices=[
            ("COD", "Cash on Delivery"),
            ("UPI", "UPI"),
            ("CARD", "Credit / Debit Card"),
        ],
        widget=forms.RadioSelect
    )

    coupon = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter coupon code",
            "id": "id_coupon",
            "autocomplete": "off",
            "style": "text-transform:uppercase;",
        })
    )