import logging

import pandas as pd
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema_view
from pymongo import MongoClient
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.application.job.services import JobPostingAppServices
from backend.interface.job import open_api
from backend.interface.job.ordering_filter import JobPostingOrderingFilter
from utils.django.middleware import AuthMiddleWare
from utils.errors.custom_response import CustomResponse

from .serializers import BulkJobPostingSerializer, ListOfJobPostingSerializer

# Logger setup
logger = logging.getLogger("django")


@extend_schema_view(
    list_of_job_posting=open_api.job_listing_extension,
    bulk_job_posting=open_api.bulk_job_posting_extension
)
class JobPostingViewSet(viewsets.ViewSet):
    """
    This ViewSet consist of Job Posting Action.
    """
    authentication_class = [JWTAuthentication]
    job_posting_app_services = JobPostingAppServices()
    filter_backends = [
        JobPostingOrderingFilter
    ]
    filterset_fields = [
        "job_title",
    ]
    search_fields = [
        "job_title",
    ]
    client = MongoClient(settings.DB_HOST)
    db = client[settings.DB_NAME]
    job_collection = db['job_jobposting']

    def get_serializer_class(self):
        if self.action == "bulk_job_posting":
            return BulkJobPostingSerializer
        if self.action == "list_of_job_posting":
            return ListOfJobPostingSerializer

    def get_queryset(self):
        """This Method will return custom queryset"""
        queryset = self.job_posting_app_services.get_list_of_job_posting()
        return queryset

    # @method_decorator(AuthMiddleWare, name="dispatch")
    @action(detail=False, methods=['GET'], url_path='posting/list')
    def list_of_job_posting(self, request):
        """
        Job Posting List Method
        """
        try:
            job_title = request.GET.get("job_title", None)
            if job_title:
                add_result = self.job_collection.aggregate(
                    [
                        {
                            "$search": {
                                "index": "job_posting",
                                "autocomplete": {
                                    "query": job_title,
                                    "path": "job_title",
                                    "fuzzy": {
                                        "maxEdits": 2
                                    }
                                }
                            }
                        }
                    ]
                )
                queryset = list(add_result)
            else:
                queryset = (self.get_queryset())
            list_of_job_posting_serializer = self.get_serializer_class()
            list_of_job_posting_serializer_obj = list_of_job_posting_serializer(
                queryset, many=True)
            return CustomResponse().listing(
                message="Job Posting Listed successfully",
                data=list_of_job_posting_serializer_obj.data
            )
        except Exception as le:
            return CustomResponse().fail(
                status=status.HTTP_400_BAD_REQUEST,
                errors={"error": le.args[0]},
                message="Unable to list jobs. Please contact administrator."
            )

    @method_decorator(AuthMiddleWare, name="dispatch")
    @action(detail=False, methods=['POST'], url_path="bulk/create")
    def bulk_job_posting(self, request):
        """
        Job Posting Bulk Create Method
        """
        try:
            bulk_job_posting_serializer = self.get_serializer_class()
            bulk_job_posting_serializer_obj = bulk_job_posting_serializer(
                data=request.data)
            if bulk_job_posting_serializer_obj.is_valid():
                df = pd.read_excel(
                    bulk_job_posting_serializer_obj.validated_data.get("file"))
                bulk_create_job_post_list = []
                for _, row in df.iterrows():
                    job_posted_data = {
                        "job_title": row['job_name'],
                        "company_name": row['company_name'],
                        'job_description': row['job_full_text'],
                        'job_post_url': row['post_url'],
                        'job_apply_url': row['post_apply_url'],
                        'company_url': row['company_url'],
                        'company_industry': row['Company Industry'],
                        'min_compensation': row['Minimum Compensation'],
                        'max_compensation': row['Maximum Compensation'],
                        'type_of_compensation': row['Compensation Type'],
                        'job_hours': row['Job Hours'],
                        'role_seniority': row['Role Seniority'],
                        'min_education': row['Minimum Education'],
                        'office_location': row['Office Location'],
                        'post_html': row['post_html'],
                        'city': row['city'],
                        'region': row['region'],
                        'country': row['country']
                    }
                    bulk_create_job_post_list.append(job_posted_data)
                self.job_posting_app_services.bulk_create_job_posting_data(
                    data=bulk_create_job_post_list)

                return CustomResponse().success(
                    message="Job Posting created successfully")
            else:
                return CustomResponse().serializer_invalid(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors=bulk_job_posting_serializer_obj.errors,
                    message="Unable to create jobs. Please contact administrator."
                )
        except Exception as le:
            return CustomResponse().fail(
                status=status.HTTP_400_BAD_REQUEST,
                errors={"error": le.args[0]},
                message="Unable to create jobs. Please contact administrator."
            )
