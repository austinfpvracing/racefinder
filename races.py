import argparse
import arrow
import json
from lxml import html
import requests


class RaceFinder(object):
    url = "https://www.multigp.com/mgp/chapters/view/{chapter}"

    def upcoming_races(self, chapter):
        tree = html.fromstring(requests.get(self.url.format(chapter=chapter)).content)

        payload = []
        for tr in tree.xpath('//div[@id="race-grid"]/table/tbody/tr'):
            children = list(tr)

            # Extract event date
            race_date = children[0].text
            time = arrow.get(race_date, 'MMM D, YYYY')

            # Skip past events
            if time.__lt__(arrow.now()):
                continue

            # Get name and link
            race_race_info = list(children[1])
            race_name = race_race_info[0].text
            link_relative = race_race_info[0].attrib['href']
            important_path = link_relative.split('../../')[1]
            race_link = "https://multigp.com/{}".format(important_path)

            # Build JSON
            payload.append({
                'date': time.format('MMM D'),
                'name': race_name,
                'link': race_link
            })

        return json.dumps(payload, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find upcoming races for a MultiGP chapter')
    parser.add_argument('--chapter', help="Chapter URL Key", type=str, required=True)
    args = parser.parse_args()

    finder = RaceFinder()
    print finder.upcoming_races(args.chapter)

