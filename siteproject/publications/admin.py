from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin


from .models import Publication


class PublicationAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Publication
        fields = "__all__"


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    form = PublicationAdminForm
