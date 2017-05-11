from datetime import datetime

from pupa.scrape import Scraper, Bill

from openstates.utils import LXMLMixin


class NEBillScraper(Scraper, LXMLMixin):
    def scrape(self, session=None):
        if session is None:
            session = self.jurisdiction.legislative_sessions[-1]
            self.info('no session specified, using %s', session['identifier'])

        start_year = datetime.strptime(session['start_date'], '%Y-%m-%d').year
        end_year = datetime.strptime(session['end_date'], '%Y-%m-%d').year
        yield from self.scrape_year(session['identifier'], start_year)
        if start_year != end_year:
            yield from self.scrape_year(session['identifier'], end_year)

    def scrape_year(self, session, year):
        main_url = 'http://nebraskalegislature.gov/bills/search_by_date.php?'\
            'SessionDay={}'.format(year)
        page = self.lxmlize(main_url)

        document_links = self.get_nodes(
            page,
            '//div[@class="main-content"]//div[@class="panel panel-leg"]//'
            'table[@class="table table-condensed"]/tbody/tr/td[1]/a')

        for document_link in document_links:
            # bill_number = document_link.text
            bill_link = document_link.attrib['href']

            # POST request for search form
            # post_dict = {'DocumentNumber': bill_number, 'Legislature': session}
            # headers = urllib.urlencode(post_dict)
            # bill_resp = self.post('http://nebraskalegislature.gov/bills/'
            #     'search_by_number.php', data=post_dict)
            # bill_link = bill_resp.url
            # bill_page = bill_resp.text

            yield self.bill_info(bill_link, session, main_url)

    def bill_info(self, bill_link, session, main_url):
        bill_page = self.lxmlize(bill_link)

        long_title = self.get_node(
            bill_page,
            '//div[@class="main-content"]/div[1]/div/h2').text.split()

        bill_number = long_title[0]
        title = ''
        for x in range(2, len(long_title)):
            title += long_title[x] + ' '
        title = title[0:-1]

        if not title:
            self.error('no title, skipping %s', bill_number)
            return

        bill_type = 'resolution' if 'LR' in bill_number else 'bill'

        bill = Bill(bill_number, session, title, classification=bill_type)

        bill.add_source(main_url)
        bill.add_source(bill_link)

        introduced_by = self.get_node(
            bill_page,
            '//div[@class="main-content"]/div[3]/div[1]/ul/li[1]/a[1]/text()')

        if not introduced_by:
            introduced_by = self.get_node(
                bill_page,
                '//div[@class="main-content"]/div[3]/div[1]/ul/li[1]/text()')
            introduced_by = introduced_by.split('Introduced By:')[1].strip()

        bill.add_sponsorship(
            name=introduced_by,
            entity_type='person',
            primary=True,
            classification='primary',
        )

        action_nodes = self.get_nodes(
            bill_page,
            '//div[@class="main-content"]/div[5]//table/tbody/tr')

        for action_node in action_nodes:
            date = self.get_node(
                action_node,
                './td[1]').text
            date = datetime.strptime(date, '%b %d, %Y')

            # The action node may have an anchor element within it, so
            # we grab all the text within.
            action = self.get_node(
                action_node,
                './td[2]').text_content()

            if 'Governor' in action:
                actor = 'Governor'
            elif 'Speaker' in action:
                actor = 'Speaker'
            else:
                actor = 'upper'

            action_type = self.action_types(action)
            bill.add_action(
                action,
                date.strftime('%Y-%m-%d'),
                chamber=actor,
                classification=action_type,
            )

        # Were in reverse chronological order.
        bill.actions.reverse()

        # Grabs bill version documents.
        version_links = self.get_nodes(
            bill_page,
            '//div[@class="main-content"]/div[3]/div[2]/'
            'div[@class="hidden-xs"]/ul[1]/li/a')

        for version_link in version_links:
            version_name = version_link.text
            version_url = version_link.attrib['href']
            # replace Current w/ session number
            version_url = version_url.replace('Current', session)
            bill.add_version_link(version_name, version_url, media_type='application/pdf')

        # Adds any documents related to amendments.
        amendment_links = self.get_nodes(
            bill_page,
            '//div[@class="main-content"]/div[5]/div[2]/table/tr/td[1]/a')

        for amendment_link in amendment_links:
            amendment_name = amendment_link.text
            amendment_url = amendment_link.attrib['href']
            bill.add_document_link(amendment_name, amendment_url)

        # Related transcripts.
        transcript_links = self.get_nodes(
            bill_page,
            '//div[@class="main-content"]/div[5]/div[2]/'
            'div[@class="hidden-xs"]/table/tr/td/a')

        for transcript_link in transcript_links:
            transcript_name = transcript_link.text
            transcript_url = transcript_link.attrib['href']
            bill.add_document_link(transcript_name, transcript_url)

        return bill

    def action_types(self, action):
        if 'Date of introduction' in action:
            action_type = 'introduction'
        elif 'Referred to' in action:
            action_type = 'referral-committee'
        elif 'Indefinitely postponed' in action:
            action_type = 'committee-failure'
        elif ('File' in action) or ('filed' in action):
            action_type = 'filing'
        elif 'Placed on Final Reading' in action:
            action_type = 'reading-3'
        elif 'Passed' in action or 'President/Speaker signed' in action:
            action_type = 'passage'
        elif 'Presented to Governor' in action:
            action_type = 'executive-receipt'
        elif 'Approved by Governor' in action:
            action_type = 'executive-signature'
        elif 'Failed to pass notwithstanding the objections of the Governor' in action:
            action_type = 'executive-veto'
        elif 'Failed' in action:
            action_type = 'failure'
        elif 'Bill withdrawn' in action:
            action_type = 'withdrawal'
        else:
            action_type = None
        return action_type
