import sys
import argparse

TLB_SIZE = 16
NUM_PAGES = 256
PAGE_SIZE = 256
DEFAULT_FRAMES = 256
# variable number of frames based off of args

PRA = 'FIFO'
REF_SEQ = []

# tlb will be a queue of dictionaries

# page number to frame number


def get_page_and_offset(logical_address):
    page_number = logical_address >> 8
    offset = logical_address & 0xFF
    return page_number, offset


def parse_args():
    # file name, frame number, page replacement algorithm
    if len(sys.argv) == 3:
        # open file name, store it as an array in ref_seq
        # default_frames = second arg
        # DEFALT_pra = third arg
        # return ()
        # else if len ==2 :
        # check if second arg is num => set default frames
        # if not num, set pra


def main():

    parser = argparse.ArgumentParser(description='memSim')

    args = parser.parse_args()

    return 0


if __name__ == "__main__":
    sys.exit(main())
