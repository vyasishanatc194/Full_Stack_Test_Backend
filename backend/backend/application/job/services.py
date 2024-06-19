import logging
from typing import Union

from django.db.models.query import QuerySet

from backend.domain.job.models import JobPosting
from backend.domain.job.services import JobPostingServices

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


class JobPostingAppServices:
    """
    Job Application Services
    """

    def __init__(self):
        self.job_posting_services = JobPostingServices()

    def get_job_posting_by_id(self, id: str) -> Union[JobPosting, None]:
        """
        This method will return JobPOsting object if obtained by ID else return None.
        """
        try:
            return self.job_posting_services.get_job_posting_repo().get(id=id)
        except JobPosting.DoesNotExist as e:
            logger.error("Error while Getting JobPosting by Id: %s", e)
            return None

    def get_job_posting_by_job_title(self, job_title: str) -> Union[JobPosting, None]:
        """
        This method will return JobPOsting object obtained by Email.
        """
        try:
            return JobPosting.objects.get(job_title=job_title)
        except JobPosting.DoesNotExist as e:
            logger.error("Error while Getting jobPosting by Job Title: %s", e)
            return None

    def get_list_of_job_posting(self) -> QuerySet[JobPosting]:
        """
        This Method will give list of all Job Postings.
        """
        return self.job_posting_services.get_job_posting_repo().order_by("-created_at")

    def bulk_create_job_posting_data(self, data: list) -> list:
        """
        This Method will create list of Job Postings.
        """
        return self.job_posting_services.get_job_posting_repo().bulk_create(
            [self.job_posting_services.get_job_posting_factory().build_entity_with_id(
                **job_posting_data) for job_posting_data in data]
        )
