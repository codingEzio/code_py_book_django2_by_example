from django.urls import reverse_lazy

from django.views.generic.edit import (CreateView,
                                       FormView)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.mixins import LoginRequiredMixin

from courses.models import Course

from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """
        CreateView
            template_name   | form_class
            success_url
    """
    
    template_name   = 'students/student/registration.html'
    form_class      = UserCreationForm
    success_url     = reverse_lazy('student_course_list')
    
    def form_valid(self, form):
        result      = super(StudentRegistrationView, self).form_valid(form)
        
        clned_data  = form.cleaned_data
        user        = authenticate(username=clned_data['username'],
                                   password=clned_data['password1'])
        
        login(self.request, user)
        
        return result
    
    
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    
    """
    
    course          = None
    form_class      = CourseEnrollForm
    
    def form_valid(self, form):
        """
            Get the course -> add the student to the course
            
            The logic is not that hard,
                but .. the abstraction is kind weird to me ( the way getting data )
        """
        
        # `ModelChoiceField` while was hidden
        self.course = form.cleaned_data['course']
        
        self.course.students.add(self.request.user)
        
        return super(StudentEnrollCourseView,
                     self).form_valid(form)
    
    def get_success_url(self):
        """
            attr::success_url == method::get_success_url
        """
        
        # The page that user being redirected after he(she) enrolled
        #   Well, the page hasn't been impl_ed yet #TODO impl needed, XD
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
        This view is for students
            to < list the courses > that they're < enrolled in >
            
        LoginRequiredMixin      restricting access
        ListView                simply used for displaying data
    """
    
    model           = Course
    template_name   = 'students/course/list.html'
    
    def get_queryset(self):
        qset        = super(StudentCourseListView,
                            self).get_queryset()
        
        # init a qset -> do filtering -> enrolled-only
        return qset.filter(students__in=[self.request.user])
    

class StudentCourseDetailView(DetailView):
    model           = Course
    template_name   = 'students/course/detail.html'
    
    def get_queryset(self):
        qset        = super(StudentCourseDetailView,
                            self).get_queryset()
        
        return qset.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        """
            This function is for the 'urls.py'.
        """
        
        context     = super(StudentCourseDetailView,
                            self).get_context_data(**kwargs)
        
        # "Return the object the view is displaying."
        course      = self.get_object()
        
        # Two cases for this
        #   -- course/<pk>/<module_id>/
        #   -- course/<pk>/
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]
            
        return context