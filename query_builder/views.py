from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .forms import EngineSelectForm, QueryBuilderForm


class MainIndex(TemplateView):
    template_name = 'query_builder/main_index.html'


class QueryBuilderView(FormView):
    template_name = 'query_builder/query_builder.html'

    def __init__(self, **kwargs):
        super(QueryBuilderView, self).__init__()
        self.form_class = QueryBuilderForm  # ! How to set form class dynamically?

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super().post(self, request, context)

    def form_valid(self, form):
        context = self.get_context_data()
        context['form'] = QueryBuilderForm()
        return render(self.request, self.template_name, context=context)


# def query_builder(request, **kwargs):
#     context = {
#         'form': EngineSelectForm(),
#         'status': '0'
#     }

#     if request.method == 'POST':
#         if context['status'] == '1':
#             redirect('https://www.duckduckgo.com/')
#         else:
#             context['form'] = QueryBuilderForm(initial=request.POST)
#             context['status'] = '1'
#     return render(request, 'query_builder/query_builder.html', context)
