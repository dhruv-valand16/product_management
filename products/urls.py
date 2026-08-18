from django.urls import path,include
from . import views 


urlpatterns = [
    path("",views.product_list , name = "product_list"),
    path("<int:id>/",views.product_detail,name = "product_detail"),
    path("create/",views.product_create,name="product_create"),
    path("<int:id>/edit/",views.product_edit,name="product_edit"),
    path("<int:id>/delete/",views.product_delete,name="product_delete"),
    path("export/",views.export_products,name = "export_products"),

    
]


