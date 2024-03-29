from django import forms


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
