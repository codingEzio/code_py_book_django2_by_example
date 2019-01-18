from django.urls import reverse_lazy

from django.views.generic.edit import (CreateView,
                                       FormView)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.mixins import LoginRequiredMixin

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
    