from django.urls import path, include


from cgaforum.views import CategoriesView, SubCategoriesView, TopicsView


urlpatterns = [
    path('cgaforum', CategoriesView.as_view(), name='cgaforum'),
    path('cgaforum/', include([
        path('<slug:category_slug>', SubCategoriesView.as_view(), name='subcategories'),
        path('<slug:category_slug>/', include([
            path('<slug:subcategory_slug>', TopicsView.as_view(), name='topics'),
        ])),
    ]))
]
