import os
import hashlib
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.python import to_bytes
from six.moves.urllib.parse import urlparse

class GazetteFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        media_ext = os.path.splitext(url)[1]
        # scrapy bug. for more details see issue #15
        if not media_ext.isalnum():
            media_ext = os.path.splitext(urlparse(url).path)[1]
        return 'full/%s%s' % (media_guid, media_ext)
