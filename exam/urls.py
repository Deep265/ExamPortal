from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'exam'

urlpatterns = [
    path('list/',views.ExamListView.as_view(),name='exam_list'),
    path('detail/<int:pk>/',views.ExamDetailView.as_view(),name='exam_detail'),
    path('new/',views.ExamCreateView,name='add_question'),
    path('',views.ExamPage.as_view(),name='exam_page'),
    path('detail/',views.ExamTarget.as_view(),name='exam_target'),
    path('index/',views.IndexView,name='index'),
    path('test/',views.NewTest,name='Test'),
    path('testlist/',views.TestListView.as_view(),name='test_list'),
    path('testdetail/<slug:slug>/<int:pk>/',views.TestDetailView.as_view(),name='test_detail'),
    path('testdelete/<int:pk>/',views.TestDeleteView.as_view(),name='test_delete'),
    path('testqusetiond/<int:pk>/',views.TestQuestionDelete,name='test_q_delete'),
    path('test/index/',views.TestIndex,name='test_index'),
    path('questions/list/',views.AllQuestions,name='question'),
    path('test/math/',views.NewMathsTest,name='maths_test'),
    path('test/physics/',views.NewPhysicsTest,name='physics_test'),
    path('test/chemistry/',views.NewChemistryTest,name='chemistry_test'),
    # Questions URL's
    path('test/maths/question/',views.question_maths,name='maths_question'),
    path('test/chemistry/question/',views.question_chemistry,name='chemistry_question'),
    path('test/physics/question/',views.question_physics,name='physics_question'),
    path('test/<int:pk>/question/',views.add_new_question_detail,name='add_question_detail'),
    # Student Register
    path('test/student/<int:pk>/',views.register,name='register'),
    path('test/student/list/',views.register_list,name='student_register'),
    path('test/student/11th/<int:pk>/',views.add_all_11th,name='add_11th'),
    # Endtest
    path('test/<int:pk>/end/',views.Endtest,name='end_test'),
]

