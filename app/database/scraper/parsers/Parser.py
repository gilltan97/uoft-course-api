from utils import Scraper
from parsers import CourseParser

import re
import json
import sys
import time


class Parser:
    """
    A parser to parse information of every course

    -- reference --
    :see: https://docs.python.org/3/library/sys.html
    """
    host_url = 'http://coursefinder.utoronto.ca/course-search/search/'
    course_codes = []

    def load_course_codes(self):
        """
        Return the list of course codes of all the courses provided at
        University of Toronto
        """
        scraper = Scraper.Scraper()
        url = Parser.host_url + 'courseSearch/course/search'
        params = {
            'requirements': '',
            'queryText': '',
            'campusParam': 'St. George,Scarborough,Mississauga'}

        json_ = scraper.get_data(url, params=params, write=False, json=True)

        if json_:
            for course_data in json_["aaData"]:
                Parser.course_codes.append(
                    re.search('offImg(.*)',
                    course_data[0]).group(1).split('"')[0]
                )

    def create_json(self, location=''):
        """
        Create a JSON file with the information regarding each course provided
        at University of Toronto
        """
        t1 = time.time()
        parsing_source = 'http://coursefinder.utoronto.ca/course-search/search/courseInquiry/'
        course_info = {'UofT-Courses' : []}
        self.load_course_codes()

        if self.course_codes:
            print('Source: {}'.format(parsing_source))
            for code in self.course_codes:
                courseParser = CourseParser.CourseParser(code)
                course_info['UofT-Courses'].append(courseParser.parse_html())
                sys.stdout.write('\r')
                sys.stdout.write('Parsing course with code %s ' % (code[:-5]))
                sys.stdout.flush()

        if course_info['UofT-Courses']:
            f = open(location + 'courses.json', 'w')
            json.dump(course_info, f, indent=4, sort_keys=True, separators=(',', ':'))

        t2 = time.time()
        print('\n-- Summary --')
        print('Took {} minutes to parse {} courses'.format((t2 - t1)/60, len(self.course_codes)))

