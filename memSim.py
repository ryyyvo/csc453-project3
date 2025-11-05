#!/usr/bin/env python3
import sys
import argparse
import numpy as np
from queue import Queue
from collections import deque
  

# variable number of frames based off of args





ADDS = [] #addresses from file
SEQ = [] #all of them translated to their page number

DEFAULT_FRAMES = 256
DEFAULT_PRA = 'fifo'
PAGE_TO_FRAME_DICT = {}
TLB_SIZE = 16
NUM_PAGES = 256
PAGE_SIZE = 256
PAGE_TABLE_SIZE = 256
    
FRAME_COUNTER = 0
TLB_COUNTER=0
TLB_MISS=0
PAGE_TABLE_MISS=0
ADDS_TRANSLATED=0

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

def fifo_tlb(queue, page_num, frame_num):
    popped = queue.pop(0)
    queue.append((page_num, frame_num))

def fifo_page_table(queue_page_table,queue_tlb, page_num):
    popped = queue_page_table.pop(0)
    queue_tlb.remove(popped)
    new_frame_num = popped[1]
    queue_page_table.append((page_num, new_frame_num))
    return new_frame_num

def optimal(queue_page_table,queue_tlb, page_num):
    page_table_keys = []#all the page numbers in the page table
    copy_SEQ = SEQ 
    #ADDRESES_TRANS = index in SEQ that you are currently at
    # start iterating through the rest of the list(for loop until you hit the end of copy_seq)
    # remove whatever you encounter from PAGE_TABLE_KEYS 
    
    #use get_frame to find page number and frame tuple <= remove it from page_table_queue and queue_tlb
    #get_frame_from_queue(page_table, page_num)
    #add the new tuple to page table and tlb
 
    


    


def parse_args():
    global ADDS, DEFAULT_FRAMES, DEFAULT_PRA
    # file name, frame number, page replacement algorithm
    with open('addresses.txt', 'r') as file:
            ADDS = [int(line.strip()) for line in file]
        
    for i in range(len(ADDS)):
        ADDS[i] = int(ADDS[i])
            
    if len(sys.argv) == 4:
        print("hi")
    
        DEFAULT_FRAMES = int(sys.argv[2])
        DEFAULT_PRA = str(sys.argv[3])
    
    elif len(sys.argv) == 3:
        #if isinstance(sys.argv[2],int):
        if sys.argv[2].isdigit():
            DEFAULT_FRAMES = int(sys.argv[2])
        else:
            DEFAULT_PRA = str(sys.argv[2])
    
    print("frames", DEFAULT_FRAMES)
    print("pra", DEFAULT_PRA)
    print("adds", ADDS)
        
                    
        # open file name, store it as an array in ref_seq
        # default_frames = second arg
        # DEFALT_pra = third arg
        # return ()
        # else if len ==2 :
        # check if second arg is num => set default frames
        # if not num, set pra
    return 0

def read_page_from_backing_store(address, page_num):
    
    offset = page_num * PAGE_SIZE
   
    with open("BACKING_STORE.bin", "rb") as f:
        f.seek(offset)
        data = f.read(PAGE_SIZE)
    return(data.hex().upper())

def read_byte_from_backing_store(address, page_num):
    offset = page_num * PAGE_SIZE
    with open("BACKING_STORE.bin", "rb") as f:
        f.seek(address)
        data = f.read(1)
    return(int.from_bytes(data, 'big'))



def main():
    global TLB_SIZE, NUM_PAGES, PAGE_SIZE,PAGE_TABLE_SIZE,FRAME_COUNTER,TLB_COUNTER,TLB_MISS,PAGE_TABLE_MISS,ADDS_TRANSLATED
    
    parse_args()

    
    #have to make global...?
    PAGE_TABLE = []
    TLB = []
    
    for address in ADDS:
        page_num, offset = get_page_and_offset(address)
        SEQ.append(page_num)
    
    print("sequence page numbers", SEQ)
    

    
    for address in ADDS:
        page_num, offset = get_page_and_offset(address)
        if not check_page_exist(TLB, page_num):
            if check_page_exist(PAGE_TABLE, page_num):
                TLB_MISS+=1
                frame_from_table = get_frame_from_queue(PAGE_TABLE, page_num)
                TLB.append(page_num, frame_from_table)
            
        if not check_page_exist(TLB, page_num) and not check_page_exist(PAGE_TABLE, page_num):
            PAGE_TABLE_MISS += 1
            if FRAME_COUNTER<DEFAULT_FRAMES:
                PAGE_TABLE.append((page_num, FRAME_COUNTER))
                new_frame = FRAME_COUNTER
                PAGE_TO_FRAME_DICT[page_num] = new_frame

                FRAME_COUNTER+=1 
                     
            else:
                if DEFAULT_PRA == 'fifo':
                    new_frame = fifo_page_table(PAGE_TABLE, TLB, page_num)
                    PAGE_TO_FRAME_DICT[page_num] = new_frame
                    
            if TLB_COUNTER<TLB_SIZE:
                    TLB.append((page_num,new_frame))
                    
                    TLB_COUNTER+=1
            else:
                    #call fifo on tlb
                    fifo_tlb(TLB, page_num, new_frame)
                    
            
            
            
    
    print("TLB", TLB)
    print("PAGE TABLE", PAGE_TABLE)
                
    
    
    for index, value in enumerate(ADDS):
        print(ADDS[index], end="")
        print(", ", end="")
        print(read_byte_from_backing_store(ADDS[index], SEQ[index]), end="")
        print(", ", end="")
        print(PAGE_TO_FRAME_DICT[SEQ[index]])
        print(read_page_from_backing_store(ADDS[index], SEQ[index]))
    
    print("Number of Translated Addresses = ", ADDS_TRANSLATED)
    print("Page Faults = ", PAGE_TABLE_MISS)
    print("Page Fault Rate = ??")
    print("TLB Hits = ??")
    print("TLB Misses = ", TLB_MISS)
    print("TLB Hit Rate = ??")
    

    return 0



if __name__ == "__main__":
    # sys.exit(main())
    main()
