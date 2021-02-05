from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

from .forms import SettingsSelectForm


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
        context = form.cleaned_data
        return HttpResponseRedirect(self.success_url, context)


class QueryBuilderView(TemplateView):
    # TODO embrance the chaos with templates
    template_name = 'query_builder/main_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = 'Done!'
        return context

# ignore this class for now
# class QueryBuilderView(FormView):
#     template_name = 'query_builder/query_builder.html'

#     def __init__(self, form_class=EngineSelectForm, **kwargs):
#         super(QueryBuilderView, self).__init__()
#         self.form_class = form_class  # ! How to set form class dynamically?

#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         return super().post(self, request, context)

#     def form_valid(self, form):
#         context = self.get_context_data()
#         context['form'] = QueryBuilderForm(initial=form.data)
#         return render(self.request, self.template_name, context=context)
