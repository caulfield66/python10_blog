from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        exclude = ('slug', 'author')


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    # def get_form(self, request, *args, **kwargs):
    #     form = super().get_form(request, *args, **kwargs)
    #     form.request = request
    #     return form

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)


