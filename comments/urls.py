from rest_framework.urls import path
from . import views

urlpatterns = [
    path("<int:pk>", views.CommentDetail.as_view()),
    # path("<int:comment_pk>/recomments/<int:recomment_pk>", views.Recomments.as_view()),
    path("recomments/<int:recomment_pk>", views.DeleteRecomment.as_view()),
]
