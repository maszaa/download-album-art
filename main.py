import sys

from download_album_art import read_path, handle_jobs

def main(argv):
  if len(argv) != 1:
    raise ValueError("Invalid amount of arguments passed, please pass one (input directory)")

  jobs = []
  read_path(argv[0], jobs)
  handle_jobs(jobs)

if __name__ == "__main__":
  main(sys.argv[1:])
