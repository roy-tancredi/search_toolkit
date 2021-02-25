from django.db import models


class SearchEngine(models.Model):
    """
    Represents a search engine.

    Atributes
    ---------
    name : <str>
        Distinctive name of search engine (or specific query type).

    get_url : <str>
        The base of specific URL for sending query.

    icon_path : <str>
        The path to search engine brand icon.

    """

    name = models.CharField(max_length=32, unique=True)
    get_url = models.CharField(max_length=64, unique=True)
    icon_path = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} Engine'


class SearchSetting(models.Model):
    """
    Represents search operators/special operators and more advenced search option, 
    like changing location or language, etc.

    Atributes
    ---------
    descritor : <str>
        Distinctive and diserable name of given option.

    ascriptors : <str>
        Synonims and alternatives for descriptor.

    description : <str>
        Description of option usage.

    engine : <ManyToManyField>
        Relation to SearchEngine Model through Invocation Model.

    tips : <str>
        Independent of engine general clues for using specific setting.

    group : <str>
        Settings' functional group marker.

    """

    descriptor = models.CharField(
        'the most adequate setting\'s name', max_length=64, unique=True)
    ascriptors = models.CharField(
        'verbal equivalents to descriptor', max_length=256, blank=True)
    description = models.TextField()
    engine = models.ManyToManyField(SearchEngine, through='Invocation')
    tips = models.CharField(
        'general clues for using specific setting', max_length=256, blank=True)
    group = models.CharField(
        'typology of search settings', max_length=64, blank=True)

    class Meta:
        ordering = ['descriptor']

    def __str__(self):
        return f'{self.descriptor}'


class Invocation(models.Model):
    """
    Contains specific usage parametrs for specific option in various search engines.

    Atributes
    ---------
    engine : <ForeignKey>
        Relation to SearchEngine Model.

    setting : <ForeignKey>
        Relation to SearchSetting Model.

    param_construct : <str>
        Specific parameter construction defined by engine provider as str object
        with placeholder for value.

    extra_tips : <str>
        Tips for usage setting in specific search engine.

    """

    engine = models.ForeignKey(SearchEngine, on_delete=models.CASCADE)
    setting = models.ForeignKey(SearchSetting, on_delete=models.CASCADE)
    param_construct = models.CharField(
        'search parameter key and syntax', max_length=128)
    extra_tips = models.CharField(
        'tips for usage in specific engine', max_length=256, blank=True)

    class Meta:
        ordering = ['setting']

    def __str__(self):
        return f'Invocation of {self.setting} for {self.engine}'


class SettingValue(models.Model):
    """
    Storing choices for settings if is needed.

    Atributes
    ---------

    value : <str>
        Value defined by engine provider.

    human_readable : <str>
        Value for performing.

    setting : <ManyToOneField>
        Relation to specific setting that refers to choices.

    """
    value = models.CharField(max_length=128)
    human_readable = models.CharField(max_length=128)
    setting = models.ForeignKey(
        SearchSetting, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'Value of {self.setting} Setting: {self.human_readable}'
