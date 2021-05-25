""" create thread demo """

import threading
import time

def do_it() -> None:

    time.sleep(1)

    print("".join([
        "thread id: ",
        str(threading.get_ident()),
        ", thread name: ",
        threading.current_thread().name
    ]))

thread1 = threading.Thread(target=do_it, name="thread1")
thread1.start()

thread2 = threading.Thread(target=do_it, name="thread2")
thread2.start()

print("made it here")
