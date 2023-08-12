from django.shortcuts import render
from django.db.models.query import Prefetch
from django.contrib.auth.decorators import login_required

from shortener.models import ShortenedUrls
from shortener.urls.decorators import admin_only


@login_required
@admin_only
def url_list(request):
    urls = (
        ShortenedUrls.objects.order_by("-id")
        .prefetch_related(
            Prefetch("creator"),
            Prefetch("creator__user"),
            Prefetch("creator__organization"),
            Prefetch("creator__organization__pay_plan"),
            Prefetch("statistic_set"),
        ).all()
    )
    context = {"urls": urls}
    return render(request, "admin_url_list.html", context)
