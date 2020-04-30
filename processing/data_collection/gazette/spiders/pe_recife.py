"""Recife's gazettes spider

This spider is implemented to crawl Recife's `newest gazette system
<https://www.cepe.com.br/prefeituradiario/>`_. This system covers gazettes from 2017 to
current days. There is also a `deprecated system
<http://www.recife.pe.gov.br/diariooficial-acervo/>`_ which covers gazettes from 2001 to
2016 which is still not implemented.

Implementation details:
    The newest system presents gazettes in three ways:
        - Pagination:
            - Always available
            - Document is a gazette's page
            - Document is an image
        - Exporting:
            - Always available
            - Document can be a gazette's page or the entire gazette
            - Document is a PDF
            - Takes a long time to export and sometimes fails to do it on large gazettes
        - Attachment:
            - Sometimes available
            - When available, sometimes it's encrypted (so... not available)
            - Document is the entire gazette
            - Document is a PDF

    Because "Exporting" is unreliable, "Attachment" is chosen whenever possible and
    "Pagination" is the fallback.

    There weren't found any indications in the responses' content to differentiate extra
    from main editions and executive from legislative sections.

Gazettes examples:
    - `27/02/2018, main edition, 24 pages, with attachment, encrypted (.p7s)
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20180227&pasta=Fevereiro%5CDia%2027>`_
    - `27/07/2019, main edition, 32 pages, with attachment, not encrypted
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20190727&pasta=Julho\Dia%2027>_
    - `24/03/2020, extra edition, 16 pages, without attachment
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20200324&pasta=Marco%5CDia%2024>`_
    - `07/04/2020, main edition, 8 pages, without attachment
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20200407&pasta=Abril\Dia%2007>`_
"""
