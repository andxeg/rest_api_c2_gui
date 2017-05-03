import time
import threading
from start_rest import start_rest


if __name__ == "__main__":
    thread = threading.Thread(target=start_rest, args=())
    thread.setDaemon(True)
    thread.start()

    for i in range(10):
        print "Main Thread"
        time.sleep(2)
