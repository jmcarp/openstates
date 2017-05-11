import lxml.html

from pupa.scrape import Jurisdiction, Organization
from .people import CTPersomScraper
from .bills import CTBillScraper
from .events import CTEventScraper

settings = {
    'SCRAPELIB_RPM': 20
}


class Connecticut(Jurisdiction):
    division_id = "ocd-division/country:us/state:ct"
    classification = "government"
    name = "Connecticut"
    url = "http://www.cga.ct.gov/"
    scrapers = {
        'people': CTPersomScraper,
        'bills': CTBillScraper,
        'events': CTEventScraper,
    }
    parties = [
        {'name': 'Republican'},
        {'name': 'Democratic'}
    ]
    legislative_sessions = [
        {
            "_scraped_name": "2011",
            "identifier": "2011",
            "name": "2011 Regular Session"
        },
        {
            "_scraped_name": "2012",
            "identifier": "2012",
            "name": "2012 Regular Session"
        },
        {
            "_scraped_name": "2013",
            "identifier": "2013",
            "name": "2013 Regular Session"
        },
        {
            "_scraped_name": "2014",
            "identifier": "2014",
            "name": "2014 Regular Session"
        },
        {
            "_scraped_name": "2015",
            "identifier": "2015",
            "name": "2015 Regular Session"
        },
        {
            "_scraped_name": "2016",
            "end_date": "2016-05-04",
            "identifier": "2016",
            "name": "2016 Regular Session",
            "start_date": "2016-02-03"
        },
        {
            "_scraped_name": "2017",
            "identifier": "2017",
            "name": "2017 Regular Session"
        }
    ]
    ignored_scraped_sessions = [
        "2010",
        "2009",
        "2008",
        "2007",
        "2006",
        "2005"
    ]

    def get_organizations(self):
        legislature_name = "Connecticut General Assembly"
        lower_chamber_name = "House"
        lower_seats = 151
        lower_title = "Representative"
        upper_chamber_name = "Senate"
        upper_seats = 36
        upper_title = "Senator"

        legislature = Organization(name=legislature_name,
                                   classification="legislature")
        upper = Organization(upper_chamber_name, classification='upper',
                             parent_id=legislature._id)
        lower = Organization(lower_chamber_name, classification='lower',
                             parent_id=legislature._id)

        for n in range(1, upper_seats+1):
            upper.add_post(
                label=str(n), role=upper_title,
                division_id='{}/sldu:{}'.format(self.division_id, n))
        for n in range(1, lower_seats+1):
            lower.add_post(
                label=str(n), role=lower_title,
                division_id='{}/sldl:{}'.format(self.division_id, n))

        yield legislature
        yield upper
        yield lower

    def get_session_list(self):
        import scrapelib
        text = scrapelib.Scraper().get('ftp://ftp.cga.ct.gov').text
        sessions = [line.split()[-1] for line in text.splitlines()]

        for not_session_name in ('incoming', 'pub', 'CGAAudio', 'rba', 'NCSL', "apaac", 'FOI_1'):
            sessions.remove(not_session_name)
        return sessions

    def get_extract_text(self, doc, data):
        doc = lxml.html.fromstring(data)
        text = ' '.join(p.text_content() for p in doc.xpath('//body/p'))
        return text
