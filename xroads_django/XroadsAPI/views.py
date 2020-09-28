from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from XroadsAPI.serializers import *


# Create your views here.
def csrf(request):
    return render(request, template_name='home.html')


# TODO change querysets
class DistrictViewset(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]

class SchoolViewset(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = BasicInfoSchoolSerial
    permission_classes = [IsAuthenticated]

    # TODO make permission that checks the request user belongs to the object
    @action(detail=True, methods=['post'])
    def join_school(self, request, *args, **kwargs):
        self.request.user.join_school(self.get_object())
        return Response(status=status.HTTP_202_ACCEPTED)


class ClubViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    # TODO change the serializer depending on what request it is
    serializer_class = ClubDetailSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        school_id = self.kwargs['school_pk']
        queryset = Club.objects.filter(school=school_id)
        return Response(BasicClubInfoSerial(queryset, many=True).data)

    @action(detail=True, methods=['post'])
    def join_club(self, request, *args, **kwargs):
        club = self.get_object()
        club.join(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def leave_club(self, request, *args, **kwargs):
        club = self.get_object()
        club.leave(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def ask_question(self, request, *args, **kwargs):
        club = self.get_object()
        question = QuestionSerializer(data=request.data, context={'request': request, 'club': club})
        if question.is_valid():
            question = question.save()

            club = self.get_object()
            club_editors = club.editors
            subject, from_email, to = f'Somebody asked a question about {club.name}!', settings.DJANGO_NO_REPLY, [prof.email for prof in club_editors]
            plain_text = get_template('email/question/EditorEmail.txt')
            
            text_content = plain_text.render({'club': club, 'question': question})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()

            return Response(status=status.HTTP_201_CREATED)
        return Response(question.errors, status=status.HTTP_400_BAD_REQUEST)
