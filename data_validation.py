import time

from prefect import flow, get_run_logger, task
from tiled.client import from_profile

tiled_client = from_profile("nsls2")


@task(retries=2, retry_delay_seconds=10)
def read_all_streams(uid, beamline_acronym="rsoxs"):
    logger = get_run_logger()
    run = tiled_client[beamline_acronym]["raw"][uid]
    logger.info(f"Validating uid {run.start['uid']}")
    start_time = time.monotonic()
    for stream in run:
        logger.info(f"{stream}...")
        stream_start_time = time.monotonic()
        stream_data = run[stream].read()
        stream_elapsed_time = time.monotonic() - stream_start_time
        logger.info(f"{stream} elapsed_time = {stream_elapsed_time}")
        logger.info(f"{stream} nbytes = {stream_data.nbytes: _}")
    elapsed_time = time.monotonic() - start_time
    logger.info(f"{elapsed_time = }")  # noqa: E202,E251


@flow
def general_data_validation(uid, beamline_acronym="rsoxs"):
    read_all_streams(uid, beamline_acronym)
