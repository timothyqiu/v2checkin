from __future__ import absolute_import

import sys


PY2 = sys.version_info[0] == 2


if PY2:
    def iteritems(d, **kwargs):
        return d.iteritems(**kwargs)

    import urlparse
    urllib_parse = urlparse
else:
    def iteritems(d, **kwargs):
        return d.items(**kwargs)

    import urllib.parse
    urllib_parse = urllib.parse
