import time
import threading
from start_rest import create_rest_messenger
from start_rest import start_rest_messenger


def work_before_timeout(messenger):
    start_time = int(time.time())
    work_time = 30

    while True:
        print "Main Thread\n"
        time.sleep(5)
        current_time = int(time.time())
        if current_time - start_time >= work_time:
            messenger.terminate()
            break

    print "Main Thread was finished"


if __name__ == "__main__":
    rest_messenger = create_rest_messenger()
    thread = threading.Thread(target=start_rest_messenger, args=(rest_messenger,))
    thread.setDaemon(True)
    thread.start()

    work_before_timeout(rest_messenger)
