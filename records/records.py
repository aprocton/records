import requests
import pandas as pd


class Records:
    """
    Class to query GBIF for all records matching query in given year interval
    """

    def __init__(self, q=None, interval=None):

        self.q = q
        self.interval = interval
        self.params = {"q": self.q,
                       "year": str(self.interval)[1:-1],
                       "basisOfRecord": "PRESERVED_SPECIMEN",
                       "hasCoordinate": "true",
                       "hasGeospatialIssue": "false",
                       "country": "US",
                       "offset": "0",
                       "limit": "300"}
        self.df = self._get_all_records()

    def _get_all_records(self):
        "iterate requests and concatenate responses until end of records"
        baseurl = "http://api.gbif.org/v1/occurrence/search?"
        data = []

        while 1:
            # make request and store results
            res = requests.get(
                url=baseurl,
                params=self.params,
            )

            # increment counter
            self.params["offset"] = str(int(self.params["offset"]) + 300)

            # concatenate data
            idata = res.json()
            data += idata["results"]

            # stop when end of record is reached
            if idata["endOfRecords"]:
                break

        return pd.DataFrame(data)
