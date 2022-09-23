from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router, File
from ninja.files import UploadedFile

from petappbackend.utils import status
from petappbackend.utils.permissions import AuthBearer
from petappbackend.utils.schemas import MessageOut
from petappbackend.utils.utils import response
from ecommerce.models import Category, Images, Product, Article
from ecommerce.schema import *

User = get_user_model()

category_controller = Router(tags=['Categories'])
product_image_controller = Router(tags=['Product images'])
item_controller = Router(tags=['Items'])
article_controller = Router(tags=['Articles'])


@category_controller.get('all', response={
    200: List[CategoryData],
    404: MessageOut
})
def get_categories(request):
    category_qs = Category.objects.filter(is_active=True).filter(parent=None)
    if category_qs:
        return 200, category_qs
    return 404, {'message': 'no categories found'}


@category_controller.get('{pk}', response={
    200: List[CategoryData],
    404: MessageOut
})
def retrieve_category(request, pk: UUID4):
    category_qs = Category.objects.filter(is_active=True, id=pk).filter(parent=None)
    if category_qs:
        return 200, category_qs
    return 404, {'message': 'no categories found'}


@category_controller.get('{pk}/products', response={
    200: ProductDataOut,
    404: MessageOut
})
def category_products(request, pk: UUID4, per_page: int = 12, page: int = 1):
    if pk is None:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'No category specified'})
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Category does not exist'})
    products = (
        Product.objects.filter(category__in=category.get_descendants(include_self=True))
        .select_related('category')
    )

    return response(status.HTTP_200_OK, products, paginated=True, per_page=per_page, page=page)

@article_controller.get('all', response={
    200: List[ArticleData],
    404: MessageOut
})
def get_articles(request):
    article_qs = Article.objects.filter(is_active=True)
    if article_qs:
        return 200, article_qs
    return 404, {'message': 'no articles found'}


@article_controller.get('{pk}', response={
    200: ArticleData,
    404: MessageOut
})
def retrieve_article(request, pk: UUID4):
    article_qs = Article.objects.get(is_active=True, id=pk)
    if article_qs:
        return response(status.HTTP_200_OK, article_qs)
    return 404, {'message': 'no article found'}


