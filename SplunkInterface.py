import splunklib.client as client
import splunklib.results as results

class SplunkInterface:
    def __init__(self):
        self.service = client.connect(host="localhost", port=8089, username="admin")

    def deleteLogFiles(self, source):
        saved_searches = self.service.saved_searches
        saved_searches.create('my_saved_search',
                              'source="' + source + '" | delete')
        assert 'my_saved_search' in saved_searches
        saved_searches.delete('my_saved_search')
        assert 'my_saved_search' not in saved_searches

    def ingestLogFiles(self, source):
        if len(self.retrieveLogEntries(source)) > 0:
            return True
        inputs = self.service.inputs
        inputs.create(source, "monitor")
        return False

    def retrieveLogEntries(self, source):
        jobs = self.service.jobs
        logEntries = list()

        kwargs_blockingsearch = {"exec_mode": "blocking"}
        searchquery_blocking = 'search source="' + source + '"'

        job = jobs.create(searchquery_blocking, **kwargs_blockingsearch)
        rr = results.ResultsReader(job.preview())
        for result in rr:
            if isinstance(result, results.Message):
                print('%s: %s' % (result.type, result.message))
            elif isinstance(result, dict):
                logEntries.append(result["_raw"])
        return logEntries