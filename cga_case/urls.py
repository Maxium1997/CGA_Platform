from django.urls import path, include


from cga_case.views import CaseCategoriesView, CaseSectionsView, CaseDetailView, \
    CaseCreateView, CaseUpdateView, CaseLRUpdateView

urlpatterns = [
    path('cgacase', CaseCategoriesView.as_view(), name='cgacase'),
    path('cgacase/', include([
        path('<str:case_category_name>', CaseSectionsView.as_view(), name='case_sections'),
        path('<str:case_title>/', include([
            path('detail', CaseDetailView.as_view(), name='case_detail'),
            path('update', CaseUpdateView.as_view(), name='case_update'),
            path('update/', include([
                path('lr', CaseLRUpdateView.as_view(), name='case_lr_update')
            ])),
        ])),
        path('<str:case_section_name>/', include([
            path('new-case', CaseCreateView.as_view(), name='case_create'),
        ]))
    ])),
]
