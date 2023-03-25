from rest_framework import serializers
from .model import question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = ["qn_id", "question", "created_at", "resrc_url", "original_url", 
                    "cropped_json", "difficulty_level", "category",
                    "model_release", "property_release", "license", "system_check",
                    "invalid_reason", "is_image_hint", "status", "original_qn_id",
                    "qn_verified_by_editor", "ans_verified_by_editor", 
                    "rejected_by_editor", "qn_rejected_by_reviewer", "img_rejected_by_reviewer",
                    "approved_by_reviewer", "approved_by_manager", "rereview_by_manager", "published",
                    "discarded_by_editor", "should_overwrite", "reason_for_overwrite",  "vendor_id", "vendor_name",  "options",
                    "comments", "qn_submitted_date", "user_id", "user_reviewed", "options_str", "right_answer", "comments_str",
                    "offline_content", "resrc_type", "reveal_image_url", "is_active", "flagged_reason"]
