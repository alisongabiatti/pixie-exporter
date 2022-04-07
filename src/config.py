import logging
import os

# Variables to connect to the Pixie cluster.
if "PIXIE_API_KEY" not in os.environ:
    logging.error("Missing `PIXIE_API_KEY` environment variable.")
pixie_api_key = os.environ['PIXIE_API_KEY']

if "PIXIE_CLUSTER_ID" not in os.environ:
    logging.error("Missing `PIXIE_CLUSTER_ID` environment variable.")
pixie_cluster_id = os.environ['PIXIE_CLUSTER_ID']

if "PL_CLOUD_ADDR" not in os.environ:
    logging.error("Missing `PL_CLOUD_ADDR` environment variable.")
pixie_cloud_addr = os.environ.get('PL_CLOUD_ADDR', "work.withpixie.ai")