from rest_framework import serializers

from ..models import Subject, Course, Module


class SubjectSerializer(serializers.ModelSerializer):
    """
        Testing its usage in 'Python Console' ( using PyCharm )
            
            from courses.models import Subject
            from courses.api.serializers import SubjectSerializer
            
            subject = Subject.objects.latest('id')
            selizer = SubjectSerializer(subject)
            
            selizer.data
            >> {'id': 2, 'title': 'Computer Science', 'slug': 'computer-science'}
    """
    
    class Meta:
        """
            model    what models to be serialized
            fields   what fields need to be included (all if not specified)
        """
        
        model   = Subject
        fields  = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Module
        fields  = ['order', 'title', 'description']
        
        
class CourseSerializer(serializers.ModelSerializer):
    
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model   = Course
        fields  = ['id',
                   'subject', 'title',
                   'slug', 'overview', 'created',
                   'owner', 'modules']