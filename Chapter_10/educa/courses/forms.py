from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module

__doc__ = \
"""
    inlineformset_x     Many modules in one course ("inline" -> "closer")
    
        Course      Parent model
        Module      (child) Model
        
        fields      What fields will be included
        extra=2     How many 'forms' to display (default: 1)
        
        can_delete  Auto-add a `Delete` boolean field (mark-del => submit => del_ed)
"""

ModuleFormSet = inlineformset_factory(Course, Module,
                                      fields=['title',
                                              'description'],
                                      extra=2,
                                      can_delete=True)

