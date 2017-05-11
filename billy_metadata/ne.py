import datetime

metadata = dict(
    name='Nebraska',
    abbreviation='ne',
    legislature_name='Nebraska Legislature',
    legislature_url='http://nebraskalegislature.gov/',
    capitol_timezone='America/Chicago',
    chambers = {
        'upper': {'name': 'Unicameral', 'title': 'Senator'},
    },
    terms=[
        {'name': '2011-2012', 'sessions': ['102', '102S1'],
        'start_year': 2011, 'end_year': 2012},
        {'name': '2013-2014', 'sessions': ['103'],
        'start_year': 2013, 'end_year': 2014},
        {'name': '2015-2016', 'sessions': ['104'],
        'start_year': 2015, 'end_year': 2016},
        {'name': '2017-2018', 'sessions': ['105'],
        'start_year': 2017, 'end_year': 2018},
    ],
    session_details={
        '102': {
            'start_date': datetime.date(2011, 1, 5),
            'end_date': datetime.date(2012, 4, 18),
            'display_name': '102nd Legislature (2011-2012)',
            '_scraped_name': '102nd Legislature 1st and 2nd Sessions',
               },
        '102S1': {
            'display_name': '102nd Legislature, 1st Special Session (2011)',
            '_scraped_name': '102nd Legislature 1st Special Session',
            'start_date': datetime.date(2011, 11, 1),
            'end_date': datetime.date(2011, 11, 22)
                 },
        '103': {
            'start_date': datetime.date(2013, 1, 8),
            'end_date': datetime.date(2014, 5, 30),
            'display_name': '103rd Legislature (2013-2014)',
            '_scraped_name': '103rd Legislature 1st and 2nd Sessions',
               },
        '104': {
            'start_date': datetime.date(2015, 1, 7),
            # Placeholder end date for now
            'end_date': datetime.date(2016, 12, 31),
            'display_name': '104th Legislature (2015-2016)',
            '_scraped_name': '104th Legislature 1st and 2nd Sessions',
               },
        '105': {
            'start_date': datetime.date(2017, 1, 4),
            # Placeholder end date for now
            'end_date': datetime.date(2018, 12, 31),
            'display_name': '105th Legislature (2017-2018)',
            '_scraped_name': '105th Legislature 1st and 2nd Sessions',
               },
        },
    feature_flags=['influenceexplorer'],
    _ignored_scraped_sessions=['101st Legislature 1st and 2nd Sessions',
                               '101st Legislature 1st Special Session',
                               '100th Legislature 1st and 2nd Sessions',
                               '100th Leg. First Special Session',
                              ]

)
