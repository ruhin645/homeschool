
from django.utils import timezone
from tkinter import CASCADE
from xmlrpc.client import DateTime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here
from django.template.defaultfilters import slugify
from jazzmin.templatetags.jazzmin import User


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_id = models.CharField(max_length=10)
    course_sec = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(25)])
    classroom_id = models.CharField(max_length=50,unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    slug=models.SlugField(null=True, blank=True)
    

    def __str__(self):
        return self.course_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.classroom_id)
        super().save(*args, **kwargs)

    def is_valid(self):
        pass




class StudentsByClassroom(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    classroom = models.ForeignKey("Course",on_delete=models.CASCADE)


class TeachersByClassroom(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE)
    classroom = models.ForeignKey("Course",on_delete=models.CASCADE)

class Assignments(models.Model):
    title=models.CharField(max_length=50)
    classroom_id=models.ForeignKey(Course,on_delete=models.CASCADE)
    due_date=models.DateField()
    due_time=models.TimeField()
    posted_date=models.DateField(auto_now_add=True)
    instructions=models.TextField()
    total_marks=models.IntegerField(default=100)
    
    def __str__(self):
        return self.title 

class Submissions(models.Model):
    assignment_id=models.ForeignKey(Assignments,on_delete=models.CASCADE)
    student_id=models.ForeignKey(StudentsByClassroom,on_delete=models.CASCADE)
    submitted_date=models.DateField(auto_now_add=True)
    submitted_time=models.TimeField(auto_now_add=True)
    submitted_on_time=models.BooleanField(default=True)
    marks_alloted=models.IntegerField(default=0)
    submission_file = models.FileField(upload_to='doc')

class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    classroom_id =  models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    @property
    def resources(self):
        return self.resource_set.all()
    
    @property
    def content_type(self):
        return 'post'
    
    @property
    def post_comment(self):
        return list(self.comment_set.all())

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.post.title} -> {self.user.username} ({self.pk})'



# class Todo(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     is_done = models.BooleanField(default=False)



