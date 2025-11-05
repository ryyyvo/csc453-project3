import sys
import argparse
from queue import Queue
from collections import deque
  

# variable number of frames based off of args

ADDS = [] #addresses from file
SEQ = [] #all of them translated to their page number
CURRENT_INDEX = 0 # tracks current position in SEQ for optimal algorithm

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

def optimal(queue_page_table, queue_tlb, page_num):
    global CURRENT_INDEX
    
    page_table_keys = [page for page, frame in queue_page_table]
    
    farthest_use = -1
    page_to_replace = None
    
    for page, frame in queue_page_table:
        # look for next occurrence of this page
        next_use = None
        for i in range(CURRENT_INDEX + 1, len(SEQ)):
            if SEQ[i] == page:
                next_use = i
                break
        
        # if page is never used again, replace it
        if next_use is None:
            page_to_replace = (page, frame)
            break
        
        # track page that will be used farthest in the future
        if next_use > farthest_use:
            farthest_use = next_use
            page_to_replace = (page, frame)
    
    queue_page_table.remove(page_to_replace)
    if page_to_replace in queue_tlb:
        queue_tlb.remove(page_to_replace)
    
    new_frame_num = page_to_replace[1]

    queue_page_table.append((page_num, new_frame_num))
    
    return new_frame_num

def lru(queue_page_table, queue_tlb, page_num):
    global CURRENT_INDEX
    
    least_recent_use = CURRENT_INDEX
    page_to_replace = None
    
    for page, frame in queue_page_table:
        last_use = -1
        for i in range(CURRENT_INDEX - 1, -1, -1):
            if SEQ[i] == page:
                last_use = i
                break

        # track page that was used least recently
        if last_use < least_recent_use:
            least_recent_use = last_use
            page_to_replace = (page, frame)
    
    queue_page_table.remove(page_to_replace)
    if page_to_replace in queue_tlb:
        queue_tlb.remove(page_to_replace)
    
    new_frame_num = page_to_replace[1]
    
    queue_page_table.append((page_num, new_frame_num))
    
    return new_frame_num


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
    global CURRENT_INDEX
    TLB_SIZE = 16
    NUM_PAGES = 256
    PAGE_SIZE = 256
    PAGE_TABLE_SIZE = 256
    DEFAULT_FRAMES = 256
    DEFAULT_PRA = 'fifo'
    FRAME_COUNTER = 0
    TLB_COUNTER=0
    TLB_MISS=0
    PAGE_TABLE_MISS=0
    ADDS_TRANSLATED=0
    
    #parser = argparse.ArgumentParser(description='memSim')

    #args = parser.parse_args()
    ADDS = [256, 512, 768, 1024, 1280, 1536, 256, 512, 1792, 768]
    #PAGE_TABLE = Queue()
    #TLB = Queue()
    
    PAGE_TABLE = []
    TLB = []
    
    for address in ADDS:
        page_num, offset = get_page_and_offset(address)
        SEQ.append(page_num)
    
    print("sequence page numbers", SEQ)
    

  
    for idx, address in enumerate(ADDS):
        CURRENT_INDEX = idx
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
                   
                #next_frame_num = FRAME_COUNTER
                FRAME_COUNTER+=1 
                     
            else:
                if DEFAULT_PRA == 'fifo':
                    new_frame = fifo_page_table(PAGE_TABLE, TLB, page_num)
                elif DEFAULT_PRA == 'optimal':
                    new_frame = optimal(PAGE_TABLE, TLB, page_num)
                elif DEFAULT_PRA == 'lru':
                    new_frame = lru(PAGE_TABLE, TLB, page_num)
              
                    
            if TLB_COUNTER<TLB_SIZE:
                    TLB.append((page_num,new_frame))
                    
                    TLB_COUNTER+=1
            else:
                    #call fifo on tlb
                    fifo_tlb(TLB, page_num, new_frame)
                    
                
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
    # sys.exit(main())
    main()
