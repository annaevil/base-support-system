import os
import logging

worker_name = f'api-service-{os.getpid()}'

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-16.16s %(message)s')

logging.getLogger(worker_name).setLevel(logging.INFO)

root_logger = logging.getLogger(worker_name)
normal_format = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-16.16s %(message)s')
error_format = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-16.16s %(filename)s:%(lineno)s %(message)s')


def info(msg):
    root_logger.log(logging.INFO, msg)


def warn(msg):
    root_logger.log(logging.WARN, msg)


def error(msg):
    root_logger.log(logging.ERROR, msg)
