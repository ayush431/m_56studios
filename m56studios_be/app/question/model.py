from django.db import models
import uuid
from ..models import user_model
from common.utility import validate_capitalized


class question(models.Model):

    class resrc_type(models.TextChoices):
        IMG = "image/jpeg"
        MP3 = "audio/mp3"

    class difficult_level(models.TextChoices):
        EASY = "Easy", "easy" 
        MEDIUM = "Medium", "medium" 
        HARD = "Hard", "hard"
        VERY_HARD = "Very Hard", "very_hard"
    
    class system_checks(models.TextChoices):
        VALID = "Valid", "valid"
        INVALID = "Invalid", "invalid"
        DUPLICATE = "Duplicate", "duplicate"
        PROFANITY = "Profanity", "Profanity"

    class status_choice(models.TextChoices):
        DRAFT = "Draft"
        FOR_REVIEW = "For Review"
        APPROVED = "Approved"
        REJECTED_BY_EDITOR = "Rejected"
        IMAGE_REJECTED = "Image Rejected"
        QUESTION_REJECTED = "Question Rejected"
        READY_TO_PUBLISH = "Ready To Publish"
        PUBLISHED = "Published"
        RE_REVIEW = "ReReview"
        DISCARDED = "Discarded"
        OVERWRITTEN = "Overwritten"
        FLAGGED = "Flagged"

    class categories(models.TextChoices):
        PEOPLE = "PEOPLE", "People"
        POLITICS = "POLITICS", "Politics"
        BUSINESS_AND_TECH = "BUSINESS & TECH", "Business & Tech"
        CARS = "CARS", "Cars"
        ART = "ART", "Art"
        TRUE_OR_FALSE = "TRUE OR FALSE", "True_or_false"
        I_SPY = "I SPY", "I_spy"
        WHO_S_THIS = "WHO's THIS", "Who's this"
        MATH = "MATH", "Math"
        SCIENCE = "SCIENCE", "Science"
        FOOD = "FOOD", "Food"
        HISTORY = "HISTORY", "History"
        BOOKS = "BOOKS", "Books"
        LIFESTYLE = "LIFESTYLE", "Lifestyle"
        MUSIC = "MUSIC", "Music"
        WORD_JAM = "WORD JAM", "Word_jam"
        GEOGRAPHY = "GEOGRAPHY", "Geography"
        SPORTS = "SPORTS", "Sports"
        ENTERTAINMENT = "ENTERTAINMENT", "Entertainment"
        HANX_MOVIES = "HANX MOVIES", "Hanx Movies"

        
    qn_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now=True)
    resrc_url = models.CharField(max_length=2000, null=True)
    original_url = models.CharField(max_length=2000, null=True)
    cropped_json = models.JSONField(blank=True, null=True)
    images_x = models.JSONField(blank=True, null=True)
    difficulty_level = models.CharField(
        ("Type"), max_length=50, choices=difficult_level.choices, null=True)
    flagged_reason =  models.JSONField(blank=True, null=True)
    category = models.CharField(
        ("Type"), max_length=50, choices=categories.choices, null=True)
    model_release = models.BooleanField(default=False)
    property_release = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    license = models.CharField(max_length=254, null=True)
    system_check = models.CharField(
        ("Type"), max_length=50, choices=system_checks.choices, null=True)
    invalid_reason = models.CharField(max_length=254, null=True, blank=True)
    status = models.CharField(
        ("Type"), max_length=50, choices=status_choice.choices, null=False, default=status_choice.DRAFT)
    is_image_hint =  models.BooleanField(default=False)
    original_qn_id = models.CharField(max_length=254, null=False)
    vendor_id = models.UUIDField(default=uuid.uuid4, editable=False)
    vendor_name = models.CharField(max_length=254, null=True)
    qn_submitted_date = models.DateField(null=True)

    rejected_by_editor = models.BooleanField(default=False)
    qn_rejected_by_reviewer = models.BooleanField(default=False)
    img_rejected_by_reviewer = models.BooleanField(default=False)
    approved_by_reviewer = models.BooleanField(default=False)
    approved_by_manager = models.BooleanField(default=False)
    rereview_by_manager = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    offline_content = models.BooleanField(default=False, null=False)
    discarded_by_editor = models.BooleanField(default=False)
    should_overwrite = models.BooleanField(default=False)
    reason_for_overwrite = models.TextField(null=True)
    exported_date = models.DateTimeField(null=True, default=None)
        
    user_id = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="user_id_key")
    user_reviewed = models.ForeignKey(user_model, null=True, related_name="user_reviewed_key", on_delete=models.CASCADE)

    resrc_type = models.CharField(
        ("Type"), max_length=50, choices=resrc_type.choices, null=True, default=None)
    reveal_image_url = models.CharField(max_length=2000, null=True)

    @property
    def options(self):
        "Returns the question's choices."
        from app.options.controller import OptionsController
        return OptionsController().get(qn_id=self.qn_id)

    @property
    def options_str(self):
        "Returns the question's choices in string."
        all_options = ""
        for each_option in self.options:
            all_options += each_option["option"] + ", "
        return all_options

    @property
    def right_answer(self):
        "Returns the question's choices in string."
        for each_option in self.options:
            if each_option["is_correct"]:
                return each_option["option"]
        

    @property
    def comments(self):
        "Returns the question's comments."
        from app.comments.controller import CommentsController
        return CommentsController().get(qn_id=self.qn_id)
    
    @property
    def comments_str(self):
        "Returns the question's choices in string."
        return str(self.comments)

    @property
    def qn_verified_by_editor(self):
        return False
    
    @property
    def ans_verified_by_editor(self):
        return False

    # @property
    # def user_email(self):
    #     print("HERE IS USER_EMAIL", user_id.email)
    #     return user_id.email