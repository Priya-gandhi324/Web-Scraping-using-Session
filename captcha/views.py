from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
from datetime import datetime
from .models import CaseStatus, Cases
import pandas as pd
import re
import json

# Create your views here.

def captcha_session(request):
    session = requests.Session()
    response = session.get('https://drt.gov.in/front/captcha.php')
    if response.status_code == 200:
        with open("captcha.png", "wb") as f:
            f.write(response.content)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        img = Image.open('captcha.png')
        text = int(pytesseract.image_to_string(img))
        url = "https://drt.gov.in/front/page1_advocate.php"
        
        payload = {
            'schemaname' : 2,
            'name' : 'sha',
            'answer' : text,
            'submit11': 'Search'
        }

        response = session.post(url, data=payload)
        
        if response.status_code == 200:
            scrape_status = 0
            parse_page = BeautifulSoup(response.text, 'html.parser')
            div = parse_page.find('div', class_= 'col-md-12')
            table = div.find('table')
            rows = table.find_all('tr')

            if len(rows) > 1:
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) == 8:
                        diary_no = cells[0].text.strip()
                        case_no = cells[1].text.strip()	
                        date_of_filing = cells[2].text.strip()
                        date_of_filing = datetime.strptime(date_of_filing, "%d/%m/%Y").date()
                        applicant = cells[3].text.strip()
                        respondent = cells[4].text.strip()	
                        applicant_advocate = cells[5].text.strip()
                        respondent_advocate = cells[6].text.strip()
                        view_more = cells[7].find('a', href=True)['href'].split("'")
                        filename = view_more[1]
                        view_more = f'https://drt.gov.in/drtlive/Misdetailreport.php?no={filename}'
                        
                        if not Cases.objects.filter(diary_no=diary_no, date_of_filing=date_of_filing):
                            cases = Cases(scrape_status=scrape_status, diary_no = diary_no, case_no = case_no, date_of_filing = date_of_filing, 
                                          applicant = applicant, respondent = respondent, applicant_advocate = applicant_advocate, 
                                          respondent_advocate = respondent_advocate, view_more = view_more)
                            cases.save()
                        
                        if Cases.objects.filter(scrape_status = 0):
                            r2 = session.get(view_more)
                            if r2.status_code == 200:
                                pdf_parse = BeautifulSoup(r2.text, 'html.parser')
                                tables = pdf_parse.find_all('table')
                                court_details = []
                                for table in tables:
                                    title = table.find('th')
                                    if title != None:
                                        title = title.text.strip()
                                        if title == 'CASE STATUS':
                                            cells = table.find_all('td')
                                            case_type = cells[3].text.strip()
                                            drt_detail = cells[5].text.strip()
                                            case_status = cells[9].text.strip()
                                            in_the_court_of = court_no = next_listing_date = next_listing_purpose = ''
                                            for i in range(10, len(cells)):
                                                what = cells[i].text.strip()
                                                if what == 'In the Court of':
                                                    in_the_court_of = cells[i + 1].text.strip()
                                                elif what == 'Court No.':
                                                    court_no = cells[i+1].text.strip()
                                                elif what == 'Next Listing Date' and what != '':
                                                    next_listing_date = cells[i+1].text.strip()
                                                    if next_listing_date != '':
                                                        next_listing_date = datetime.strptime(next_listing_date, "%d/%m/%Y").date()
                                                elif what == 'Next Listing Purpose':
                                                    next_listing_purpose = cells[i+1].text.strip()
                                        elif title == 'CASE PROCEEDING DETAILS':
                                            cells = table.find_all('td')[3::]
                                            if len(cells) > 1:
                                                for i in range(0, len(cells)-2, 2):
                                                    court_detail = {
                                                        'court_name' : cells[i].text.strip(),
                                                        'causelist_Date' : cells[i+1].text.strip(),
                                                        'purpose' : cells[i+2].text.strip()
                                                    }
                                                    court_details.append(court_detail)
                                                court_details = json.dumps(court_details)
                                        elif title == 'PETITIONER/APPLICANT DETAIL':
                                            cells = table.find_all('td')
                                            petitioner_name = petitioner_address = petitioner_additional_party = petitioner_additional_advocate = ''
                                            petitioner = cells[0].text.strip()
                                            petitioner = re.sub('[^A-Za-z0-9]', ' ', petitioner)
                                            petitioner = petitioner.split('   ')
                                            petitioner = [i for i in petitioner if i]
                                            for i in range(len(petitioner) - 1):
                                                if petitioner[i].strip() == 'Petitioner Name' and petitioner[i + 1].strip() != 'Petitioner Applicant Address':
                                                    petitioner_name = petitioner[i + 1]
                                                if petitioner[i].strip() == 'Petitioner Applicant Address' and petitioner[i + 1].strip() != 'Additional Party':
                                                    petitioner_address = petitioner[i + 1]
                                                if petitioner[i].strip() == 'Additional Party' and petitioner[i + 1].strip() != 'Advocate Name':
                                                    petitioner_additional_party = petitioner[i + 1]
                                                if 'Additional Advocate' not in petitioner[-1].strip():
                                                    petitioner_additional_advocate = petitioner[-1]
                                            respondent_name = respondent_address = respondent_additional_party = respondent_additional_advocate = ''
                                            respondent = cells[1].text.strip()
                                            respondent = re.sub('[^A-Za-z0-9]', ' ', respondent)
                                            respondent = respondent.split('   ')
                                            respondent = [i for i in respondent if i]
                                            for i in range(len(respondent) - 1):
                                                if respondent[i].strip() == 'Respondent Name' and respondent[i + 1].strip() != 'Respondent Defendent Address':
                                                    respondent_name = respondent[i + 1]
                                                if respondent[i].strip() == 'Respondent Defendent Address' and respondent[i + 1].strip() != 'Additional Party':
                                                    respondent_address = respondent[i + 1]
                                                if respondent[i].strip() == 'Additional Party' and respondent[i + 1].strip() != 'Advocate Name':
                                                    respondent_additional_party = respondent[i + 1]
                                                if 'Additional Advocate' not in respondent[-1].strip():
                                                    respondent_additional_advocate = respondent[-1]
                                                
                                table3 = pdf_parse.find_all('table', class_ = 'table table-striped')
                                prop_details = []
                                if len(table3) > 1:
                                    cells = table3.find_all('td')[2::]
                                    if len(cells) > 1:
                                        for i in range(0, len(cells)-1, 1):
                                            prop_detail = {
                                                'property_type' : cells[i].text.strip(),
                                                'detail_of_property' : cells[i+1].text.strip(),
                                            }
                                            prop_details.append(prop_detail)
                                        prop_details = json.dumps(prop_details)
                            
                                case_statuses = CaseStatus(diary_no = diary_no, case_type = case_type, drt_detail = drt_detail, 
                                                             date_of_filing = date_of_filing, case_status = case_status, 
                                                             in_the_court_of = in_the_court_of, court_no = court_no, 
                                                             next_listing_date = next_listing_date, next_listing_purpose = next_listing_purpose,
                                                             petitioner_name = petitioner_name, petitioner_address = petitioner_address, 
                                                             petitioner_additional_party = petitioner_additional_party, 
                                                             petitioner_advocate_name = applicant_advocate,
                                                             petitioner_additional_advocate = petitioner_additional_advocate,
                                                             respondent_name = respondent_name, respondent_address = respondent_address,
                                                             respondent_additional_party = respondent_additional_party,
                                                             respondent_advocate_name =  respondent_advocate, 
                                                             respondent_additional_advocate = respondent_additional_advocate,
                                                             court_details = court_details, prop_details = prop_details)
                                case_statuses.save()
                                Cases.objects.filter(diary_no = diary_no, date_of_filing = date_of_filing).update(scrape_status = 1, modified = datetime.utcnow())
    
    df = pd.DataFrame.from_records(Cases.objects.values()).to_html()
    return HttpResponse(df)
