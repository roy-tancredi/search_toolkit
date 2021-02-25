from itertools import chain, groupby
# from operator import attrgetter
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import SearchEngine
from .customized import ListTextWidget


# makeshift solution before implementing more search engines
all_settings = SearchEngine.objects.get(pk=3).searchsetting_set.all()


class SettingsSelectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SettingsSelectForm, self).__init__(*args, **kwargs)

        # _setting_attrs = attrgetter('id', 'descriptor', 'group')
        _settings = [(s.id, s.descriptor, s.group)
                     for s in all_settings.exclude(group__in=('basic', 'basic operators'))]

        _grouped_settings = self._group_by_value(_settings, 2).items()

        for label, choices in _grouped_settings:
            self.fields[label] = forms.MultipleChoiceField(
                label=label.title(), choices=choices, required=False,
                widget=forms.CheckboxSelectMultiple)
            self.fields[label].group = label

    @ staticmethod
    def _group_by_value(items, i):
        """
        Infirm copy of groupby function from itertools.

        Args:
            items (<iterable>): Collection of items to sort.
            i (<int>): Index of item to group by.

        Returns:
            <dict>: Dictionary of items grouped by unique values of given item.
        """
        groups = {}
        for item in items:
            key = item[i]
            groups[key] = [item[:2], ] if key not in groups.keys(
            ) else groups[key] + [item[:2]]

        return groups

    def clean(self):
        """
        Returns simple list of ids.

        Returns:
            <list>: List of integers.
        """
        data = list(chain.from_iterable(super().clean().values()))
        cleaned_data = list(map(int, data))
        return cleaned_data


class QueryBuilderForm(forms.Form):

    query = forms.CharField(required=True)

    def __init__(self, settings_ids, *args, **kwargs):
        super(QueryBuilderForm, self).__init__(*args, **kwargs)

        # received ids from SettingsSelectForm instance
        self.settings_ids = settings_ids
        self.settings = [s for s in all_settings.filter(
            id__in=self.settings_ids)]

        for s in self.settings:

            name = f'setting_{s.id}'
            n = s.settingvalue_set.count()

            # boolean fields
            if n == 2:
                self.fields[name] = forms.BooleanField(
                    label=s.descriptor, required=False)

            # choice fields
            elif 2 < n:
                choices = [(v.id, v.human_readable)
                           for v in s.settingvalue_set.all()]
                coerce_list = [v[1] for v in choices]
                self.fields[name] = forms.TypedChoiceField(
                    label=s.descriptor, choices=choices, coerce=coerce_list, required=False)

            # char fields - the rest of the usual fields
            else:
                self.fields[name] = forms.CharField(
                    label=s.descriptor, required=False)

            self.fields[name].group = s.group

    def clean_query(self):
        value = self.cleaned_data['query'].replace(' ', '+')
        # complex_terms_patterns = re.compile(r"""
        #                                      (?P<phrases>".+?")|                       # phrases
        #                                      (?P<parenthesis>\(.+?\))|                 # parenthesis
        #                                      (?P<alternations>(\w+?\s*\|\s*\w+?\b))    # alternations
        #                                      (?P<specials>\w[a-z]+?[:].+(?:\s))        # special operators
        #                                      """, re.VERBOSE)

        # complex_terms = re.findall(complex_terms_patterns, query)

        return value

    def clean(self):
        # boolean_fields = ('81', '84', '85', '86', '91')
        cleaned_data = self.cleaned_data
        data = super().clean()
        print(data)
        return cleaned_data

    @ staticmethod
    def _clean_boolean_fields():
        data = [(k, v) for (k, v) in cleaned_data.items() if type(v) == bool}

        cleaned_data = {}
        for k, v in data:
            key = k.split('_')[1]
