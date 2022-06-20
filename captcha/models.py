from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class Cases(TimeStampedModel):
    scrape_status = models.IntegerField()
    diary_no = models.TextField()
    case_no = models.TextField()
    date_of_filing = models.DateField()
    applicant = models.TextField()
    respondent = models.TextField()
    applicant_advocate = models.TextField()
    respondent_advocate = models.TextField()
    view_more = models.URLField()

    
class CaseStatus(models.Model):
    diary_no = models.TextField()
    case_type =  models.TextField()
    drt_detail = models.TextField()
    date_of_filing = models.DateField()
    case_status = models.TextField()
    in_the_court_of = models.TextField()
    court_no = models.TextField()
    next_listing_date = models.TextField()
    next_listing_purpose = models.TextField()
    petitioner_name = models.TextField()
    petitioner_address = models.TextField()
    petitioner_additional_party = models.TextField()
    petitioner_advocate_name = models.TextField()
    petitioner_additional_advocate = models.TextField()
    respondent_name = models.TextField()
    respondent_address = models.TextField()
    respondent_additional_party = models.TextField() 
    respondent_advocate_name = models.TextField()
    respondent_additional_advocate = models.TextField()
    court_details = models.TextField()
    prop_details = models.TextField()