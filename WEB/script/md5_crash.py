# md5碰撞
import multiprocessing
import datetime
import hashlib
import string
import random

CHARS = string.digits + string.ascii_letters
def cmp_md5(substr, stop_event, str_len, start=0, size=20):
    global CHARS
    while not stop_event.is_set():
        rnds = ''.join(random.choice(CHARS) for _ in range(size))
        md5 = hashlib.md5(rnds.encode())
        if md5.hexdigest()[start: start+str_len] == substr:
            print(rnds)
            stop_event.set()
if __name__ == '__main__':
    substr = 'c235b'    # md5子字符串
    start_pos = 0
    str_len = len(substr)
    cpus = multiprocessing.cpu_count()
    print(cpus)
    stop_event = multiprocessing.Event()
    processes = [multiprocessing.Process(target=cmp_md5, args=(substr,stop_event, str_len, start_pos,)) for i in range(cpus)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
