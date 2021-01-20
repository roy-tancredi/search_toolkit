from django.db import models


class SearchOption(models.Model):
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

    # SOON....
    """
    descriptor = models.CharField(max_length=64)
    # TODO \/ Need to be converted to some iterable.
    ascriptors = models.CharField(max_length=256)
    description = models.TextField()
    tips = models.CharField(max_length=256)

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

    option : <ManyToManyField>
        Relation to Option Model through Invocation Model.

    """

    name = models.CharField(max_length=32)
    get_url = models.CharField(max_length=64)
    icon_path = models.CharField(max_length=128)
    # ! Need to add related_name if there are another field in other model with same name?
    option = models.ManyToManyField(SearchOption, through='Invocation')

    def __str__(self):
        return f'{self.name} Engine'


class Invocation(models.Model):
    """
    Contains specific usage parametrs for specific option in various search engines.

    ...
    Atributes
    ---------
    # SOON...

    """
    engine = models.ForeignKey(SearchEngine, on_delete=models.CASCADE)
    option = models.ForeignKey(SearchOption, on_delete=models.CASCADE)
    parameter_construct = models.CharField(max_length=128)
    extra_tips = models.CharField(max_length=256)

    def __str__(self):
        return f'Invocation of {self.option} for {self.engine}'
