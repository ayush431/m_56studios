from rest_framework import pagination

class SetPagination(pagination.PageNumberPagination):
    page_size = 20