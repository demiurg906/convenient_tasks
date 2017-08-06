from django import forms
from problems.templatetags.problems_extras import convert_to_mathml


class EditableTexTextarea(forms.Textarea):
    template_name = 'tex_textarea.html'

    def render(self, name, value, attrs=None, renderer=None):
        attrs['math'] = convert_to_mathml(value)
        return super().render(name, value, attrs, renderer)
