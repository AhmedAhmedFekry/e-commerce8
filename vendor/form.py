from django.forms import ModelForm

from product.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'title_en', 'title_ar', 'description_en',
            'description_ar', 'image', 'price', 'variant', 'amount'
        ]
