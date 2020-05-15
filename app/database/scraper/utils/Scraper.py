import requests
import time
import json


class Scraper:
    """
    Scraper to scrape data do from web services at given url

    -- reference --
    :see: https://media.readthedocs.org/pdf/requests/master/requests.pdf
    :see: https://goo.gl/AvJVc7
    """
    s = requests.Session()

    def get_data(self, url, params=None, headers=None, rendered_doc=None,
                 attempts=15, write=False, location='', json=False):
        """
        Scrape data from web service at specified url through get request.
        More requests are automatically made if the status code is either
        not 200.

        TODO: provide a proper documentation

        :param url: url of the web page from which data is to be scrapped
        :type url: str
        :return: html content of host as a string
        :rtype: str
        """
        while attempts:
            try:
                request = Scraper.s.get(url, params=params, headers=headers, timeout=7)
                if request.status_code == requests.codes.ok:
                    rendered_doc = request.json() if json else request.text
                    break
                else:
                    attempts -= 1
                    time.sleep(1)
                    continue
            except requests.exceptions.RequestException:
                attempts -= 1
                continue

        def format_chooser(format):
            return open(location + 'unfilteredData.{}'.format(format), 'w')

        if json and write:
            f = format_chooser('json')
            json.dump(
                rendered_doc,
                f,
                indent=4,
                sort_keys=True,
                separators=(',', ':')
            )

        elif not json and write:
            f = format_chooser('text')
            f.write(rendered_doc)

        return rendered_doc
