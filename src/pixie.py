from config import *
import re
import pxapi

# Fixing array of services
def trim(service_list):
    regex = r"[\"\"\[\]]"
    subst = ""
    result = re.sub(regex, subst, service_list, 0, re.MULTILINE)
    return result

class PixieMetrics:
    """
    Representation of Pixie metrics and return metrics in Prometheus format.
    """

    def __init__(self):
        # Script PxL to get metrics from Pixie
        self.pxl_script = open("script.pxl", "r").read()

        # Pixie client
        logging.debug("Authorizing Pixie client.")
        self.px_client = pxapi.Client(token=pixie_api_key, server_url=pixie_cloud_addr)

        self.cluster_conn = self.px_client.connect_to_cluster(pixie_cluster_id)
        logging.debug("Pixie client connected to %s cluster.", self.cluster_conn.name())

    def get_metrics(self):
        """Return metrics from Pixie"""

        # Run the PxL script on the cluster.
        script = self.cluster_conn.prepare_script(self.pxl_script)

        # Array of slis
        slis = []

        # If you change the PxL script, you'll need to change the
        # columns this script looks for in the result table.
        for row in script.results("http_table"):
            sli = {
                "service": trim(row["service"]),
                "latency_p50": row["latency_p50"],
                "latency_p90": row["latency_p90"],
                "latency_p99": row["latency_p99"],
                "request_throughput": row["request_throughput"],
                "inbound_throughput": row["inbound_throughput"],
                "outbound_throughput": row["outbound_throughput"],
                "error_rate": row["error_rate"],
                "throughput_total": row["throughput_total"],
            }
            slis.append(sli)

        return slis