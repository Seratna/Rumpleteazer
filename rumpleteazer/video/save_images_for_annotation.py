from itertools import count
from pathlib import Path
from datetime import datetime

import cv2 as cv

from rumpleteazer.util.logging import get_logger

logger = get_logger(name=__name__)


def save_images_for_annotation(output_dir: str, saving=False):
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        logger.error('could not open video capture')
        exit()

    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

    for i in count(0):
        # Capture frame-by-frame
        successful, frame = capture.read()
        if not successful:
            logger.error('failed to get frame. Exiting ...')
            break

        # save image
        if saving and i % 300 == 0:
            file_path = str(Path(output_dir, f'{datetime.now().isoformat()}.png'))
            cv.imwrite(file_path, frame)
            logger.info(f'saved image to {file_path}')

        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    capture.release()
    cv.destroyAllWindows()


def main():
    save_images_for_annotation(output_dir='/home/antares/temp', saving=True)


if __name__ == '__main__':
    main()
