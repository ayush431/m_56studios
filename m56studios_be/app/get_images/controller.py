from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
from .config import Config2

class GetImagesController():
    def __init__(self):
        self.accessed_finished = ""
        self.image_type = ""
        self.query_string = ""
        self.cxs = Config2.cxs
        self.api_keys = Config2.api_keys
        self.link = []
        self.start = 1

    def google_search_t(self, filters, count=0, start_range=1, api_key_change=1, cxs=1):
        if cxs > 18:
            raise Exception(self.accessed_finished)
        local_cxs = self.cxs.get(cxs)
        service = build("customsearch", "v1", developerKey=self.api_keys[api_key_change], cache_discovery=False)
        res = ""
        try:
            if filters.image_type == "all":
                res = service.cse().list(q=filters.query_string,
                                         cx=local_cxs
                                         , searchType="image"
                                         , num=10
                                         , start=start_range
                                         , rights="cc_publicdomain"
                                         , imgSize="LARGE"
                                         , filter="1").execute()
            else:
                res = service.cse().list(q=filters.query_string
                                         , cx=local_cxs
                                         , imgSize=filters.image_type
                                         , rights="cc_publicdomain"
                                         , searchType="image"
                                         , num=10
                                         , start=start_range
                                         , filter="1").execute()

        except GoogleHttpError as e:
            api_key_change += 1
            cxs += 1
            self.accessed_finished += local_cxs
            return self.google_search_t(filters, count, start_range, api_key_change, cxs)
        count = count + 1
        self._form_list(res)
        if count <= 2:
            self.start += 10
            return self.google_search_t(filters, count, self.start, api_key_change)
        return self.link

    def _form_list(self, res):
        data = res
        if "items" in data:
            for _link in data["items"]:
                self.link.append(str(_link["link"]))
