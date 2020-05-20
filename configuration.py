import datetime
import logging
import sys
import threading

SACAD_R_PATH = "sacad_r"
SACAD_R_PRE_MUSIC_FOLDER_ARGUMENTS = ["--size-tolerance", "33", "--amazon-sites", "fr", "de", "co.uk", "--"]
SACAD_R_POST_MUSIC_FOLDER_ARGUMENTS = ["1500", "Folder.jpg"]

def SACAD_R_NOT_ALLOWED_STDERR_CONTENT(content):
  content = content.lower()

  if "analyzing library" in content:
    return "errors=0" not in content
  elif "searching covers" in content:
    return "errors=0" not in content or "no result found=0" not in content
  return "error" in content

ALLOWED_MUSIC_FILE_EXTENSIONS = [".flac"]
ALLOWED_IMAGE_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

MODIFICATION_DATETIME_DELTA = datetime.timedelta(days=5)
MODIFICATION_DATETIME_THRESHOLD = datetime.datetime.now() - MODIFICATION_DATETIME_DELTA

MAX_CONCURRENCY = 4
SEMAPHORE = threading.Semaphore(value=MAX_CONCURRENCY)

LOGGER_NAME = "download-album-art"
LOG_FORMAT = "[%(asctime)-15s: %(levelname)s/%(funcName)s] %(message)s"
LOG_FORMATTER = logging.Formatter(LOG_FORMAT)

LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(logging.DEBUG)

STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(STDOUT_HANDLER)

STDERR_HANDLER = logging.StreamHandler(sys.stderr)
STDERR_HANDLER.setFormatter(LOG_FORMATTER)
STDERR_HANDLER.setLevel(logging.ERROR)
LOGGER.addHandler(STDERR_HANDLER)

try:
  from local_configuration import *
except ModuleNotFoundError:
  pass
