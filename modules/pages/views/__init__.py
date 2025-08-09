from .home import HomeView
from .detail import PageDetailView
from .crud import PageListView, PageCreateView, PageUpdateView, PageDeleteView

__all__ = [
    'HomeView', 'PageDetailView', 
    'PageListView', 'PageCreateView', 'PageUpdateView', 'PageDeleteView'
]