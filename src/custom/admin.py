from django.contrib import admin
from django.urls import path, include, re_path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from users.admin import hidden_admin
from django.conf import settings
from django.conf.urls.static import static
from games.views import game_loader
from django.contrib.auth import views as auth_views
from payments import views as paymentsViews
from django.views.static import serve
from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from app.cron import send_report_mail
from django.http import HttpResponse, HttpResponseRedirect

class CustomAdmin(admin.AdminSite):
    index_template = "admin/custom_index.html"

    def reportPage(self, request):
        # (email, num_creat_today, num_login_today, today, yesterday, userHistory, paymentHistory) = send_report_mail()
        # print(email,num_creat_today,num_login_today )
        report_context = send_report_mail(False)
        context = {
            "text": "None",
            "page_name": "Report Page",
            "app_list": self.get_app_list(request),
            **self.each_context(request),
            "num_creat_today": report_context['num_creat_today'],
            "num_login_today": report_context['num_login_today'],
            "today": report_context['today'],
            "yesterday":report_context['yesterday'],
            "userHistories": report_context['userHistories'],
            "paymentHistories": report_context['paymentHistories']
        }
        # return TemplateResponse(request, "admin/custom_page.html", context)
        return TemplateResponse(request, "admin/report_admin.html", context)

        # return HttpResponse(send_report_mail())
    def sendReportPage(self, request):
        
        report_context = send_report_mail(True)
        context = {
            "text": "None",
            "page_name": "Sent Report",
            "app_list": self.get_app_list(request),
            **self.each_context(request),
            "num_creat_today": report_context['num_creat_today'],
            "num_login_today": report_context['num_login_today'],
            "today": report_context['today'],
            "yesterday":report_context['yesterday'],
            "userHistories": report_context['userHistories'],
            "paymentHistories": report_context['paymentHistories'],
            "success": report_context['success'],
            "messages":report_context['message']
        }
        return TemplateResponse(request, "admin/report_admin.html", context)
       
    def get_urls(
        self,
    ):
        return [
            path(
                "report/",
                self.admin_view(self.reportPage),
                name="report",
            ),
            path(
                "report/send",
                self.admin_view(self.sendReportPage),
                name="sent Report",
            ),
        ] + super().get_urls()