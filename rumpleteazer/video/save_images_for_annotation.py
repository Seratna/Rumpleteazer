from itertools import count
from pathlib import Path
from datetime import datetime
import logging

import cv2 as cv


def save_images_for_annotation(output_dir: str, auto_save=False):
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        logging.error('could not open video capture')
        exit()

    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

    for i in count(0):
        # Capture frame-by-frame
        successful, frame = capture.read()
        if not successful:
            logging.error('failed to get frame. Exiting ...')
            break

        # display
        cv.imshow('frame', frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            # quit
            break
        elif (key == ord('s')) or (auto_save and (i % 120 == 0)):
            # save image
            file_path = str(Path(output_dir,
                                 f'{datetime.now().isoformat().replace(":", "-")}.bmp'))
            cv.imwrite(file_path, frame)
            logging.info(f'saved image to {file_path}')

    # When everything done, release the capture
    capture.release()
    cv.destroyAllWindows()


def main():
    save_images_for_annotation(output_dir='/Users/Antares/Documents/data/overwatch',
                               auto_save=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
