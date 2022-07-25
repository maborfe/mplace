from multiprocessing import parent_process

import algoliasearch_django as algoliasearch
from django.contrib import messages
from django.contrib.messages import constants
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from portal.forms import ProductAnswerForm, ProductForms, ProductQuestionForm

from .models import Category, Product, ProductAnswer, ProductQuestion


################################################################################################
#                                          HOME
################################################################################################
def home(request):
    return render(request, 'portal/home.html', )


################################################################################################
#                                          LISTAR ANÚNCIO
################################################################################################
def productList(request):
    # products = Product.objects.filter(user=request.user).filter(status='Active').order_by('-id')
    products = Product.objects.filter(user=request.user).order_by('-id')
    context = {
        'products': products
    }

    return render(request, 'portal/product_list.html', context)


################################################################################################
#                                          LISTAR PERGUNTAS
################################################################################################
def question_list(request, id_anuncio):
    
    #lista para retornar para o template
    question_without_answer = list()

    #armazena o produto do id selecionado na lista
    produto = get_object_or_404(Product,pk=id_anuncio)

    #busca todas as questões daquele produto, desta maneira abaixo, já conseguimos diretamente com um unico
    #comando, trazer todas as ProductQuestion que não tem um registro de resposta, isso funciona pq o django
    #entende que ProductAnswer tem um relacionamento com ProductQuestion, então podemos utlizar o comando productanswer__isnull
    # poderiamos fazer isso diretamente em uma funcao na classe de Produtos, pois este tem um relacionamento com ProductQuestion e este
    # tem um relacionamento com ProductAnswer, criando ela e decorando como uma propriedade, e utilizando diretamente no html
    #economizando esta função aqui nesta view, com praticamente 2 linhas de codigo como no exemplo abaixo.
    #@property
    #def questions_no_answer(self):
    #   return self.productquestion_set.filter(xxxxx, productanswer__isnull= True)
    #pq = ProductQuestion.objects.filter(product = produto, productanswer__isnull = True)
    
    
    #busca todas as questões daquele produto
    #desta forma estamos buscando mais manualmente se temos respostas para cada pergunta, e adicionando as perguntas sem resposta
    #na lista que foi retornada para o template
    pq = ProductQuestion.objects.filter(product = produto)

    for question in pq:
        ps = ProductAnswer.objects.filter(product_question=question)
        if len(ps) == 0:
            question_without_answer.append(question)

    context = {
        'product': produto,
        'questions': question_without_answer
    }

    return render(request, 'portal/question_list.html', context)


################################################################################################
#                                          CADASTRAR ANÚNCIO
################################################################################################
def addProduct(request):
    if request.method == 'POST':
        form = ProductForms(request.POST)
        if form.is_valid():
            product = Product()
            product.user = request.user
            product.name = form.cleaned_data['name']
            product.slug = form.cleaned_data['name']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.short_description = form.cleaned_data['short_description']
            product.description = form.cleaned_data['description']
            product.status = form.cleaned_data['status']
            product.save()

            # tratamento campo slug posterior a geração do ID do produto.
            product.slug = '%s-%i' % (slugify(product.name), product.id)

            # tratamento campo categoria para adicionar cada ocorrencia
            categories = Category.objects.filter(id__in=request.POST.getlist('categories'))

            if categories:
                for category in categories:
                    product.categories.add(category)
            product.save()

            messages.add_message(request, constants.SUCCESS, 'Anúncio cadastrado com sucesso!')

            return redirect('products')

    else:
        categories = Category.objects.all()
        form = ProductForms()
        context = {'form': form,
                   'categories': categories}
        return render(request, 'portal/AddProduct.html', context)


################################################################################################
#                                          EDITAR
################################################################################################
def editProduct(request, id_anuncio):
    produto = get_object_or_404(Product, pk=id_anuncio)

    if produto.user != request.user:
        return HttpResponseForbidden

    if request.method == 'POST':

        form = ProductForms(request.POST)

        if form.is_valid():
            produto.name = form.cleaned_data['name']
            produto.quantity = form.cleaned_data['quantity']
            produto.price = form.cleaned_data['price']
            produto.short_description = form.cleaned_data['short_description']
            produto.description = form.cleaned_data['description']
            produto.categories.set(form.cleaned_data['categories'])
            produto.status = form.cleaned_data['status']
            produto.slug = produto.slug = '%s-%i' % (slugify(produto.name), produto.id)

            produto.save()
            messages.add_message(request, constants.SUCCESS, 'Alteração efetuada com sucesso!')
            return redirect('products')

    form = ProductForms(instance=produto)

    context = {
        'product': produto,
        'form': form
    }

    return render(request, 'portal/EditProduct.html', context)


################################################################################################
#                                          DESATIVAR
################################################################################################
def desativar(request, id_anuncio):
    produto = get_object_or_404(Product, pk=id_anuncio)
    produto.status = 'Inactive'
    produto.save()

    messages.add_message(request, constants.SUCCESS, 'Anúncio Desativado!')

    return redirect('products')


################################################################################################
#                                          ATIVAR
################################################################################################
def ativar(request, id_anuncio):
    produto = get_object_or_404(Product, pk=id_anuncio)
    produto.status = 'Active'
    produto.save()

    messages.add_message(request, constants.SUCCESS, 'Anúncio Ativado!')

    return redirect('products')


################################################################################################
#                                          Gravar Questões
################################################################################################
def product_question(request, id_anuncio):
    produto = get_object_or_404(Product, pk=id_anuncio)

    if request.method == 'POST':
        form = ProductQuestionForm(request.POST)
        if form.is_valid():
            question = ProductQuestion()
            question.user = request.user
            question.product = produto
            question.question = form.cleaned_data['question']
            question.status = 'Active'
            question.save()

    return redirect('show', produto.slug)


################################################################################################
#                                          Mostrar Questões
################################################################################################
def show(request, slugid):
    produto = get_object_or_404(Product, slug=slugid)

    questions = ProductQuestion.objects.filter(product=produto)

    form = ProductQuestionForm()

    context = {
        'questions': questions,
        'form': form,
        'product': produto
    }

    return render(request, 'portal/product_show.html', context)



################################################################################################
#                                          RESPONDER PERGUNTA
################################################################################################
def responder(request, id_question):
    form = ProductAnswerForm()
    
    
    question = ProductQuestion.objects.get(id=id_question)

    context = {
        'form': form,
        'question': question,
    }

    if request.method == 'POST':
        form = ProductAnswerForm(request.POST)
        if form.is_valid():
            answer = ProductAnswer()
            answer.user = request.user
            answer.answer = form.cleaned_data['answer']
            answer.product_question = ProductQuestion.objects.get(id=id_question)
            answer.status = 'Active'
            answer.save()
        
        messages.add_message(request, constants.SUCCESS, 'Resposta enviada!')
        return redirect('products')


    return render(request, 'portal/answer_question.html', context)



################################################################################################
#                                          BUSCA / PAGINACAO
################################################################################################
def search(request):
    categories = Category.objects.filter(parent__isnull=True).order_by('name')
    
############################### COM ALGOLIA
    if request.GET.get('busca'):
        qs= request.GET.get('busca')
    else:
        qs = ''

    str_category = request.GET.get('category', '')
    
    page = request.GET.get('page', '0')

    results = None
    next_page = ""
    previous_page = ""
    cat_name = ""
    next_page = int(page) + 1
    previous_page = int(page) -1


    params = {
        'hitsPerPage': 3,
        'page': page,
    }  
    if qs == ' ' or qs =='' or qs==None:
        results = Product.objects.all()
        paginator = Paginator(results, 2)
        page = request.GET.get('page','1')

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(2)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
    else:
        results = algoliasearch.raw_search(Product, qs, params)

############################### COM DJANGO PAGINATOR NO BD    
    if str_category:
        cat = get_object_or_404(Category, slug=str_category)        
        cat_name = cat.name
        results = Product.objects.filter(categories=cat)
        paginator = Paginator(results, 2)
        page = request.GET.get('page','1')

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(2)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'results': results,
        'cat_name': cat_name,
        'str_category': str_category,
        'next_page': next_page,
        'previous_page': previous_page,
    }

    return render(request, 'portal/search_category.html', context)


################################################################################################
#                                          BUSCA / PAGINACAO
################################################################################################
def search_category(request,id):
    categories = Category.objects.filter(parent__isnull=True).order_by('name')  
    cat = get_object_or_404(Category, id=id)        
    results = Product.objects.filter(id=cat.id)
    print(results.query)
    paginator = Paginator(results, 2)
    page = request.GET.get('page',"0")

    next_page = ""
    previous_page = ""

    if page:        
        next_page = int(page) + 1
        previous_page = int(page) -1
    
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(2)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'results': results,
        'next_page': next_page,
        'previous_page': previous_page,
    }

    return render(request, 'portal/search_category.html', context)



################################################################################################
#                                          ADMIN 
################################################################################################
def admin(request):
    return render(request, 'http://127.0.0.1:8000/admin/')
