from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'hasker_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('order_by/<str:orderby>', views.IndexView.as_view(), name='index'),
    path('new/', views.AskQuestionView.as_view(), name='ask'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('vote_up_<str:object_type>_<int:obj_id>/', views.vote, {'vote_up': True}, name='vote_up'),
    path('vote_down_<str:object_type>_<int:obj_id>/', views.vote, {'vote_up': False}, name='vote_down'),
    path('mark_<int:answer_id>_correct_for_<int:question_id>/', views.mark_correct_answer, name='correct_answer'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='hasker_app:index'), name='logout'),
    path('settings/', views.ChangeProfileView.as_view(), name='settings'),
]
