from django import forms

PRODUCT_QUANTITY_CHOICES = [
    (i, str(i)) for i in range(1, 21)
]


class CartAddProductForm(forms.Form):
    """
        TypedChoiceField
            1. field for selecting
            2. the 'coerce' is for conv the 'str(i)' to int :D

        BooleanField (update)
            I'll leave it our own (not display to users)

            True    #NOTE this one is related to 'cart/cart.py/Cart/add'
            False   #TODO notes needed (p420)
    """

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
