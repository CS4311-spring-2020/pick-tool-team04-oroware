import splunklib.client as client
import splunklib.results as results

class SplunkInterface:

    def deleteLogFiles(self, source):
        service = client.connect(host="localhost", port=8089, username="admin")
        saved_searches = service.saved_searches
        saved_searches.create('my_saved_search',
                              'source="' + source + '" | delete')
        assert 'my_saved_search' in saved_searches
        saved_searches.delete('my_saved_search')
        assert 'my_saved_search' not in saved_searches

    def ingestLogFiles(self, source):
        service = client.connect(host="localhost", port=8089, username="admin")
        if len(self.retrieveLogEntries(source)[0]) > 0:
            return True
        inputs = service.inputs
        inputs.create(source, "monitor")
        return False

    def retrieveLogEntries(self, source):
        service = client.connect(host="localhost", port=8089, username="admin")
        jobs = service.jobs
        logEntries = list()
        timestamps = list()

        kwargs_blockingsearch = {"exec_mode": "blocking"}
        searchquery_blocking = 'search source="' + source + '"'
        job = jobs.create(searchquery_blocking, **kwargs_blockingsearch)
        resultCount = job["resultCount"]
        offset = 0
        count = 100

        while(offset < int(resultCount)):
            kwargs_paginate = {"count": count,
                               "offset": offset}
            # Get the search results and display them
            blocksearch_results = job.results(**kwargs_paginate)

            for result in results.ResultsReader(blocksearch_results):
                if isinstance(result, results.Message):
                    print('%s: %s' % (result.type, result.message))
                elif isinstance(result, dict):
                    logEntries.append(result["_raw"])
                    timestamp = result["_time"]
                    timestamp = timestamp[0:timestamp.index(".")]
                    timestamp = timestamp.replace("T", " ")
                    timestamps.append(timestamp)

            # Increase the offset to get the next set of results
            offset += count
        return logEntries, timestamps