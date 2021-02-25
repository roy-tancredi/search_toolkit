from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import QueryBuilderForm, SettingsSelectForm
from .models import SearchEngine


class MainIndex(TemplateView):
    template_name = 'query_builder/main_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = 'Hello!'
        return context


class SettingsSelectView(FormView):
    template_name = 'query_builder/query_builder.html'
    form_class = SettingsSelectForm
    success_url = '/query_builder'

    def form_valid(self, form):
        self.request.session['temp_data'] = form.cleaned_data
        return HttpResponseRedirect(self.success_url)


class QueryBuilderView(FormView):
    template_name = 'query_builder/query_builder.html'
    form_class = QueryBuilderForm
    success_url = '/'

    def get_form(self, form_class=None):
        settings_ids = self.request.session.get('temp_data')
        if form_class is None:
            form_class = self.get_form_class()
        return self.form_class(settings_ids, **self.get_form_kwargs())

    def form_valid(self, form):
        # makeshift solution before implementing more search engines
        engine = SearchEngine.objects.get(pk=3).get_url
        params = form.cleaned_data
        print(engine)

        return super().form_valid(form)
