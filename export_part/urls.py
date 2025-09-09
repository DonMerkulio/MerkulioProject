from django.urls import path

from export_part.views import DownloadFileView, DownloadFileDromView

urlpatterns = [
    path('<str:key>/<str:file_type>/', DownloadFileView.as_view(), name='download_file'),
    path('drom/<str:key>/<str:file_type>/', DownloadFileDromView.as_view(), name='download_file_drom')
]
