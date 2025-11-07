from django.urls import path

from export_part.views import DownloadFileView

urlpatterns = [
    path('<str:key>/<str:file_type>/', DownloadFileView.as_view(), name='download_file')
]
