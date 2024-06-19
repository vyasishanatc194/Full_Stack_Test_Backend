from typing import Type

from django.db.models.manager import BaseManager

from .models import JobFactory, JobPosting


class JobPostingServices:
    @staticmethod
    def get_job_posting_factory() -> Type[JobFactory]:
        """
        This Method will return JobFactory.
        """
        return JobFactory

    @staticmethod
    def get_job_posting_repo() -> BaseManager[JobPosting]:
        """
        This method will return database manager for the Job Posting model.
        """
        return JobPosting.objects
