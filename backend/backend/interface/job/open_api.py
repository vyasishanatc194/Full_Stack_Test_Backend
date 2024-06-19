from drf_spectacular.utils import extend_schema

from .serializers import BulkJobPostingSerializer, ListOfJobPostingSerializer

job_listing_tags = ['Job_Posting_Module']

bulk_job_posting_extension = extend_schema(
    tags=job_listing_tags, request=BulkJobPostingSerializer, responses={
        200: BulkJobPostingSerializer}
)
job_listing_extension = extend_schema(
    tags=job_listing_tags, request=ListOfJobPostingSerializer, responses={
        200: ListOfJobPostingSerializer}
)
