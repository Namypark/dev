from django.forms import ModelForm
from django import forms
from .models import Project, Review


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
        #can set the classes one at a time or just use a for loop
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"input"})

        

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        
        labels = {
            'value':'Place your vote',
            'body' : 'Add a comment with your vote'
        }
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        #* loops through the  fields and adds a class of input to them.
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        