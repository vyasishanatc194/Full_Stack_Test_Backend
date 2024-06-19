import logging
import uuid
from dataclasses import dataclass

from django.db import models

from utils.django.custom_models import ActivityTracking

# logging setup
logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


@dataclass(frozen=True)
class JobID:
    """
    This will create UUID that will pass in JobFactory Method

    """
    value: uuid.UUID


# ---------
# Job Posting Model
# ---------
class CompensationChoices(models.TextChoices):
    """
    Choices for Compensation
    """
    ANNUAL = "annual", "Annual"
    HOURLY = "hourly", "Hourly"


class RoleSeniorityChoices(models.TextChoices):
    """
    Choices for Compensation
    """
    MID = "MidLevel", "Mid-Level"
    ENTRY = "EntryLevel", "Entry-Level"
    TL = "TeamLead", "Team_Lead"


class OfficeLocationChoices(models.TextChoices):
    """
    Choices for Compensation
    """
    HYBRID = "Hybrid", "Hybrid"
    WFO = "InOffice", "In-Office"
    WFH = "WorkFromHome", "work-from-home"


class JobPosting(ActivityTracking):
    """
    Job Posting class defined with job title,post_id,company name,description,
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_title = models.CharField(max_length=50, blank=False, null=False)
    company_name = models.CharField(max_length=50, blank=False, null=False)
    job_description = models.CharField(max_length=500, blank=False, null=False)
    job_post_url = models.CharField(max_length=100, blank=False, null=False)
    job_apply_url = models.CharField(max_length=100, blank=False, null=False)
    company_url = models.CharField(max_length=100, blank=False, null=False)
    company_industry = models.CharField(
        max_length=1000, blank=False, null=False)
    min_compensation = models.CharField(
        max_length=10, blank=False, null=False)
    max_compensation = models.CharField(
        max_length=10, blank=False, null=False)
    type_of_compensation = models.CharField(choices=CompensationChoices.choices,
                                            max_length=6, blank=False, null=False)
    job_hours = models.CharField(max_length=10, blank=False, null=False)
    role_seniority = models.CharField(
        choices=RoleSeniorityChoices.choices, max_length=10, blank=False, null=False)
    min_education = models.CharField(max_length=20, blank=False, null=False)
    office_location = models.CharField(
        choices=OfficeLocationChoices.choices, max_length=100, blank=False, null=False)
    post_html = models.TextField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=100, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return self.company_name


class JobFactory:
    """
    This Method is used for building instance of Job
    """
    @staticmethod
    def build_entity(
        id: JobID,
        job_title: str,
        company_name: str,
        job_description: str,
        job_post_url: str,
        job_apply_url: str,
        company_url: str,
        company_industry: str,
        min_compensation: str,
        max_compensation: str,
        type_of_compensation: str,
        job_hours: str,
        role_seniority: str,
        min_education: str,
        office_location: str,
        post_html: str,
        city: str,
        region: str,
        country: str,
    ) -> JobPosting:
        return JobPosting(
            id=id.value,
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            job_post_url=job_post_url,
            job_apply_url=job_apply_url,
            company_url=company_url,
            company_industry=company_industry,
            min_compensation=min_compensation,
            max_compensation=max_compensation,
            type_of_compensation=type_of_compensation,
            job_hours=job_hours,
            role_seniority=role_seniority,
            min_education=min_education,
            office_location=office_location,
            post_html=post_html,
            city=city,
            region=region,
            country=country
        )

    @classmethod
    def build_entity_with_id(
        cls,
        job_title: str,
        company_name: str,
        job_description: str,
        job_post_url: str,
        job_apply_url: str,
        company_url: str,
        company_industry: str,
        min_compensation: str,
        max_compensation: str,
        type_of_compensation: str,
        job_hours: str,
        role_seniority: str,
        min_education: str,
        office_location: str,
        post_html: str,
        city: str,
        region: str,
        country: str,
    ) -> JobPosting:
        entity_id = JobID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id,
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            job_post_url=job_post_url,
            job_apply_url=job_apply_url,
            company_url=company_url,
            company_industry=company_industry,
            min_compensation=min_compensation,
            max_compensation=max_compensation,
            type_of_compensation=type_of_compensation,
            job_hours=job_hours,
            role_seniority=role_seniority,
            min_education=min_education,
            office_location=office_location,
            post_html=post_html,
            city=city,
            region=region,
            country=country
        )
