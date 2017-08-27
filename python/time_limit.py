import utils
import time


def foo():
    _timeout = 3

    @utils.time_limit(timeout=_timeout)
    def bar():
        print "call function bar()..."

        i = 0
        while i < 5:
            print i
            i += 1
            time.sleep(1)

    try:
        bar()
    except Exception as e:
        print "err=%s" % e


if __name__ == "__main__":
    foo()
