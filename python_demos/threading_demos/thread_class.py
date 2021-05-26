""" thread class demo """

import threading

class DoItThread(threading.Thread):
    """ do it thread class """

    def __init__(self, msg: str):
        threading.Thread.__init__(self)
        self.msg = msg

    def run(self) -> None:

        print("do it thread id: " + str(threading.get_ident()))

        print(self.msg)
        self.whoami()

    def whoami(self) -> None:
        print("whoami thread id: " + str(threading.get_ident()))


print("main thread id: " + str(threading.get_ident()))


some_thread = DoItThread("this is cool")
some_thread.start()

some_thread.whoami()

some_thread.join()
