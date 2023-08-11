from rest_framework.pagination import PageNumberPagination


class PageNumberCustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
