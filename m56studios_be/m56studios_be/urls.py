"""questionset_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, register_converter
from datetime import datetime
from app.users.views import UserView, LoginView
from app.question.views import QuestionView, BulkQuestionView
from app.comments.views import CommentsView
from app.file_upload.views import UploadFileView
from app.get_images.views import GetImagesView
from app.aws_creds.views import GetAWSCredsView
from app.manager.views import ManagerView, EditorView, CategoryView, FlaggedQuestionsView
from app.super_admin.views import SuperAdminView
from app.export_question.views import ExportQuestionView
from app.generate_thumbnail.views import GenerateThumbnailView

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', UserView.as_view()),
    path('api/user/<slug:user_id>', UserView.as_view()),
    path('api/user/login/', LoginView.as_view()),
    path('api/question' + '/', QuestionView.as_view()),
    path('api/question' + '/' + 'bulk_operation' + '/', BulkQuestionView.as_view()),
    path('api/question' + '/' + '<slug:qn_id>' + '/', QuestionView.as_view()),
    path('api/question' + '/' + '<slug:qn_id>' + '/' + 'comment' + '/', CommentsView.as_view()),
    path('api/file/<slug:vendor_id>/<slug:vendor_name>', UploadFileView.as_view()),
    path('api/get_images/', GetImagesView.as_view()),
    path('api/aws_creds/', GetAWSCredsView.as_view()),
    path('api/manager/', ManagerView.as_view()),
    path('api/editor_data/', EditorView.as_view()),
    path('api/flagged_ques_data/', FlaggedQuestionsView.as_view()),
    path('api/category_view/', CategoryView.as_view()),
    path('api/export_question/', ExportQuestionView.as_view()),
    path('api/publish_question/', SuperAdminView.as_view()),
    path('api/generate_thumbnail/', GenerateThumbnailView.as_view()),

]
