from django.urls import path, include


from cga_case.views import CaseCategoriesView, CaseSectionsView, CaseDetailView

urlpatterns = [
    path('cgacase', CaseCategoriesView.as_view(), name='cgacase'),
    path('cgacase/', include([
        path('<str:category_name>', CaseSectionsView.as_view(), name='case_sections'),
        path('detail/', include([
            path('<str:case_title>', CaseDetailView.as_view(), name='case_detail')
        ])),
    ])),
]
