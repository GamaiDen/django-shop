from django import forms
from django.core.exceptions import ValidationError
from .models import Product
import os

FORBIDDEN_WORDS = ["казино","криптовалюта","крипта","биржа","дешево","бесплатно","обман","полиция","радар"]
ALLOWED_EXTENSIONS = ['.jpg','.jpeg','.png']
MAX_FILE_SIZE = 5*1024*1024

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","description","image","category","price"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control","placeholder":"Название"}),
            "description": forms.Textarea(attrs={"class":"form-control","rows":4,"placeholder":"Описание"}),
            "category": forms.Select(attrs={"class":"form-control"}),
            "price": forms.NumberInput(attrs={"class":"form-control","placeholder":"Цена"}),
            "image": forms.ClearableFileInput(attrs={"class":"form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
    def clean_name(self):
        name = self.cleaned_data.get("name","")
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f'Название содержит запрещённое слово: "{word}".')
        return name
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price
