import functools
import time


def do_retry(retry_times=1, delay_seconds=0):
    """
    Decorator for function retry .

    @param retry_times: retry times
    @param delay_seconds: sleep time after per try
    @return: the return value of the called function
    @raise Exception: raises an exception when an error occurred after last time
    """

    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            _retry_times, _delay_seconds = retry_times, delay_seconds
            _err = None

            while _retry_times > 0:
                try:
                    _err = None
                    return f(*args, **kwargs)
                except Exception as e:
                    _err = e
                    if _delay_seconds > 0:
                        time.sleep(_delay_seconds)
                    _retry_times -= 1

            if _err:
                raise _err
        return wrapper
    return deco


def foo():
    _retry_times =3
    _delay_seconds = 1

    @do_retry(retry_times=_retry_times, delay_seconds=_delay_seconds)
    def bar():
        print "call function bar()..."

        def do_sth():
            return False

        flag = do_sth()

        if not flag:
            raise Exception("some error occur...")

        return flag

    try:
        ret = bar()
        print "ret=%d" % ret
    except Exception as e:
        print "err=%s" % e

if __name__ == "__main__":
    foo()
