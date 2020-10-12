from spidermon import Monitor, MonitorSuite, monitors


@monitors.name("Requests/Items Ratio")
class RequestsItemsRatioMonitor(Monitor):
    @monitors.name("Maximum requests/items ratio")
    def test_requests_items_ratio(self):
        pass


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        RequestsItemsRatioMonitor,
    ]
