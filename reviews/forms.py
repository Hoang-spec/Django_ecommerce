from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': '1', 'max': '5'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=True,
        min_length=10,
        max_length=1000
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Đánh giá phải từ 1 đến 5 sao')
        return rating
