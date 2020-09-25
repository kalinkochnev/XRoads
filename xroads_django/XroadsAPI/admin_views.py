from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

from XroadsAPI import mixins as api_mixins
from XroadsAPI.forms import *
from XroadsAuth.permissions import *
from XroadsAPI.serializers import *
from XroadsAuth.serializers import ProfileSerializer


# TODO make sure that you set read_only=True on nested fields so then .update() works

class UserViewset(viewsets.GenericViewSet, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, MinSchoolAdminForUser]
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    hier_perms = ['view-user-detail']
    queryset = Profile

    def retrieve(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().retrieve(request, *args, **kwargs)

# TODO make views that lists everybody who has permissions for that view


class DistrictViewset(api_mixins.ModifyAndReadViewset, api_mixins.AdminMixin):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    allowed_methods = ['get', 'post', 'put', 'patch']
    hier_perms = []
    permission_classes = [IsAuthenticated, MinDistrictRole]

    @action(detail=True, methods=['post'])
    def add_admin(self, request, *args, **kwargs):
        return self.add_admin(request, hier_role=PermConst.SCHOOL_ADMIN)

    @action(detail=True, methods=['post'])
    def remove_admin(self, request, *args, **kwargs):
        return self.remove_admin(request)


class SchoolViewset(api_mixins.ModifyAndReadViewset, api_mixins.AdminMixin):
    queryset = School.objects.all()
    serializer_class = SchoolAdminSerializer
    permission_classes = [IsAuthenticated, MinSchoolRole]
    hier_perms = []

    # TODO test create_school
    @action(detail=True, methods=['post'])
    def create_school(self, request, *args, **kwargs):
        serializer = SchoolAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # TODO test toggle hide
    @action(detail=True, methods=['post'])
    def toggle_hide(self, request, *args, **kwargs):
        school = self.get_object()
        school.toggle_hide()
        return Response(status=204)

    @action(detail=True, methods=['get'])
    def clubs(self, request, *args, **kwargs):
        return self.add_admin(request, hier_role=PermConst.SCHOOL_ADMIN)

    @action(detail=True, methods=['post'])
    def add_admin(self, request, *args, **kwargs):
        return self.add_admin(request, hier_role=PermConst.SCHOOL_ADMIN)

    @action(detail=True, methods=['post'])
    def remove_admin(self, request, *args, **kwargs):
        return self.remove_admin(request)

    # TODO test create_club
    @action(detail=True, methods=['post'])
    def create_club(self, request, *args, **kwargs):
        club_serializer = CreateClubForm(data=request.data)
        if club_serializer.is_valid():
            club_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=club_serializer.errors)


class ClubViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, api_mixins.AdminMixin):
    queryset = Club.objects.all()
    serializer_class = ClubEditorSerializer
    permission_classes = [IsAuthenticated, MinClubEditor]
    hier_perms = []

    modify_perms = {
        'Advisor': ['Editor', 'Advisor'],
        'Editor': ['Editor']
    }
    # TODO change the queryset to only include the clubs in the person's school

    # TODO create toggle_hide mixin
    @action(detail=True, methods=['post'])
    def toggle_hide(self, request, *args, **kwargs):
        club = self.get_object()
        club.toggle_hide()
        return Response(status=202)

    @action(detail=True, methods=['post'])
    def add_editor(self, request, *args, **kwargs):
        def invite_club_admin(to_emails):
            subject, from_email, to = "You were invited to xroads!", settings.DJANGO_NO_REPLY, to_emails
            plain_text = get_template('email/sharing/invite.txt')

            text_content = plain_text.render({'club': self.get_object()})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()
        return self.add_admin(request, hier_role=PermConst.CLUB_EDITOR, email_func=invite_club_admin)

    @action(detail=True, methods=['post'])
    def remove_editor(self, request, *args, **kwargs):
        return self.remove_admin(request)

    @action(detail=True, methods=['get'])
    def list_editors(self, request, *args, **kwargs):
        return self.list_admins(request)

    # TODO create slide views
    @action(detail=True, methods=['get'])
    def slides(self, request, *args, **kwargs):
        pass

    @action(detail=True, methods=['post'])
    def answer_question(self, request, *args, **kwargs):
        question = AnswerQuestionSerializer(
            data=request.data, context={'request': request})
        if question.is_valid():
            question = question.save()

            club = self.get_object()
            subject, from_email, to = f'Your question about {club.name} was answered!', settings.DJANGO_NO_REPLY, [
                question.asker.email]
            plain_text = get_template('email/question/AnswerEmail.txt')

            text_content = plain_text.render(
                {'question': question, 'club': club})

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.send()

            return Response(status=status.HTTP_200_OK)
        return Response(question.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def questions(self, request, *args, **kwargs):
        club = self.get_object()
        questions = Question.objects.filter(club=club)
        return Response(GetQuestionSerializer(questions, many=True).data, status=status.HTTP_200_OK)
