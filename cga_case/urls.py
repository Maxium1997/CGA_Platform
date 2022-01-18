from django.urls import path, include


from cga_case.views import CaseCategoriesView, CaseSectionsView

urlpatterns = [
    path('cgacase', CaseCategoriesView.as_view(), name='cgacase'),
    path('<str:category_name>', CaseSectionsView.as_view(), name='case_sections'),
]