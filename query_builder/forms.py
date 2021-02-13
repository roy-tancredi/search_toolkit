from django import forms
from django.core.exceptions import ValidationError

from .models import SearchEngine

all_settings = SearchEngine.objects.get(pk=3).searchsetting_set.all()


class SettingsSelectForm(forms.Form):
    setting_choices = [(s.id, s.descriptor) for s in all_settings]

    search_settings = forms.MultipleChoiceField(
        choices=setting_choices, required=True, widget=forms.CheckboxSelectMultiple)

    def clean_search_settings(self):
        settings = self.cleaned_data['search_settings']
        data = list(map(int, settings))
        for item in data:
            if item not in [setting.id for setting in all_settings]:
                raise ValidationError(
                    "Something went wrong. Please try again.")
        return data


class QueryBuilderForm(forms.Form):

    def __init__(self, settings=None, *args, **kwargs):
        settings = all_settings.filter(id__in=settings)

        super(QueryBuilderForm, self).__init__(*args, **kwargs)

        for i, setting in enumerate(settings):
            self.fields[f'setting_{setting.id}'] = forms.CharField(
                label=setting.descriptor)


# ignore this class for now
# class ListTextWidget(forms.TextInput):

#     def __init__(self, name, data_list, *args, **kwargs):
#         super(ListTextWidget, self).__init__(*args, **kwargs)
#         self._name = name
#         self._list = data_list
#         self.attrs.update({'list': f'list__{self._name}'})

#     def render(self, name, value, attrs=None, renderer=None):
#         """
#         Render the widget as an HTML string.
#         """
#         text_html = super(ListTextWidget, self).render(
#             name, value, attrs=attrs)
#         data_list = f'<datalist id="list__{self._name}">'
#         for item in self._list:
#             data_list += f'<option value="{item}">'
#         data_list += '</datalist>'

#         return (text_html + data_list)
