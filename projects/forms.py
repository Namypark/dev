from django.forms import ModelForm
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "featured_image", "description", "demo_link", "source_link", "tags"]
        #* this is one way to customize the classes
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        #inherits the form(telling it the class we are modifying)
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"input"})

        