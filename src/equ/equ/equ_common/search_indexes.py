from haystack import indexes
from equ_common.models import Article, Category

class SearchArticle(indexes.SearchIndex, indexes.Indexable):
    text= indexes.CharField(document=True, use_template=True)
    name_art = indexes.CharField(model_attr='name')
    content = indexes.CharField(model_attr='description')
    category = indexes.MultiValueField(indexed=True, stored=True)

    def get_model(self):
        return Article

    """
    This function describes the search in the model Article
    """
    def index_queryset(self, using=None):
        return self.get_model().objects.all() 
"""
class SearchCategory(indexes.SearchIndex, indexes.Indexable):
    text= indexes.CharField(document=True, use_template=True)
    name_cat = indexes.CharField(model_attr='name_category')

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(name_category=self.)
"""
