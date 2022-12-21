from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from . models import Product,Contact,Order,OrderUpdate
import json 
# Create your views here.
def index(request):
    products = Product.objects.all()
    allprod=[]
    catprod = Product.objects.values('category','id')
    cat = {item['category'] for item in catprod}
    #print(products)
    print(cat)
    for i in cat:
        prod = Product.objects.filter(category=i)
        allprod.append(prod)
    print(allprod)
    params={'allprod':allprod}
    return render(request, 'shop/index.html',params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    #return HttpResponse('we are at contact page')
    if request.method == 'POST':
        print(request)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        print(name,email,phone,desc)
        contact = Contact(name=name,email=email,phone=phone,msg_desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def product(request,prodid):
    product = Product.objects.filter(id=prodid)
    params={'product':product[0]}
    print(product)
    return render(request, 'shop/productview.html',params)

def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('order','')
        email = request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for items in update:
                    updates.append({'text':items.update_desc, 'time':items.timestamp})
                    response = json.dumps(updates,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('else')
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'shop/tracker.html')

def checkout(request):
    if request.method == 'POST':
        item_Json = request.POST.get('itemJson')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address1') + ' ' + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')
        order = Order(items_json=item_Json,name=name, email=email, address=address, city=city,state=state, zip=zip, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="Your order has been placed.")
        update.save()
        thank = True
        id = Order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')