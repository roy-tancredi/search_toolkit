# import json

# from query_builder.models import SearchEngine, SearchSetting, Invocation

# google = SearchEngine.objects.get(name='Google Search')


# with open(r'C:\Users\Maciej\search_toolkit\search_toolkit\search_engines\google_params.json') as f:
#     settings_json = json.load(f)['settings']

# for setting in settings_json:
#     setting_obj = SearchSetting(descriptor=setting['descriptor'], ascriptors=setting['ascriptors'], description=setting['description'],
#                                 tips=setting['tips'], setting_type=setting['setting_type'])
#     setting_obj.save()
#     setting_obj.engine.add(google)
#     through_model = Invocation.objects.get(
#         engine=google.id, setting=setting_obj.id)
#     through_model.param_construct = setting['param_construct']
#     through_model.extra_tips = setting['extra_tips']
#     through_model.save()
