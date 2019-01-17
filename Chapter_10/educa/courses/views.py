from django.forms.models import modelform_factory
from django.apps import apps

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

from .models import Course, Content, Module
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
    
    
class ContentCreateUpdateView(TemplateResponseMixin, View):
    """ This view is corresponding to two url patterns.
        - one for 'module_content_create'
        - one for 'module_content_update'
        
        With ID     ->  update
        Without ID  ->  create
    """
    
    module          = None
    model           = None
    obj             = None
    template_name   = 'courses/manage/content/form.html'
    
    def get_model(self, model_name):
        """
            Return the actual model (one of four)
                while excluding some of them (we don't need)
        """
        
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        
        return None
    
    def get_form(self, model, *args, **kwargs):
        """
            As the name of `modelform_factory` suggests,
                it simply "produces" the fields (of 'text | video | image | file').
                
            We'll exclude some fields (e.g. `owner`) ,
                as we only need stuff like `title`, `video` etc.
                
                Details
                    Content     order
                    ItemBase    owner, created, updated
        """
        
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        """
            Here's what the <Django-doc> says
            
                The default implementation will
                -  inspect the HTTP method and
                -  attempt to delegate to a method that matches one of them.
                
            So from my understanding,
                it might be a pre-setup for the incoming `GET`, `POST` ?
                
            ----- ----- -----
            
            Q
                Oh, where're these params come from?
                I mean, the `module_id`, `model_name` kind of thing?
            A
                Well, it lives in <urls.py> (as placeholder).
                e.g. "module/<int:module_id>/content/<model_name>/<id>/"
                
            ----- ----- -----
            
            Quotes from the book
            
                It receives the URL params and
                    stores the { module, model, content-obj } as class attrs.
                    
                module_id   the module's ID (the content'll be associated with)
                model_name  the content's model-name (create | update)
                id | obj    the ID of the object that is being updated
        """
        
        # urls.py :: <int:module_id>
        self.module = get_object_or_404(Module, id=module_id,
                                        course__owner=request.user)

        # urls.py :: <model_name>
        self.model = self.get_model(model_name)

        # urls.py :: <id>
        if id:
            self.obj = get_object_or_404(self.model, id=id,
                                         owner=request.user)
            
        return super(ContentCreateUpdateView,
                     self).dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        """
            #TODO further explanation needed
            Build the model-form for the ['text', 'video', 'image', 'file'].
        """
        
        form = self.get_form(self.model, instance=self.obj)
        
        return self.render_to_response({'form'      : form,
                                        'object'    : self.obj})
    
    def post(self, request, module_id, model_name, id=None):
        """
            #TODO further explanation needed
        """
        
        # Build form with submitted data :D
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        
        # Add an 'user' before saving
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            
            # This option indicates the opt (create | update)
            if not id:
                Content.objects.create(module=self.module,
                                       item=obj)
            
            # Done here if 'create'
            return redirect('module_content_list', self.module.id)
        
        # Done here if 'update'
        return self.render_to_response({'form'      : form,
                                        'object'    : self.obj})
        
        
class ContentDeleteView(View):
    
    def post(self, request, id):
        content = get_object_or_404(Content, id=id,
                                    module__course__owner=request.user)
        
        # fk related
        module = content.module
        
        content.item.delete()
        content.delete()
        
        return redirect('module_content_list', module.id)