from django.urls import reverse_lazy
from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from .models import Course


# This is the only change we've made
#   that is "Making users can only CRUD their own courses"


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