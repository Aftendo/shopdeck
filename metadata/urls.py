from django.urls import path

from . import views

urlpatterns = [
    path('news', views.news, name='news'),
    path('telops', views.telops, name="telops"),
    path('languages', views.language, name="language"),
    path('eshop_message/about', views.eshop_message, name="about"),
    path('eshop_message/agreement_send_info', views.agreement_send_info, name="agreementuseless"),
    path('directories', views.directories, name="directories"),
    path('directory/<int:cid>', views.directory, name="categoryview"),
    path('title/<int:tid>', views.title, name="titleview"),
    path('movie/<int:mid>', views.viewmovie, name="movie"),
    path('searchcategory', views.searchcategory, name="searchcategory"),
    path('genres', views.genres, name="genres"),
    path('publishers', views.publishers, name="publishers"),
    path('contents', views.contents, name="contents"),
    path('titles', views.titles, name="titles"),
    path('movies', views.movies_content, name="movies"),
    path('rankings', views.rankings, name="rankings"),
    path('ranking/<int:rid>', views.ranking, name="ranking")
]