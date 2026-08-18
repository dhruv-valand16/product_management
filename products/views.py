from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from .forms import ProductForm
from django.http import HttpResponse
import csv


# Create your views here.
def product_list(request):

    search = request.GET.get("search")

    if search:
        products = Product.objects.filter(name__icontains = search)
    else:
        products = Product.objects.all()

    return render(
        request , "product_list.html" , {'products':products,'search':search}
    )

def product_detail(request,id):
    # product = Product.objects.get(id = id)
    product = get_object_or_404(Product,id = id)

    return render(request , "product_detail.html" , {'product' : product})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()

            return redirect("product_list")
    else:
        form = ProductForm()

    return render(
        request,"product_form.html",{"form":form,
            "page_title": "Add Product",
            "button_text": "Add Product"}
    )


def product_edit(request, id):

    product = get_object_or_404(Product,id=id)

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect("product_detail", id=product.id)

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "page_title": "Edit Product",
            "button_text": "Update Product"
        }
    )


def product_delete(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        product.delete()

        return redirect("product_list")

    return render(
        request,
        "product_delete.html",
        {"product": product}
    )





def export_products(request):

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = 'attachment; filename="products_data.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "ID",
        "Name",
        "Price",
        "Description",
        "Category",
        "Created At",
        "Updated At",
    ])
    search_data = request.GET.get("search")
    products = Product.objects.all()
    print(search_data)
    print(request)
    if search_data:
        print(search_data)
        products = Product.objects.filter(name__icontains=search_data)

    for product in products:

        writer.writerow([
            product.id,
            product.name,
            product.price,
            product.description,
            product.category.name,
            product.created_at,
            product.updated_at,
        ])

    return response