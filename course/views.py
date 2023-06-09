import datetime
from datetime import datetime
from itertools import chain, count
from tkinter.messagebox import NO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentCreateForm, CreateAssignmentForm, PostForm, add_course
from .models import Assignments, Course, Post, StudentsByClassroom, Submissions, TeachersByClassroom ,Comment
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timesince import timesince

# Create your views here.
@login_required
def teacher_view(request, *args, **kwargs):
    form = add_course(request.POST or None)
    context = {}
    if form.is_valid():
        course = form.save(commit=False)
        course.created_by = request.user
        course.save()
        teacher = TeachersByClassroom(teacher=request.user,classroom=course)
        teacher.save()
        messages.success(request, "Class Created Sucessfully!!")
        return redirect('/tdashboard')
    context['add_courses'] = form
    return render(request, 'teacherview.html', context)

@login_required
def view_courses(request, *args, **kwargs):
    courses = Course.objects.filter(created_by=request.user)
    dict = {'course': courses}
    return render(request, 'teacherhome.html', dict)


@login_required
def view_courses_std(request, *args, **kwargs):
    courses = StudentsByClassroom.objects.filter(student=request.user)
    dict = {'course': courses}
    return render(request, 'stview.html', dict)

'''def course_details(request, slug):
    dict = { "slug": slug}
    return render (request, 'crsdetail.html',dict)'''

def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course.delete()
    return redirect('/tdashboard')

    '''return render(request, 'teacherhome.html', {'course': course})'''

# def join_class(request):
#     if request.POST.get('action') == 'post':
#         code = request.POST.get('classroom_id')
#         try:
#             classroom = Course.objects.get(classroom_id=code)
#             student = StudentsByClassroom.objects.filter(student = request.user,classroom=classroom)
#             if (student.count()!=0):
#                 return redirect('/sdashboard')
#             else:
#                 return render(request, "join.html", {"message": "Classroom code does not exist"})
#         except Exception as e:
#             print(e)
#             return JsonResponse({'status':'FAIL','message':str(e)})
#         student = StudentsByClassroom(student= request.user, classroom = classroom)
#         student.save()
#         return JsonResponse({'status':'SUCCESS'})



def join_class(request):
    if request.method == "POST":
        if request.user.is_student:
            code = request.POST["code"]
            try:
                classrooms = Course.objects.get(classroom_id=code)
            except Exception as e:
                classrooms = None
            students = StudentsByClassroom.objects.filter(student=request.user,classroom=classrooms)
            if (students.count()!=0):
                return redirect('/tdashboard/std')
        if(classrooms != None):  
            student = StudentsByClassroom(student= request.user, classroom = classrooms)
            student.save()
            messages.success(request, 'Successfully Enrolled')
            return redirect('/tdashboard/std')
        else:
            messages.error(request, 'Check Your code again')
            return render(request, "join.html")
    else:
        return render(request, "join.html")

def render_class(request,id):
    classroom = Course.objects.get(pk=id)
    try: 
        assignments = Assignments.objects.filter(classroom_id = id)
    except Exception as e:
        assignments = None

    try:
        students = StudentsByClassroom.objects.filter(classroom = id)
    except Exception as e:
        students = None
    
    teachers = TeachersByClassroom.objects.filter(classroom = id)
    teacher_mapping = TeachersByClassroom.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = StudentsByClassroom.objects.filter(student=request.user).select_related('classroom')
    mappings = chain(teacher_mapping,student_mapping) 
    post_form = PostForm()
    comment_form = CommentCreateForm()
    context = {
        'post_form': post_form,
        'comment_form': comment_form,
        'classroom':classroom,'assignments':assignments,'students':students,'teachers':teachers,"mappings":mappings,
    }
    try:
        post = Post.objects.filter(classroom_id=classroom)
        context.update({'posts':post})
        try:
            comment = Comment.objects.filter(post__in=post)
            context.update({'contents':comment})
            return render(request,'class_page.html',context)
        except:
            return render(request,'class_page.html',context)
    except:
        return render(request,'class_page.html',context)


def create_assignment(request,classroom_id):
    mappings = TeachersByClassroom.objects.filter(teacher=request.user).select_related('classroom')
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            assignment_name = form.cleaned_data.get('title')
            due_date = form.cleaned_data.get('due_date')
            due_time = form.cleaned_data.get('due_time')
            classroom_id = Course.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            total_marks = form.cleaned_data.get('total_marks')
            assignment = Assignments(title = assignment_name,due_date = due_date,due_time=due_time,instructions = instructions,total_marks = total_marks,classroom_id=classroom_id)
            assignment.save()
            # email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('/tdashboard')
        else:
            return render(request,'create_assignment.html',{'form':form,'mappings':mappings})
    form = CreateAssignmentForm()
    return render(request,'create_assignment.html',{'form':form,'mappings':mappings})

#assingment submit view + summeary view

def assignment_summary(request,assignment_id):
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teachers = TeachersByClassroom.objects.filter(classroom = assignment.classroom_id)
    teacher_mapping = TeachersByClassroom.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = StudentsByClassroom.objects.filter(student=request.user).select_related('classroom')
    no_of_students = StudentsByClassroom.objects.filter(classroom=assignment.classroom_id)
    mappings = chain(teacher_mapping,student_mapping)
    return render(request,'assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})


def assignment_summary_std(request,assignment_id):
    assignment = Assignments.objects.get(pk = assignment_id)
    teacher_mapping = TeachersByClassroom.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = StudentsByClassroom.objects.filter(student=request.user).select_related('classroom')
    mappings = chain(teacher_mapping,student_mapping)
    try:
        submission = Submissions.objects.get(assignment_id=assignment)
        return render(request,'crsdetail.html',{'assignment':assignment,'mappings':mappings,'submission':submission})
    except:
        return render(request,'crsdetail.html',{'assignment':assignment,'mappings':mappings})


def delete_assignment(request,assignment_id):
    try:
        assignment = Assignments.objects.get(pk=assignment_id)
        classroom_id = assignment.classroom_id.id 
        Assignments.objects.get(pk=assignment_id).delete()
        return redirect('render_class', id=classroom_id)
    except Exception(e):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def mark_submission_request(request,submission_id,teacher_id):
    if request.method == 'POST':
        marks =  request.POST["submission_marks"]
        submission = Submissions.objects.get(pk=submission_id)
        submission.marks_alloted = marks
        submission.save()
        #email.submission_marks_mail(submission_id,teacher_id,marks)
        messages.success(request, 'Graded!!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def submit_assignment_request(request,assignment_id):
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = StudentsByClassroom.objects.get(classroom=assignment.classroom_id,student=request.user)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
        submission.submission_file = file_name
        submission.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:  
        print(str(e))  
        submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
        dt1=datetime.now()
        dt2=datetime.combine(assignment.due_date,assignment.due_time)
        time = timesince(dt1, dt2)
        if time[0]=='0':
            submission.submitted_on_time=False
        submission.save()
        #email.submission_done_mail(assignment_id,request.user,file_name)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@login_required
def create_post(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            classroom = get_object_or_404(Course,pk = pk)
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            post = Post.objects.create(title=title,description=description,created_by=request.user,classroom_id=classroom)
            
        else:
            messages.danger(request, f'Cannot create post')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def create_comment(request, post_pk):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=post_pk)
            comment = Comment(
                user=request.user, 
                comment_text=form.cleaned_data.get('comment_text'),
                post = post
            )
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_post(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    