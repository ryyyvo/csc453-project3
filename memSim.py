import sys
import argparse
import numpy as np
from queue import Queue
from collections import deque
  
TLB_SIZE = 16
NUM_PAGES = 256
PAGE_SIZE = 256
DEFAULT_FRAMES = 256
FRAME_COUNTER=0
TLB_COUNTER=0
TLB_MISS=0
PAGE_TABLE_MISS=0
ADDS_TRANSLATED=0
# variable number of frames based off of args

PRA = 'FIFO'


ADDS = [] 
SEQ = [] 



# tlb will be a queue of dictionaries

# page number to frame number
def get_frame_from_queue(queue, key):
    for k, v in queue:
        if k == key:
            return v
    return None 

def check_page_exist(queue, page_num):
    return any(key == page_num for key, _ in queue)
    

def get_page_and_offset(logical_address):
    page_number = logical_address >> 8
    offset = logical_address & 0xFF
    return page_number, offset


def parse_args():
    # file name, frame number, page replacement algorithm
    if len(sys.argv) == 3:
        print("hi")
        
        with open('addresses.txt', 'r') as file:
            ADDS = file.readlines()
        
        for i in ADDS:
            ADDS[i] = int(ADDS[i])
        
        DEFAULT_FRAMES = sys.argv[2]
        DEFAULT_PRA = sys.argv[3]
    
        
                    
        # open file name, store it as an array in ref_seq
        # default_frames = second arg
        # DEFALT_pra = third arg
        # return ()
        # else if len ==2 :
        # check if second arg is num => set default frames
        # if not num, set pra
    return 0


def main():

    parser = argparse.ArgumentParser(description='memSim')

    args = parser.parse_args()
    
    PAGE_TABLE = Queue()
    TLB = Queue()
    
    for address in ADDS:
        page_num, offset = get_page_and_offset(address)
        SEQ.append(page_num)
    

        
    for address in ADDS:
        page_num, offset = get_page_and_offset(address)
        if not check_page_exist(TLB, page_num) and not check_page_exist(PAGE_TABLE, page_num) :
            PAGE_TABLE_MISS += 1
            if FRAME_COUNTER<DEFAULT_FRAMES:
                PAGE_TABLE.enqueue((page_num, FRAME_COUNTER))
                   
                if TLB_COUNTER<TLB_SIZE:
                    TLB.enqueue((page_num, FRAME_COUNTER))
                    TLB_COUNTER+=1
                else:
                    #call fifo on tlb
                    
                FRAME_COUNTER+=1 
                     
            else:
                #call DEFAULT_PRA
        #adds_translated+=1
                
            
        
        
    
    #open addresses-correct.txt
    
    #loop through addresses in REF_SEQ = []
    #for each one: 
    # get page number and offset
    # check tlb, if page number value is None check page table. if that value is also None
    # check if frame counter is less than DEFAULT_FRAMES:
    # if less: update that frame as the value for page table, and put it in TLB(may need to FIFO). frame_counter++
    # if more: FIFO, LRU, OPTIMAL. frame_counter stays the same
     
     #at end of for loop put in address read, value in backingstore.bin, frame number, whole page from backingstore.bin
    
    
    
    
    
    
    

    return 0


if __name__ == "__main__":
    sys.exit(main())
