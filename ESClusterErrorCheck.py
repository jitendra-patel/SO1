/*
Since there is no programming lanugage has been mentioned in test exercise, so I choose python to create a nagios check that will trigger in case of 3 occurrences of a "Handbill not printed" string
in Elasticsearch.
Usuage: python ESClusterErrorCheck.py --host=<ESClusterURL> --port=<ESClusterPort(defaults to 9200)>
*/

#!/usr/bin/python
from nagioscheck import NagiosCheck, UsageError
from nagioscheck import PerformanceMetric, Status
import optparse
import os
ES_QUERY_STRING="Handbill not printed"

try:
    import json
except ImportError:
    import simplejson as json


class ESClusterCheckErrorCount(NagiosCheck):

    def __init__(self):

        NagiosCheck.__init__(self)

        self.add_option('H', 'host', 'host', 'The cluster to check')
        self.add_option('P', 'port', 'port', 'The ES port - defaults to 9200')

    def check(self, opts, args):
        host = opts.host
        port = int(opts.port or '9200')

        es_count_command =  os.popen("curl -XGET 'http://{host}:{port}/_count?q={ES_QUERY_STRING}' 2>/dev/null | /usr/bin/grep -o '"count":[0-9]+' |/usr/bin/cut -d":" -f2")
        error_count = es_count_command.read()
        if error_count > 3:
           raise Status("CRITICAL", "Occurrences of a string[Handbill not printed] in ES reached greater than 3")

if __name__ == "__main__":
    ESClusterCheckErrorCount().run()
