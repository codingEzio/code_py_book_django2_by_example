from rest_framework import generics

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Subject, Course
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
    queryset            = Subject.objects.all()
    serializer_class    = SubjectSerializer
    

class SubjectDetailView(generics.RetrieveAPIView):
    queryset            = Subject.objects.all()
    serializer_class    = SubjectSerializer
    

class CourseEnrollView(APIView):
    """
        It's just like the `View` provided by Django
            but the mechanics for it is kinda different :P
            
        The handlers (DjREST | Dj)
            Request     HttpRequest
            Response    HttpResponse
    """
    
    authentication_classes  = (BasicAuthentication, )
    permission_classes      = (IsAuthenticated, )
    
    def post(self, request, pk, format=None):
        
        # 'courses/<pk>/enroll/'
        course = get_object_or_404(Course, pk=pk)
        
        # auth-process needed :D
        course.students.add(request.user)
        
        return Response({'enrolled': True})