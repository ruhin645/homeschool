import datetime
from django import forms
from .models import Course

class add_course(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_id', 'course_sec', 'classroom_id')

class JoinClass(forms.ModelForm):
    code = forms.CharField(max_length=10,label='code')


class CreateAssignmentForm(forms.Form):
    title = forms.CharField(max_length=50,label='title')
    due_date = forms.DateField(initial=datetime.date.today(),label='Due Date')
    due_time = forms.TimeField(label='Due Time')
    instructions = forms.CharField(label='Instructions',widget=forms.Textarea)
    total_marks = forms.IntegerField(label='Total Marks')

class SubmitAssignmentForm(forms.Form):
    submission_file = forms.FileField()

class PostForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

class CommentCreateForm(forms.Form):
    comment_text = forms.CharField(max_length=250)
# class TodoForm(forms.ModelForm):
#     class Meta:
#         model = Todo
#         fields = ('title', 'is_done')