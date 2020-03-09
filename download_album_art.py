import datetime
import os
import subprocess
import traceback
import threading

from configuration import *

def run_sacad_r(path):
  SEMAPHORE.acquire()

  try:
    LOGGER.info(f"Executing sacad_r for {path}")

    result = subprocess.run(
      [SACAD_R_PATH, *SACAD_R_PRE_MUSIC_FOLDER_ARGUMENTS, path, *SACAD_R_POST_MUSIC_FOLDER_ARGUMENTS],
      capture_output=True
    )

    LOGGER.info(result.args)

    stdout = result.stdout
    stderr = result.stderr

    if stdout:
      LOGGER.info(stdout.decode(sys.stdout.encoding))
    if stderr:
      LOGGER.error(stderr.decode(sys.stderr.encoding))

    if result.returncode == 0:
      LOGGER.info(f"Executing sacad_r for path {path} finished successfully")
    else:
      LOGGER.error(f"Executing sacad_r for path {path} finished with error")
  except Exception:
    LOGGER.error(f"Error occured when handling path {path}:")
    LOGGER.error(traceback.format_exc())

  SEMAPHORE.release()

def read_path(path, jobs):
  LOGGER.info(f"Examining path {path}")

  path_content = os.listdir(path)
  job_name = run_sacad_r.__name__

  music_files_found = False
  image_files_found = any(extension in filename for extension in ALLOWED_IMAGE_FILE_EXTENSIONS for filename in path_content)

  for item in path_content:
    full_path = os.path.join(path, item)
    if (os.path.isfile(full_path) and
        any(extension in item for extension in ALLOWED_MUSIC_FILE_EXTENSIONS) and
        music_files_found is False and
        image_files_found is False):
      modified_at = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
      if modified_at > MODIFICATION_DATETIME_THRESHOLD:
        LOGGER.info(f"Path {path} has music files with allowed file extensions {ALLOWED_MUSIC_FILE_EXTENSIONS}, is modified ({modified_at}) later than {MODIFICATION_DATETIME_THRESHOLD} and does not have cover art ({ALLOWED_IMAGE_FILE_EXTENSIONS}")
        music_files_found = True

        jobs.append(threading.Thread(name=f"{job_name}-{path}", target=run_sacad_r, args=(path, )))
        LOGGER.info(f"Created {job_name} job for {path}")
    elif os.path.isdir(full_path):
      LOGGER.info(f"Found sub directory {full_path}")
      read_path(full_path, jobs)

def handle_jobs(jobs):
  for job in jobs:
    job.start()
    LOGGER.info(f"Started job {job.name}")

  for job in jobs:
    job.join()
    LOGGER.info(f"Job {job.name} ready")
