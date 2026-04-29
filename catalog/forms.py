"""
Формы для приложения catalog.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

import os

# Список запрещённых слов (в любом регистре)
FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта",
    "биржа", "дешево", "бесплатно",
    "обман", "полиция", "радар",
]

# Допустимые форматы изображений
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 МБ


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название продукта"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Описание продукта"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Цена"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Добавляем стили к полям."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        """Валидация названия на запрещённые слова."""
        name = self.cleaned_data.get("name", "")
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f'Название содержит запрещённое слово: "{word}".')
        return name

    def clean_description(self):
        """Валидация описания на запрещённые слова."""
        description = self.cleaned_data.get("description", "")
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f'Описание содержит запрещённое слово: "{word}".')
        return description

    def clean_price(self):
        """Проверка, что цена не отрицательная."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        """Валидация изображения: формат JPEG/PNG, размер до 5 МБ."""
        image = self.cleaned_data.get("image")
        if image:
            # Проверка расширения
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError(f"Недопустимый формат файла. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}")
            # Проверка размера
            if image.size > MAX_FILE_SIZE:
                raise ValidationError(f"Размер файла превышает 5 МБ. Текущий размер: {image.size // 1024 // 1024} МБ")
        return image
