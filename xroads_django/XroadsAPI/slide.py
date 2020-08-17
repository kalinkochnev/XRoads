import XroadsAPI.models as Models
from XroadsAPI.exceptions import SlideParamError

class SlideTemplates:
    class Template:
        possible_args = ['img', 'text', 'video_url']

        def __init__(self, temp_id: int, name, required):
            self.temp_id = temp_id

            # makes sure that position is always included
            self.required_args = required
            self.required_args.append('position')

            self.name = name

        def args_match(self, args):
            return set(args) == set(self.required_args)

    templates = [
        Template(temp_id=1, name="img/text",  required=['img', 'text']),
        Template(temp_id=2, name="img_only", required=['img']),
        Template(temp_id=3, name="video_only", required=['video_url']),
        Template(temp_id=4, name="text_only", required=['text'])
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

        if template.args_match(kwargs.keys()):
            return Models.Slide.objects.create(club=club, template_type=temp_id, **kwargs)
        raise SlideParamError(
            f'Args given do not match. Expected args: {template.required_args} Given: {kwargs} ')

