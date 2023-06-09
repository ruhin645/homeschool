from django.contrib import admin
from .models import Assignments, Comment, Course, Post, Submissions,TeachersByClassroom,StudentsByClassroom
# Register your models here.
admin.site.register(Course)
admin.site.register(TeachersByClassroom)
admin.site.register(StudentsByClassroom)
admin.site.register(Assignments)
admin.site.register(Submissions)
admin.site.register(Post)
admin.site.register(Comment)

# admin.site.register(Todo)