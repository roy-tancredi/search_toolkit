from django.db import models


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

    """

    name = models.CharField(max_length=30)
    get_url = models.CharField(max_length=50)
    icon_path = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SearchOption(models.Model):
    descriptor = models.CharField(max_length=50)
    ascriptors = models.CharField(max_length=200)
    engine = models.ManyToManyField(SearchEngine)

    def __str__(self):
        return self.descriptor

# class SearchOptionValue(models.Model):
