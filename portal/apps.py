from pyexpat import model
from django.apps import AppConfig
from algoliasearch_django import AlgoliaIndex
import algoliasearch_django as algoliasearch

class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'

# esta função é executada toda vez que a aplicação fica online
# Aqui estamos mandando buscar dentro dos nossos models o model Product e atribuir na variavel de mesmo nome
# e depois estamos registrando no algolia o nosso model junto com o ProductIndex que são as configurações do nosso index. 
# Associando assim de qual model é o index que estamos criando e registrando, e os campos que iremos utilizar.

# para que isso aconteça precisamos registrar em nosso arquivo __init__.py que está na pasta principal do projeto
# as configurações padrões que devem subir junto com a aplicação. (default_app_config = 'portal.apps.PortalConfig')
    def ready(self):
        Product = self.get_model('Product')
        algoliasearch.register(Product,ProductIndex)

class ProductIndex(AlgoliaIndex):
    fields = ('id', 'name', 'short_description', 'description', 'slug', 'price')
    settings = {'searchableAttributes': [ 'name', 'description']}
    index_name = 'product_index'