from tabnanny import verbose

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import path, reverse

STATUS_CHOICES= (
  ('Active', 'Active'),
  ('Inactive', 'Inactive'),
)


#***************************************************************#
#********************** TABELA CATEGORIA ***********************#
#***************************************************************#
class Category(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)
  order = models.IntegerField(null=True, blank=True)
  hidden = models.BooleanField(default=False)
  parent = models.ForeignKey('Category', blank=True, null=True,related_name='cat_child', on_delete=models.DO_NOTHING)

  class Meta:
    verbose_name_plural = ('Categories')
    ordering = ('name',)


  def __str__(self):
    return self.name


#***************************************************************#
#********************** TABELA PRODUTOS ************************#
#***************************************************************#
class Product(models.Model):
  name = models.CharField(max_length=150)
  slug = models.SlugField(unique=True)
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  categories = models.ManyToManyField(Category, blank=True, related_name='categories')
  quantity = models.IntegerField(default=1)
  price = models.DecimalField(max_digits=8, decimal_places=2)
  short_description = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Inactive')

  class Meta:
    verbose_name_plural = 'Products'
    ordering = ('name',)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('show', kwargs={'slugid': self.slug})

  @property
  def questions_without_answers(self):
    qtd =  self.productquestion_set.filter(productanswer__isnull=True).count()
    return qtd




#***************************************************************#
#********************** PERGUNTAS DE PRODUTOS ******************#
#***************************************************************#
class ProductQuestion(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
  question = models.TextField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Inactive')

  class Meta:
    verbose_name_plural = 'Product Questions'

  @property
  def get_answers(self):
    return self.productanswer_set.all()

  def __str__(self):
    return self.question



#***************************************************************#
#********************** RESPOSTAS  DE PRODUTOS ******************#
#***************************************************************#
class ProductAnswer(models.Model):
  user =models.ForeignKey(User, on_delete=models.DO_NOTHING)
  product_question = models.ForeignKey(ProductQuestion, on_delete=models.DO_NOTHING)
  answer = models.TextField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Inactive')

  class Meta:
    verbose_name_plural = 'ProductAnswers'

  def __str__(self):
    return self.answer
