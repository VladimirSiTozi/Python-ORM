from django.urls import path, include

from MusicApp.musics import views

urlpatterns = [
    path('', views.index, name='index'),
    path('song/', include([
        path('create/', views.create_song, name='create song'),
        path('serve-song/<int:pk>/', views.serve_song, name='serve song'),
        path('play-song/<int:pk>/', views.play_song, name='play song')
    ])),
    path('album/', include([
        path('create/', views.create_album, name='create album'),
        path('details/<int:pk>/', views.album_details, name='details album'),
        path('edit/<int:pk>/', views.edit_album, name='edit album'),
        path('delete/<int:pk>', views.delete_album, name='delete album')
    ]))
]