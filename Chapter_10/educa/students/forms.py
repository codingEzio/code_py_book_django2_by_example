from django import forms

from courses.models import Course


class CourseEnrollForm(forms.Form):
    """
        (Note: it does NOT conv to this in our cases, cuz it's hidden)
        
        ModelChoiceField    =>  <select id=".." name="..">
                                    <option value="..">Option #1</option>
                                    <option value="..">Option #2</option>
                                    ...
                                </select>
        
        Oh, this form would be
            used for students to enroll in courses (not directly) :P
            
        It was used like this ( as a 'button', actually )
            self.course = form.cleaned_data['course']
            self.course.students.add(self.request.user)
    """
    
    # Choice pool :: all the courses
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
    
    