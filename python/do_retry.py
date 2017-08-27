import utils

def foo():
    _retry_times =3
    _delay_seconds = 1

    @utils.do_retry(retry_times=_retry_times, delay_seconds=_delay_seconds)
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