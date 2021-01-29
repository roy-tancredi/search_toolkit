from django.db import models


class SettingValue(models.Model):
    """
    SOON...
    """
    value = models.CharField(max_length=128)
    human_readable = models.CharField(max_length=128)

    def __str__(self):
        return 'Value'


class SearchSetting(models.Model):
    """
    Represents search operators/special operators and more advenced search option, 
    like changing location or language, etc.

    ...
    Atributes
    ---------
    descritor : <str>
        Distinctive and diserable name of given option.

    ascriptors : <str>
        Synonims and alternatives for descriptor.

    description : <str>
        Description of option usage.

    values : <ManyToManyField>
        Setting's values if any specific.

    tips : <str>
        Independent of engine general clues for using specific setting.
    """
    descriptor = models.CharField(
        'the most adequate setting\'s name', max_length=64, unique=True)
    ascriptors = models.CharField(
        'verbal equivalents to setting\'s name', max_length=256, blank=True)
    description = models.TextField()
    values = models.ManyToManyField(SettingValue)
    tips = models.CharField(
        'general clues for using specific setting', max_length=256, blank=True)

    class Meta:
        ordering = ['descriptor']

    def __str__(self):
        return f'{self.descriptor} Option'


class SearchEngine(models.Model):
    """
    Represents a search engine.

    ...
    Atributes
    ---------
    name : <str>
        Distinctive name of search engine (or specific query type).

    get_url : <str>
        The base of specific URL for sending query.

    icon_path : <str>
        The path to search engine brand icon.

    setting : <ManyToManyField>
        Relation to SearchSetting Model through Invocation Model.

    """

    name = models.CharField(max_length=32, unique=True)
    get_url = models.CharField(max_length=64, unique=True)
    icon_path = models.CharField(max_length=128, blank=True)
    settings = models.ManyToManyField(SearchSetting, through='Invocation')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} Engine'


class Invocation(models.Model):
    """
    Contains specific usage parametrs for specific option in various search engines.

    ...
    Atributes
    ---------
    engine : <ForeignKey>
        Relation to SearchEngine Model.

    setting : <ForeignKey>
        Relation to SearchSetting Model.

    param_construct : <str>
        Specific parameter construction - <keyword>=<placeholder> in general.

    extra_tips : <str>
        Tips for usage setting in specific search engine.

    """

    engine = models.ForeignKey(SearchEngine, on_delete=models.CASCADE)
    setting = models.ForeignKey(SearchSetting, on_delete=models.CASCADE)
    param_construct = models.CharField(
        'search parameter key and syntax', max_length=128)
    extra_tips = models.CharField(
        'tips for usage in specific engine', max_length=256, blank=True)

    def __str__(self):
        return f'Invocation of {self.setting} for {self.engine}'
