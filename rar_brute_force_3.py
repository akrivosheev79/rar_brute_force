import multiprocessing
import argparse

import rarfile
import time
from itertools import product
from tqdm import tqdm
from functools import partial


def check_password(password, rar_file):
    rf = rarfile.RarFile(rar_file)

    try:
        rf.testrar(password)
        return True, password
    except rarfile.BadRarFile:
        return False, password
    except KeyboardInterrupt:
        return False, password


def update(*a):
    pbar.update()


def init_alph():
    with open('alph.txt', 'r') as f:
        lines = f.readlines()
        if len(lines) != 1:
            raise Exception('Invalid format of alph.txt. Must be alphabet in 1 line')
        return list(lines[0].rstrip())


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser(description='Brute force rar with password')
    args_parser.add_argument('rar', help='File name for check password')
    args_parser.add_argument('pwd_len', help='Password length', type=int)
    args_parser.add_argument('--chunk_size', help='Password list chunk size. Affects to RAM!!!', default=10_000,
                             required=False, type=int)
    args = args_parser.parse_args()

    rar_file = args.rar
    pwd_len = args.pwd_len
    pwd_list_chunksize = args.chunk_size

    try:
        rf = rarfile.RarFile(rar_file)
        alph = init_alph()
    except FileNotFoundError as fe:
        print(fe)
        exit()

    pwd_alph = list(alph)
    cores = multiprocessing.cpu_count()

    start_time = time.time()

    try:
        if rf.needs_password():
            print(f'Archive need password. Will force it')

            # TODO Loop for different password length
            for current_pwd_len in range(1, pwd_len + 1):
                with multiprocessing.Pool(processes=cores) as pool:
                    pwd_list_len = pow(len(alph), current_pwd_len)

                    with tqdm(total=pwd_list_len, unit=' pwd') as pbar:
                        pwd_list = []
                        pwd_iter = product(pwd_alph, repeat=current_pwd_len)

                        counter = 0
                        for pwd in pwd_iter:
                            pwd_list.append(''.join(pwd))

                            if (
                                    len(pwd_list) >= pwd_list_chunksize) or \
                                    (len(pwd_list) == pwd_list_len) or \
                                    (len(pwd_list) + pwd_list_chunksize * counter == pwd_list_len):
                                counter += 1
                                for result, password in pool.imap_unordered(partial(check_password, rar_file=rar_file), pwd_list):
                                    if result:
                                        print(f'Password founded: {password}')
                                        pool.close()
                                        break
                                    pbar.set_description(f'Current lenght: {current_pwd_len} Current password: {password}')
                                    pbar.update()

                                pwd_list.clear()
        else:
            print(f'Archive doesn\'t need password')
    except KeyboardInterrupt:
        pool.terminate()
        print('Interrupted by user')
    finally:
        print("--- Completed for %s seconds ---" % (time.time() - start_time))


