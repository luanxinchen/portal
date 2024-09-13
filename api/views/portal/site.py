from rest_framework import serializers, filters
from api.models import Site, SiteCategory
from api.extensions import permission, pagination
from api.extensions import viewsets


class SiteSerializer(serializers.ModelSerializer):
    category_cn = serializers.ReadOnlyField(source='category.title')
    maintainer_cn = serializers.ReadOnlyField(source='maintainer.username')

    class Meta:
        model = Site
        fields = '__all__'


class SiteCategorySerializer(serializers.ModelSerializer):
    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = SiteCategory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sites = representation.get('sites', [])

        # 过滤掉 is_active 为 False 的站点
        filtered_sites = [site for site in sites if site.get('is_active', True)]

        # 对剩余的站点按照 sort 进行排序
        sorted_sites = sorted(filtered_sites, key=lambda site: site.get('sort', 0))

        representation['sites'] = sorted_sites
        return representation


class SiteCateGoryViewSet(viewsets.SafeMethodNoAuthViewset):
    queryset = SiteCategory.objects.all().order_by('sort').prefetch_related('sites')
    serializer_class = SiteCategorySerializer
    permission_classes = [permission.SuperUserEditAndGuestReadOnly, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'sort']


class SiteFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_query = request.query_params.get("category_id")
        is_active = request.query_params.get("is_active")
        if category_query:
            queryset = queryset.filter(category=category_query)
        if is_active:
            queryset = queryset.filter(is_active=is_active)
        return queryset


class SiteViewSet(viewsets.SafeMethodNoAuthViewset):
    queryset = Site.objects.all().order_by('id')
    serializer_class = SiteSerializer
    permission_classes = [permission.SuperUserEditAndGuestReadOnly, ]
    filter_backends = [SiteFilter, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'url', 'description', 'maintainer', 'tips']
    ordering_fields = ['title', 'category', 'sort', 'is_active']
