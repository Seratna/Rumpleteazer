import re
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import struct
from collections import deque
from threading import Thread
import logging
import math

from rumpleteazer.util.logging import get_logger


def distance(point):
    x, y = point
    dx = abs(x - 960)
    dy = abs(y - 540)
    return (dx ** 2 + dy ** 2) ** 0.5


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def make_sigmoid_sequence(d: int, n: int):
    steps = []

    cumulated = 0

    for i in range(1, n+1, 1):  # [1, n]
        x = (i / n) * 14 - 7  # map to [-10, 10]
        s = sigmoid(x) * d  # (0, d)
        s = int(round(s))
        step = s - cumulated
        steps.append(min(step, 5))  # clamp step to 5
        cumulated += step

    sum_steps = sum(steps)
    if sum_steps < d:
        adjustment = make_sigmoid_sequence(d-sum_steps, n)
        steps = [sum(t) for t in zip(steps, adjustment)]

    assert sum(steps) == d

    return steps


def make_sequence(dx, dy):
    n = max(dx, dy) // 5

    sequence_x = make_sigmoid_sequence(dx, n)
    sequence_y = make_sigmoid_sequence(dy, n)

    return list(zip(sequence_x, sequence_y))


def man_in_the_middle():
    # list HID devices
    for device_path in Path('/dev').glob(pattern=r'hidraw*'):
        device_name = device_path.name
        with open(Path(f'/sys/class/hidraw/{device_name}/device/uevent'), 'r') as file:
            lines = '\n'.join(file.readlines())
        match = re.search(pattern=r'^HID_NAME=(.*)$',
                          string=lines,
                          flags=re.MULTILINE)
        hid_name = match.group(1)
        logger.info(f'{device_path} {hid_name}')

    # make a queue
    queue = deque(maxlen=1)

    # prepare server
    class _RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(204)
            self.end_headers()
            _data = json.loads(self.rfile.readline().decode())

            if not _data:
                return

            queue.append(_data)

        def log_request(self, code='-', size='-'):
            """disable request log"""
            return

    def _start_server():
        _host = '127.0.0.1'
        _port = 7777
        _server = HTTPServer((_host, _port), _RequestHandler)
        logger.info(f'Server started http://{_host}:{_port}')

        try:
            _server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            _server.server_close()
            logger.info("Server stopped.")

    # run server in another thread
    thread = Thread(target=_start_server, daemon=True)
    thread.start()

    # process and forward mouse reports
    with open('/dev/hidraw0', 'rb') as in_file, open('/dev/hidg0', 'wb') as out_file:
        left_button_mask, = struct.unpack('<H', b'\x01\x00')
        non_left_button_mask, = struct.unpack('<H', b'\xFE\xFF')

        while True:
            report = in_file.read(8)
            button, x, y, wheel, ac_pan = struct.unpack('<Hhhbb', report)
            left_click = bool(button & left_button_mask)

            if left_click:
                # report = struct.pack('<Hhhbb', button & non_left_button_mask, x, y, wheel, ac_pan)
                # out_file.write(report)
                # out_file.flush()

                try:
                    data = queue.pop()
                except IndexError:
                    out_file.write(report)
                    out_file.flush()
                else:
                    x, y = min(data, key=lambda p: distance(p))
                    dx = int(round(x - 960))
                    dy = int(round(y - 540))
                    sequence = make_sequence(dx, dy)

                    for i, (step_x, step_y) in enumerate(sequence, start=1):
                        if i < len(sequence):
                            fake_report = struct.pack('<Hhhbb', button & non_left_button_mask, step_x, step_y, 0, 0)
                        else:
                            fake_report = struct.pack('<Hhhbb', button, step_x, step_y, wheel, ac_pan)

                        out_file.write(fake_report)
                        out_file.flush()

            else:
                out_file.write(report)
                out_file.flush()


def main():
    man_in_the_middle()


if __name__ == '__main__':
    logger = get_logger(name=__name__)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    main()
