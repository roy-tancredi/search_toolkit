import json
from query_builder.models import *

with open('C:\\Users\\Maciej\\search_toolkit\\search_toolkit\\search_engines\\google_params.json') as f:
    settings_json = json.load(f)


for setting in settings_json:
    setting = SearchSetting(descriptor=setting['descriptor'], ascriptors=setting['ascriptors'],
                            description=setting['description'], through_defaults={'param_construct': setting['parameter_construct']})
    setting.save()
