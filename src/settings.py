from pathlib import Path
import os


IMAGES_STORAGE_FOLDER_NAME = 'images'
JSON_STORAGE_FOLDER_NAME = 'data'

ROOT = Path(os.path.realpath(__file__)).parent.parent
IMAGES_STORAGE_FOLDER_PATH = ROOT.joinpath(IMAGES_STORAGE_FOLDER_NAME)
JSON_STORAGE_FOLDER_PATH = ROOT.joinpath(JSON_STORAGE_FOLDER_NAME)

THREADS_COUNT = 3
FROM_PAGE = 200
TO_PAGE = 205
