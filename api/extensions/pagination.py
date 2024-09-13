from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from api.extensions import return_code

class CustomPagination(PageNumberPagination):
    """ 自定义分页 """
    # 默认条数
    page_size = 20
    # 每页上限
    max_page_size = 100
    # 参数名
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        """
        自定义分页响应体
        :param data:
        :return:
        """
        return Response({
            'code':return_code.SUCCESS,
            # 总条数
            'count': self.page.paginator.count,
            'results': data
        })