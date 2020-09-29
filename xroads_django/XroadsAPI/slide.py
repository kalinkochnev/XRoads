import XroadsAPI.models as Models
from XroadsAPI.exceptions import InvalidSlideTemplate, SlideParamError

class SlideTemplates:
    class Template:
        possible_args = ['img', 'text', 'video_url', 'body', 'position']

        def __init__(self, temp_id: int, name, disabled, *args, **kwargs):
            assert 'required' not in kwargs.keys()

            self.temp_id = temp_id

            # makes sure that position is always included
            self.disabled_args = disabled

            self.name = name

        @property
        def useable_args(self):
            return set(self.possible_args).difference(self.disabled_args)

        def has_proper_args(self, args):
            has_position = 'position' in args
            has_possible = len(set(args).intersection(self.possible_args)) == len(args)# Don't include position
            contains_invalid = len(set(args).intersection(self.disabled_args)) > 0
            return has_possible and not contains_invalid and has_position

    templates = [
        Template(temp_id=1, name="img", disabled=['video_url', 'body']),
        Template(temp_id=2, name="text", disabled=['video_url', 'img']),
        Template(temp_id=3, name="video", disabled=['video_url', 'text', 'body']),
    ]

    @classmethod
    def get(cls, temp_id: int):
        for temp in cls.templates:
            if temp.temp_id == temp_id:
                return temp
        raise InvalidSlideTemplate(
            'The specified template type does not exist')

    @classmethod
    def new_slide(cls, temp_id, club, **kwargs: dict):
        template = SlideTemplates.get(temp_id)

        if template.has_proper_args(kwargs.keys()):
            return Models.Slide.objects.create(club=club, template_type=temp_id, **kwargs)
        raise SlideParamError(
            f'Args given do not match. Possible args: {template.useable_args} Given: {kwargs} ')

