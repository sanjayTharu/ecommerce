from django.shortcuts import render,get_object_or_404,redirect
from .models import Variation,Products,ReviewRating,ProductGallery
from category.models import Category
from cart.models import CartItem,Cart
from cart.views import _get_session
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q,Sum,Avg,Count,Max,Min
from django.contrib import messages
from orders.models import OrderProduct
# Create your views here.

def store(request,product_item=None):
    if product_item!=None:
        categories=get_object_or_404(Category,slug=product_item)
        products=Products.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        page_product=paginator.get_page(page)
        count=products.count()
    
    return render(request,'store/store.html',context={'products':page_product,'count':count})

def single_products_item(request,product_item,single_item):
    cart_in=None

    product=get_object_or_404(Products,slug=single_item)
    colors=Variation.objects.filter(product=product,variation_category='color')
    sizes=Variation.objects.filter(product=product,variation_category='size')
    try:
        items=Products.objects.get(category__slug=product_item,slug=single_item)
        cart=Cart.objects.get(card_id=_get_session(request))
        cart_in=CartItem.objects.get(product=items,cart=cart)

    except:
        pass

    try:
        orderProduct=OrderProduct.objects.filter(user=request.user,product_id=items.id).exists()
    except:
        orderProduct=None

    reviews=ReviewRating.objects.filter(product_id=items.id,status=True)

    avg=0
    count=0
    average_rating=ReviewRating.objects.filter(productid=items.id,status=True).aggregate(average=Avg('rating'))
    count_rating=ReviewRating.objects.filter(product_id=items.id,status=True).aggregate(counter=Count('id'))

    if average_rating['average'] is not None:
        avg=average_rating['average']

    if count_rating['counter'] is not None:
        count=count_rating['counter']

    productGallery=ProductGallery.objects.filter(product_id=items.id)
    return render(request,'store/single_prooduct.html',context={'items':items,'cart_in':cart_in,'colors':colors,'sizes':sizes,'orderProduct':orderProduct,'reviews':reviews,'count':count,'avg':avg,'productGallery':productGallery})



def search(request):
    count=0
    products=None
    if 'search' in request.GET:
        q=request.GET['search']
        if q:
            products=Products.objects.filter(Q(product_name__icontains=q))
            count=products.count()

    return render(request,'store/store.html',context={'products':products,'count':count})

def review(request,product_id):
    print(request.POST)

    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        rating_star=request.POST.get('rate')
        review_title=request.POST['review_title']
        review_box=request.POST['review_box']


        try:
            reviewRating=ReviewRating.objects.get(product__id=product_id,user=request.user)

            #update the review rating object

            reviewRating.rating=rating_star
            reviewRating.subject=review_title
            reviewRating.review=review_box
            reviewRating.ip=request.META['REMOTE_ADDR']
            reviewRating.user=request.user
            reviewRating.product_id=product_id
            reviewRating.save()
            messages.success(request,"Your Review has been updated")
        except ReviewRating.DoesNotExist:

            reviewRating=ReviewRating.objects.create(product_id=product_id,user=request.user,rating=rating_star,subject=review_title,review=review_box,ip=request.META['REMOTE_ADDR'])
            messages.success(request,'Your Review has been saved')

    return redirect(url)
