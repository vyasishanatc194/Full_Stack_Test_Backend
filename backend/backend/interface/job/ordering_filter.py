from rest_framework.filters import OrderingFilter


class JobPostingOrderingFilter(OrderingFilter):
    ordering_param = 'order'
