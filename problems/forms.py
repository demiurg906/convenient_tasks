import re

from django import forms
import latex2mathml.converter


class EditableTexTextarea(forms.Textarea):
    template_name = 'tex_textarea.html'

    def render(self, name, value, attrs=None, renderer=None):
        splitted = re.split(r'(\$.*?\$)', value)
        for i in range(1, len(splitted), 2):
            splitted[i] = latex2mathml.converter.convert(splitted[i][1:-1])
        html_value = ''.join(splitted)
        attrs['math'] = html_value
        return super().render(name, value, attrs, renderer)
