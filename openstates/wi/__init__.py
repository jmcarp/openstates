from pupa.scrape import Jurisdiction, Organization

from openstates.utils import url_xpath

from .bills import WIBillScraper
from .events import WIEventScraper
from .people import WIPersonScraper
from .committees import WICommitteeScraper


class Wisconsin(Jurisdiction):
    division_id = "ocd-division/country:us/state:wi"
    classification = "government"
    name = "Wisconsin"
    url = "http://legis.wisconsin.gov/"
    scrapers = {
        'bills': WIBillScraper,
        'events': WIEventScraper,
        'people': WIPersonScraper,
        'committees': WICommitteeScraper,
    }
    parties = [
        {'name': 'Republican'},
        {'name': 'Democratic'}
    ]
    legislative_sessions = [
        {
            "_scraped_name": "2009 Regular Session",
            "classification": "primary",
            "end_date": "2011-01-03",
            "identifier": "2009 Regular Session",
            "name": "2009 Regular Session",
            "start_date": "2009-01-13"
        },
        {
            "_scraped_name": "2011 Regular Session",
            "classification": "primary",
            "end_date": "2013-01-07",
            "identifier": "2011 Regular Session",
            "name": "2011 Regular Session",
            "start_date": "2011-01-11"
        },
        {
            "_scraped_name": "2013 Regular Session",
            "classification": "primary",
            "end_date": "2014-01-13",
            "identifier": "2013 Regular Session",
            "name": "2013 Regular Session",
            "start_date": "2013-01-07"
        },
        {
            "_scraped_name": "2015 Regular Session",
            "classification": "primary",
            "end_date": "2016-01-11",
            "identifier": "2015 Regular Session",
            "name": "2015 Regular Session",
            "start_date": "2015-01-05"
        },
        {
            "_scraped_name": "December 2009 Special Session",
            "classification": "special",
            "identifier": "December 2009 Special Session",
            "name": "Dec 2009 Special Session"
        },
        {
            "_scraped_name": "December 2013 Special Session",
            "classification": "special",
            "identifier": "December 2013 Special Session",
            "name": "Dec 2013 Special Session"
        },
        {
            "_scraped_name": "January 2011 Special Session",
            "classification": "special",
            "identifier": "January 2011 Special Session",
            "name": "Jan 2011 Special Session"
        },
        {
            "_scraped_name": "January 2014 Special Session",
            "classification": "special",
            "identifier": "January 2014 Special Session",
            "name": "Jan 2014 Special Session"
        },
        {
            "_scraped_name": "June 2009 Special Session",
            "classification": "special",
            "identifier": "June 2009 Special Session",
            "name": "Jun 2009 Special Session"
        },
        {
            "_scraped_name": "October 2013 Special Session",
            "classification": "special",
            "identifier": "October 2013 Special Session",
            "name": "Oct 2013 Special Session"
        },
        {
            "_scraped_name": "September 2011 Special Session",
            "classification": "special",
            "identifier": "September 2011 Special Session",
            "name": "Sep 2011 Special Session"
        },
        {
            "_scraped_name": "2017 Regular Session",
            "classification": "primary",
            "end_date": "2018-05-23",
            "identifier": "2017 Regular Session",
            "name": "2017 Regular Session",
            "start_date": "2017-01-03"
        },
    ]
    ignored_scraped_sessions = [
        "January 2017 Special Session",
        "February 2015 Extraordinary Session",
        "2007 Regular Session",
        "April 2008 Special Session",
        "March 2008 Special Session",
        "December 2007 Special Session",
        "October 2007 Special Session",
        "January 2007 Special Session",
        "February 2006 Special Session",
        "2005 Regular Session",
        "January 2005 Special Session",
        "2003 Regular Session",
        "January 2003 Special Session",
        "2001 Regular Session",
        "May 2002 Special Session",
        "January 2002 Special Session",
        "May 2001 Special Session",
        "1999 Regular Session",
        "May 2000 Special Session",
        "October 1999 Special Session",
        "1997 Regular Session",
        "April 1998 Special Session",
        "1995 Regular Session",
        "January 1995 Special Session",
        "September 1995 Special Session"
    ]

    def get_organizations(self):
        legislature_name = "Wisconsin State Legislature"
        lower_chamber_name = "Assembly"
        lower_seats = 99
        lower_title = "Representative"
        upper_chamber_name = "Senate"
        upper_seats = 33
        upper_title = "Senator"

        legislature = Organization(name=legislature_name,
                                   classification="legislature")
        upper = Organization(upper_chamber_name, classification='upper',
                             parent_id=legislature._id)
        lower = Organization(lower_chamber_name, classification='lower',
                             parent_id=legislature._id)

        for n in range(1, upper_seats + 1):
            upper.add_post(
                label=str(n), role=upper_title,
                division_id='{}/sldu:{}'.format(self.division_id, n))
        for n in range(1, lower_seats + 1):
            lower.add_post(
                label=str(n), role=lower_title,
                division_id='{}/sldl:{}'.format(self.division_id, n))

        yield legislature
        yield upper
        yield lower

    def get_session_list(self):
        sessions = url_xpath('http://docs.legis.wisconsin.gov/search',
                             "//select[@name='sessionNumber']/option/text()")
        return [session.strip(' -') for session in sessions]
