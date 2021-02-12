import urllib

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import QueryBuilderForm, SettingsSelectForm


class MainIndex(TemplateView):
    template_name = 'query_builder/main_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = 'Hello!'
        return context


class SettingsSelectView(FormView):
    template_name = 'query_builder/forms.html'
    form_class = SettingsSelectForm
    success_url = '/query_builder'

    def form_valid(self, form):
        self.request.session['temp_data'] = form.cleaned_data
        return HttpResponseRedirect(self.success_url)


class QueryBuilderView(FormView):
    # TODO embrance the chaos with templates
    template_name = 'query_builder/forms.html'
    form_class = QueryBuilderForm
    success_url = '/'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['settings'] = self.request.session['temp_data'].get(
    #         'search_settings')
    #     return context

    def get_form(self, form_class=None):
        settings = self.request.session['temp_data'].get(
            'search_settings')
        if form_class is None:
            form_class = self.get_form_class()
        return self.form_class(settings, **self.get_form_kwargs())

    # def get(self, request):
    #     settings = self.get_context_data().get('settings', None)
    #     print(settings)
    #     context['text'] = settings
    #     # context['form'] = QueryBuilderForm(settings=settings)
    #     return self.render_to_response(context)

# ignore this class for now
# class QueryBuilderView(FormView):
#     template_name = 'query_builder/query_builder.html'

#     def __init__(self, form_class=EngineSelectForm, **kwargs):
#         super(QueryBuilderView, self).__init__()
#         self.form_class = form_class

#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         return super().post(self, request, context)

#     def form_valid(self, form):
#         context = self.get_context_data()
#         context['form'] = QueryBuilderForm(initial=form.data)
#         return render(self.request, self.template_name, context=context)
