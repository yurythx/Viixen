from django.urls import path
from .views.home import HomeView
from .views.detail import PageDetailView
from .views.crud import PageListView, PageCreateView, PageUpdateView, PageDeleteView

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', HomeView.as_view(template_name='pages/about.html'), name='about'),
    
    # Page CRUD
    path('manage/', PageListView.as_view(), name='page_list'),
    path('manage/create/', PageCreateView.as_view(), name='page_create'),
    path('manage/<int:pk>/edit/', PageUpdateView.as_view(), name='page_update'),
    path('manage/<int:pk>/delete/', PageDeleteView.as_view(), name='page_delete'),
    
    # Page detail (public view)
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]