import re
from cv.models.raw_data import RawData

class RawDataPipeline(object):
    def process_item(self, item, spider):
        item["url"] = self.remove_slash(item["url"])
        RawData.create(**item)
        self.parse_entry(item)

    def parse_entry(self, entry):
        if entry["html"] is None:
            return
        # TODO how to remove url with a file extension?
        # a possible way is using response.headers["Content-type"]
        links = re.findall('(https?://'+entry["domain"]+'[^<>"#\s]*)', entry["html"])

        # remove last / in the url
        links = [self.remove_slash(x) for x in links]

        # duplicate
        links = list(set(links))

        # create new entries
        for url in links:
            data = {
                "url": url,
                "domain": entry["domain"],
                "depth": entry["depth"] + 1,
                "parsed_as_entry": 0
            }
            RawData.create_entry(**data)

    @staticmethod
    def remove_slash(url):
        is_with_slash = url[-1:] == '/'
        if is_with_slash:
            url = url[:-1]
        return url
