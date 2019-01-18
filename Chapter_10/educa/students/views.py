from django.urls import reverse_lazy

from django.views.generic.edit import CreateView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


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