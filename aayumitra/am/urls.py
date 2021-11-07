from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url


urlpatterns = [

    path("",views.index , name = "index"),

    path("consolt_view/<int:consolt_id>", views.consolt_view , name = "consolt_view"),

    path("d_login", views.d_login, name="d_login"),

    path("d_dashboard/<int:d_id>" , views.d_dashboard , name = "d_dashboard"),

    path("Appointment_record/<int:d_id>", views.Appointment_record, name="appointment_record"),

    path("case_confirm/<int:id><int:d_id>", views.case_confirm , name= "case_confirm"),

    path("d_search.html", views.search , name = "/d_search.html"),

    path("consolt_page.html", views.consolt_page , name = "consolt"),

    path("left-sidebar.html", views.left_sidebar , name = "leftsidebar"),

    path("right-sidebar.html", views.right_sidebar , name = "rightsidebar"),

    path("contactus.html", views.contact , name = "/contactus.html"),

    path("user_sign_up.html", views.user_sign_up , name = "/user_sign_up.html"),

    path("user_login", views.user_login, name="/user_login.html"),

    path("user_logout.html", views.user_logout, name="/user_logout.html"),

]
