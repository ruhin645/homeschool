from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_courses, name="teacher_dashboard"),
    path('/std',views.view_courses_std,name="std_home"),
    path('/addclass/', views.teacher_view, name="add_class"),
    path('/<str:slug>/delete', views.course_delete, name="course_delete"),
    path('/join',views.join_class,name='join_class'),
    path('/class/<int:id>',views.render_class,name='render_class'),
    path('/create_assignment/<int:classroom_id>',views.create_assignment,name='create_assignment'),
    path('/assignment_summary/<int:assignment_id>',views.assignment_summary,name='assignment_summary'),
    path('/assignment_summary_std/<int:assignment_id>',views.assignment_summary_std,name='assignment_summary_std'),
    path('/delete_assignment/<int:assignment_id>',views.delete_assignment,name='delete_assignment'),
    path('/submit_assignment_request/<int:assignment_id>',views.submit_assignment_request,name='submit_assignment_request'),
    path('/mark_submission_request/<int:submission_id>/<int:teacher_id>',views.mark_submission_request,name='mark_submission_request'),
    path('/create_post/<int:pk>',views.create_post,name='create_post'),
    path('/comment/create/<int:post_pk>/', views.create_comment, name='create_comment'),
    path('/delete_post/<int:post_id>',views.delete_post,name='delete_post'),
]

'''    path('/<str:slug>', views.course_details, name="course_details"),    path('/todo/', views.todo, name="todo"),

'''