from django.urls import path, include


from cgaforum.views import CategoriesView, SubCategoriesView


urlpatterns = [
    path('cgaforum', CategoriesView.as_view(), name='cgaforum'),
    path('cgaforum/', include([
        path('<slug:slug>', SubCategoriesView.as_view(), name='subcategories'),
        path('<slug:slug>/', include([
            # path('<slug:slug>', ,name=''),
        ])),
    ]))
]
