# -*- encoding: utf-8 -*-
"""
# Copyright (C) 2020 Besity AS - All Rights Reserved
#
#
# This file is part of the Besity Platform SaaS codebase.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Heuristica Sarl

__author__ = "Heuristica Sarl"
__author_website__ = "https://heuristica.ch"
__copyright__ = "Copyright (C) 2020 Besity AS"
__copyright_website__ = "https://besity.no"
__license__ = "Custom - Themesberg - Enterprise - SaaS"
__version__ = "1.0"
__maintainer__ = "Heuristica Sarl"
__maintainer_website__ = "https://heuristica.ch"
"""

# from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.urls import path, re_path
from django.conf import settings

from payment import views
from django.contrib.auth import logout as auth_logout


# Custom logout function that cleans up the session cookie.
# This is now necessary to protect media files from being accessed by anoynmous users
# NOTE: NGINX controls the cookie presence to filter requests toward the media folder
def logout_user(request):
    auth_logout(request)
    response = redirect("login")
    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return response


urlpatterns = [
    # General links
    path('', views.display_payment_form, name="display_payment_form"),
    path(
        "init-payment",
        views.init_payment,
        name="init_payment",
    ),
    path(
        "init-payment-card",
        views.init_payment_card,
        name="init_payment_card",
    ),
    path(
        "get-status",
        views.get_transaction_status,
        name="get_status",
    ),
]
