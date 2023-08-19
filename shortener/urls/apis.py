from datetime import timedelta

from django.http.response import Http404
from django.core.cache import cache
from django.db.models.aggregates import Count


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, action
from rest_framework.renderers import JSONRenderer

from shortener.models import ShortenedUrls, Statistic
from shortener.utils import MsgOk, url_count_changer, get_kst
from shortener.urls.serializers import UrlListSerializer, UrlCreateSerializer, BrowserStatSerializer


class UrlListView(viewsets.ModelViewSet):
    queryset = ShortenedUrls.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = UrlCreateSerializer(data=request.data)

        if serializer.is_valid():
            cache.delete(f"url_lists_{request.users_id}")
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)
        pass

    def retrieve(self, request, pk=None):
        # Detail GET
        queryset = self.get_queryset().filter(pk=pk).first()
        serializer = UrlListSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # PUT METHOD
        pass

    def partial_update(self, request, pk=None):
        # PATCH METHOD
        pass

    @renderer_classes([JSONRenderer])
    def destroy(self, request, pk=None):
        # DELETE METHOD

        queryset = (
            self.get_queryset().filter(pk=pk, creator_id=request.users_id)
            if not request.user.is_superuser
            else self.get_queryset().filter(pk=pk)
        )

        if not queryset.exists():
            raise Http404

        queryset.delete()
        cache.delete(f"url_lists_{request.users_id}")
        url_count_changer(request, False)

        return MsgOk()

    def list(self, request):
        # GET ALL
        queryset = self.get_queryset().filter(creator_id=request.users_id).all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def add_browser_today(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id).first()
        new_history = Statistic()
        new_history.record(request, queryset, {})

        return MsgOk()

    @action(detail=True, methods=["get"])
    def get_browser_stats(self, request, pk=None):
        queryset = Statistic.objects.filter(
            shortened_url_id=pk,
            shortened_url__creator_id=request.user.id,
            created_at__gte=get_kst() - timedelta(days=14),
        )

        if not queryset.exists():
            raise Http404

        # browers = (
        #     queryset.values("web_browser", "created_at__date")
        #     .annotate(count=Count("id"))
        #     .values("count", "web_browser", "created_at__date")
        #     .order_by("-created_at__date")
        # )

        browers = (
            queryset.values("web_browser")
            .annotate(count=Count("id"))
            .values("count", "web_browser")
            .order_by("-count")
        )

        serializer = BrowserStatSerializer(browers, many=True)
        return Response(serializer.data)
