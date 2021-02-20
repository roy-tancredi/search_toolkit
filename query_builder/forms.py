from itertools import chain

from django import forms
from django.core.exceptions import ValidationError

from .models import SearchEngine


# makeshift solution before implementing more search engines
all_settings = SearchEngine.objects.get(pk=3).searchsetting_set.all()


class SettingsSelectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SettingsSelectForm, self).__init__(*args, **kwargs)

        settings = [(s.id, s.descriptor, s.group)
                    for s in all_settings.exclude(group='basic')]

        grouped_settings = self.group_by_value(settings, 2).items()

        for label, choices in grouped_settings:
            self.fields[label] = forms.MultipleChoiceField(
                label=label.title(), choices=choices, required=False,
                widget=forms.CheckboxSelectMultiple)

    @staticmethod
    def group_by_value(items, i):
        """
        Groups iterable to dict by value of given index.

        Args:
            items (<iterable>): Iterable collection of settings.
            i (<int>): Index of value to group by.

        Returns:
            <dict> : Dict containing lists of settings as choices mapped by values of given attribute.
        """
        groups = {}
        for item in items:
            key = item[i]
            groups[key] = [item[:2], ] if key not in groups.keys(
            ) else groups[key] + [item[:2]]

        return groups

    def clean(self):
        data = list(chain(*super().clean().values()))
        cleaned_data = list(map(int, data))
        return cleaned_data


class QueryBuilderForm(forms.Form):

    query = forms.CharField(required=True)

    def __init__(self, settings, *args, **kwargs):
        super(QueryBuilderForm, self).__init__(*args, **kwargs)

        settings = [s for s in all_settings.filter(id__in=settings)]

        for s in settings:

            name = f'{s.group}_{s.id}'
            n = s.settingvalue_set.count()

            if n != 0:
                choices = [(v.id, v.human_readable)
                           for v in s.settingvalue_set.all()]
                self.fields[name] = forms.ChoiceField(
                    label=s.descriptor, choices=choices, required=False)
            else:
                self.fields[name] = forms.CharField(
                    label=s.descriptor, required=False)

            self.fields[name].group = s.group

    # def prepare_settings(self, grouped_settings):
    #     for label, settings in grouped_settings.items():
    #         settings = all_settings.filter(id__in=settings)
    #         grouped_settings[label] = settings
    #     return grouped_settings

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
