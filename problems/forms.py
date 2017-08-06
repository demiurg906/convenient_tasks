import latex2mathml.converter
import logging
import re

from django import forms




class EditableTexTextarea(forms.Textarea):
    template_name = 'tex_textarea.html'

    def render(self, name, value, attrs=None, renderer=None):
        splitted = re.split(r'(\$.*?\$)', value)
        for i in range(1, len(splitted), 2):
            try:
                splitted[i] = latex2mathml.converter.convert(splitted[i][1:-1])
            except Exception as e:
                logger.exception(e)
                splitted[i] = f'<b><i>incorrect LaTeX input {splitted[i]}</i></b>'
        html_value = ''.join(splitted)
        attrs['math'] = html_value
        return super().render(name, value, attrs, renderer)
