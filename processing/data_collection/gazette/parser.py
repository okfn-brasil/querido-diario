import os
import hashlib
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.python import to_bytes
from six.moves.urllib.parse import urlparse

"""Pipeline to handle URL containing query parameters.

This pipeline is a temporary parser to remove existing query parameters in a URL string.
Example:
- The URL to download a gazette from Rio de Janeiro is http://doweb.rio.rj.gov.br/ler_pdf.php?download=ok&edi_id=3651
- Scrapy uses URL's sha1 to store the file locally
- However, Scrapy also uses the query parameter as file extension
Resulting filename: '4f15e18052b51dd8dffad1cc243279f40a2e21c3.php?download=ok&edi_id=3651'
- GazetteFilesPipeline ignores everything after file extension ('?download=ok&edi_id=3651')
and resulting in the following filename: '4f15e18052b51dd8dffad1cc243279f40a2e21c3.php'

This pipeline is temporary and could be deleted as soon as https://github.com/scrapy/scrapy/pull/2809 gets merged

For more details, see https://github.com/okfn-brasil/diario-oficial/issues/15

"""
class GazetteFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest() # the filename is the URL's sha1
        media_ext = os.path.splitext(url)[1]
        if not media_ext.isalnum():
            media_ext = os.path.splitext(urlparse(url).path)[1] # remove everything after the file extension (like query param)
        return 'full/%s%s' % (media_guid, media_ext)
