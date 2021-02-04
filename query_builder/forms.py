from django import forms
from .models import SearchEngine
from django.core.exceptions import ValidationError


class ListTextWidget(forms.TextInput):

    def __init__(self, name, data_list, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': f'list__{self._name}'})

    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the widget as an HTML string.
        """
        text_html = super(ListTextWidget, self).render(
            name, value, attrs=attrs)
        data_list = f'<datalist id="list__{self._name}">'
        for item in self._list:
            data_list += f'<option value="{item}">'
        data_list += '</datalist>'

        return (text_html + data_list)


class ListTextField(forms.Field):
    # def __init__(self, *, name=None, data_list=[], strip=True, empty_value='', **kwargs):

    def to_python(self, value):
        """Return a string."""
        if value not in self.empty_values:
            value = str(value)
            if self.strip:
                value = value.strip()
        if value in self.empty_values:
            return self.empty_value
        return value


class EngineSelectForm(forms.Form):
    data_list = [engine.name for engine in SearchEngine.objects.all()]
    engine = forms.CharField(
        label='Search Engine', max_length=100, strip=True, widget=ListTextWidget(
            name='engine', data_list=data_list, attrs={'placeholder': 'Start typing to select...'}))

    def clean_engine(self):
        data = self.cleaned_data['engine']
        if data not in self.data_list:
            raise ValidationError(
                'Please choose one of the available engines from the list.', code='invalid select')
        print(data, type(data))
        return data


class QueryBuilderForm(EngineSelectForm):
    options = ['Option 1.', 'Option 2.']

    search_query = forms.CharField(
        label='Search Query', max_length=100, strip=True, required=False)
    option = forms.CharField(
        label='Search Option', max_length=100, strip=True, required=False, widget=ListTextWidget(
            name='option', data_list=options))

    def clean_option(self):
        data = self.cleaned_data['option']
        if data not in self.options:
            raise ValidationError(
                'Please choose one of the available options from the list.', code='invalid select')
        print(data, type(data))
        return data
