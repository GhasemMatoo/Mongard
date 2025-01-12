from django.urls import path, re_path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', views.BucketHomeView.as_view(), name='bucket'),
    path('upload/', views.UploadBuketObjectView.as_view(), name='bucketUpload'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

bucket_urls = [
    re_path(r'^delete/(?P<key>.+)/$', views.DeleteBucketObjectView.as_view(), name='bucketDelete'),
    re_path(r'^download/(?P<key>.+)/$', views.DownloadBucketObjectView.as_view(), name='bucketDownload'),
]

urlpatterns += bucket_urls
