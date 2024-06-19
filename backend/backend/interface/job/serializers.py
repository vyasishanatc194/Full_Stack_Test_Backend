import logging

from rest_framework import serializers

from backend.domain.job.models import JobPosting

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


class BulkJobPostingSerializer(serializers.Serializer):
    """
    Serializer class for Job Posting.
    """
    file = serializers.FileField()


class ListOfJobPostingSerializer(serializers.ModelSerializer):
    """
    Serializer class for List of Job Posting.
    """
    class Meta:
        model = JobPosting
        exclude = ['id', 'created_at', 'modified_at']
