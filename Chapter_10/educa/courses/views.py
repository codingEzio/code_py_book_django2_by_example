from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

from django.views.generic.base import (View,
                                       TemplateResponseMixin)

from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from .models import Course
from .forms import ModuleFormSet


class OwnerMixin(object):
    """
        Making the result that only contains
            the content for the current user (& no more).
    """
    
    def get_queryset(self):
        qset = super(OwnerMixin, self).get_queryset()
        
        return qset.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """
        Still, we're inserting the "current user" to the form validation.
        
        This mixin might be used by
            objs that related to `CreateView` and `UpdateView`.
    """
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    """
        The first mixin is used to
            restricting objects that belong to the current user.
    """
    
    model       = Course
    
    fields      = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
        OwnerCourseMixin    restrict scope(user) & naming model(Course)
        OwnerEditMixin      validation & redirect-related (`success_url`)
    """
    
    fields          = ['subject', 'title', 'slug', 'overview']
    success_url     = reverse_lazy('manage_course_list')
    template_name   = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
        Display only.
        
        OwnerCourseMixin    restrict scope(user) & naming model(Course)
        ListView            let Django help do most of the work
    """
    
    template_name   = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    """
        These are included:
            scope(user), model, validate-redirect & the related view of Dj's.
    """
    
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    """
        These are included:
            scope(user), model, validate-redirect & the related view of Dj's.
    """
    
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    """
        OwnerCourseMixin    restrict scope(user) & naming model(Course)
        DeleteView          page for displaying 'del-confirm' & 'del-success'
    """
    
    template_name       = 'courses/manage/course/delete.html'
    success_url         = reverse_lazy('manage_course_list')
    
    permission_required = 'courses.delete_course'
    
    
class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
        As the class name suggests, this view(class)
            handles the `formset` to {add, update, delete} modules for a course.
        
        HOWTO :: distinguish two inherited classes
            Ours                    get_formset, course, formset
            View                    dispatch, get, post
            TemplateResponseMixin   `render_to_response` (inside `get` & `post`)
    """
    
    template_name   = 'courses/manage/module/formset.html'
    course          = None
    
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        
        return super(CourseModuleUpdateView, self).dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        
        return self.render_to_response({'course'    : self.course,
                                        'formset'   : formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        
        return self.render_to_response({'course'    : self.course,
                                        'formset'   : formset})