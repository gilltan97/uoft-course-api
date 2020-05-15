from utils import Scraper
from parsers import Helpers
import bs4 as BeautifulSoup


class CourseParser:
    """
    Course parser which parses data from web service called
    Course Finder located at: http://coursefinder.utoronto.ca/.

    -- references --
    :see: https://docs.python.org/3.4/library/re.html
    """
    host_url = 'http://coursefinder.utoronto.ca/course-search/search/'

    def __init__(self, course_code):
        self.course_code = course_code

    def retrieve_html(self):
        """
        Search for course at host url and retrieve the html data with the
        given course code
        """
        scraper = Scraper.Scraper()
        url = CourseParser.host_url + 'courseInquiry'
        params = {
            'methodToCall': 'start',
            'viewId': 'CourseDetails-InquiryView',
            'courseId': '{}'.format(self.course_code)
        }
        return scraper.get_data(url, params=params, json=False, write=False)

    def parse_html(self):
        """
        Parse the HTML content and create a JSON file from that content
        """
        soup = BeautifulSoup.BeautifulSoup(self.retrieve_html(), 'html.parser')

        if soup.find(id='u19')['data-headerfor'] != 'correctPage':
            print("Course not found.")
            return None

        return {
            'code': self.course_code[:-5],
            'name': Helpers.get_name(soup),
            'division': Helpers.get_division(soup),
            'department': Helpers.get_department(soup),
            'prerequisites': Helpers.get_prerequisites(soup),
            'exclusion': Helpers.get_exclusion(soup),
            'level': Helpers.get_courselevel(soup),
            'campus': Helpers.get_campus(soup),
            'breadth requirements': Helpers.get_breadth(soup),
            'term': Helpers.get_term(soup),
            'sections': Helpers.get_sections(soup)
        }
