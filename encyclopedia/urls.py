from django.urls import path

from . import views


""" URL namespaces and included URLconfs, from https://docs.djangoproject.com/en/3.2/topics/http/urls/
Application namespaces of included URLconfs can be specified.
Set an app_name attribute in the included URLconf module, at the same level as the urlpatterns attribute. 
https://youtu.be/w8q0C-C1js4?t=4293 """

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page_entry, name="page_entry"),
    path("searchquery", views.searchquery, name="search_query"),
    path("newpage", views.newpage, name="new_page"),
    path("editpage", views.editpage, name="edit_page"),
    path("editsaved", views.editsaved, name="edit_saved"),
    path("rand", views.rand, name="random"),

]
