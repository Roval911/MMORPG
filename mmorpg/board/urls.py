from django.urls import path
from .views import *

urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('createpost', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('post/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('mycoments/', ComentList.as_view(), name='mycoments'),
   path('post/coment_sent_for_approval', ComentForApproval.as_view(), name='coment_sent_for_approval'),
]