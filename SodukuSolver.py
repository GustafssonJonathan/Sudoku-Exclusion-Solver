#!/usr/bin/python

import sys
import random
import copy

class box:
    """Contains all information for each box in the soduku.
    Initializer needs:
    id -- integer 0-80
    h_id -- horizontal_group_id integer 0-8
    v_id -- vertical_group_id integer 0-8
    box_id -- box_group_id integer 0-8 """
    def __init__(self, id, h_id, v_id, box_id):
        self.number = [1,2,3,4,5,6,7,8,9]
        self.id = id
        self.horizontal_group_id = h_id
        self.vertical_group_id = v_id
        self.box_group_id = box_id
    
    def __eq__(self, other):
        if not isinstance(other, box):
            return NotImplemented
        return (self.number == other.number and self.id == other.id 
            and self.horizontal_group_id == other.horizontal_group_id 
            and self.vertical_group_id == other.vertical_group_id
            and self.box_group_id == other.box_group_id)

def show_puzzle(boxes):
    """Displays the found values. Unknown values are shown with the number of 
    candidates and question mark.

    Input arguments:
    boxes -- list of boxes
    """
    for i, box in enumerate(boxes):
        if len(box.number) == 1:
            print(box.number, end = '')
        else:
            print(len(box.number), end = '')
            print("? ", end = '')
        if i != 0 and (i+1) % 9 == 0:
            print("")
    print("")

def show_horizontal_groups(boxes):
    """Displays all boxes with the horizontal_group id inside them.

    Input arguments:
    boxes -- list of boxes
    """
    for i, box in enumerate(boxes):
        print(box.horizontal_group_id, end = '')
        if i != 0 and (i+1) % 9 == 0:
            print("")

def show_vertical_groups(boxes):
    """Displays all boxes with the vertical_group id inside them.

    Input arguments:
    boxes -- list of boxes
    """
    for i, box in enumerate(boxes):
        print(box.vertical_group_id, end = '')
        if i != 0 and (i+1) % 9 == 0:
            print("")

def show_box_groups(boxes):
    """Displays all boxes with the box_group id inside them.

    Input arguments:
    boxes -- list of boxes
    """
    for i, box in enumerate(boxes):
        print(box.box_group_id, end = '')
        if i != 0 and (i+1) % 9 == 0:
            print("")

def set_number(boxes, i, j):
    """Set a box with id i to value j. It also restricts the entries of boxes 
    which are in the same group as box i.

    Input arguments:
    boxes -- list of boxes
    i -- id of box to be set
    j -- value set in box with id i
    """
    boxes[i].number = [j]
    remove_candidates(boxes, horizontal_groups[boxes[i].horizontal_group_id], 
                        boxes[i], j)
    remove_candidates(boxes, vertical_groups[boxes[i].vertical_group_id], 
                        boxes[i], j)
    remove_candidates(boxes, box_groups[boxes[i].box_group_id], boxes[i], j)

def remove_candidates(boxes, group, changed_box, j):
    """Removes candidates from boxes within the same group
    
    Input arguments:
    boxes -- list of boxes
    group -- list of boxes
    changed_box -- the box with an updated value
    j -- the value to remove from the groups
    """
    for box in group:
        if box != changed_box:
            try:
                box.number.remove(j)
                if len(box.number) == 1:
                    set_number(boxes, box.id, box.number[0])
            except ValueError:
                pass
    
def unique_group(group):
    """Checks a group of boxes for undecided boxes which can be determined

    Input arguments:
    group -- list of boxes
    """
    number_of_entries = [0 for _ in range(10)]
    for box in group:
        if len(box.number) != 1:
            for k in box.number:
                number_of_entries[k] += 1
    for index, value in enumerate(number_of_entries):
        if value == 1:
            for box in group:
                if index in box.number:
                    set_number(boxes, box.id, index)   
                
def is_solved(boxes):
    """Does the boxes solve the soduku.

    Input arguments:
    boxes -- list of boxes

    Output
    boolean
    """
    for box in boxes:
        if len(box.number) != 1:
            return False
    return True

def is_possible(boxes):
    """Is it possible to complete the soduku.

    Input arguments:
    boxes -- list of boxes

    Output
    boolean
    """
    for box in boxes:
        if len(box.number) == 0:
            return False
    return True

def read_file(boxes, filename):
    """Reads in the text file from https://qqwing.com/generate.html. The 
    following formats are supported, Readable, Compact, and One line.

    Input arguments:
    boxes -- list of boxes
    filename -- string with the name of the file
    """
    open_file = open(filename, 'r')
    i = 0
    j = 0
    line = open_file.read()
    while i < 81:
        try:
            if line[j].isdigit():
                set_number(boxes, i, int(line[j]))
                i += 1
            elif line[j] == '.':
                i += 1
            j += 1
        except IndexError as e:
            print("File has the wrong format")
            raise e
    open_file.close()

        

def minimum_number_of_candidates(boxes):
    """Finds the index of the boxes with the minimum number of candidates. 
    Solved boxes are ignored.

    Input arguments:
    boxes -- list of boxes
    """
    candidate_value = 9
    for i, box in enumerate(boxes):
        if len(box.number) != 1 and len(box.number) < candidate_value:
            candidate_value = len(box.number)
            candidate_index = [i]
    return candidate_index

def solve(boxes):
    """Try to complete the soduku based on the current state. Will trigger an 
    ValueException if not possible to solve from current state.

    Input arguments:
    boxes -- list of boxes
    """
    n = 0
    while not is_solved(boxes) and is_possible(boxes):
        boxes_copy = copy.deepcopy(boxes)
        for i in range(9):
            unique_group(horizontal_groups[i])
            unique_group(vertical_groups[i])
            unique_group(box_groups[i])
        n += 1
        if boxes_copy == boxes:
            break
    if not is_possible(boxes):
        raise ValueError

def unsolved_boxes(boxes):
    candidate_index = []
    for i, box in enumerate(boxes):
        if len(box.number) != 1:
            candidate_index.append(i)
    return candidate_index

def find_solution(boxes, i):
    #start with solve
    i += 1
    solve(boxes)
    if not is_solved(boxes):
        print("Guess depth:", i)
        min_index = minimum_number_of_candidates(boxes)
        boxes_copy = copy.deepcopy(boxes)
        for index in min_index:
            for value in boxes[index].number:
                try:
                    set_number(boxes, index, value)
                    find_solution(boxes, i)
                    return
                except ValueError:
                    boxes = copy.deepcopy(boxes_copy)
                    assign_groups(boxes)
        raise ValueError
    else:
        print('solved')
        show_puzzle(boxes)
        
horizontal_groups = [[] for _ in range(9)]
vertical_groups = [[] for _ in range(9)]
box_groups = [[] for _ in range(9)]

def assign_groups(boxes):
    global horizontal_groups
    global vertical_groups
    global box_groups

    horizontal_groups = [[] for _ in range(9)]
    vertical_groups = [[] for _ in range(9)]
    box_groups = [[] for _ in range(9)] 
    for box in boxes:
        horizontal_groups[box.horizontal_group_id].append(box)
        vertical_groups[box.vertical_group_id].append(box)
        box_groups[box.box_group_id].append(box)
  
if __name__ == "__main__":
    boxes = []
    for i in range(81):
        horizontal_group_id = i // 9
        vertical_group_id = i % 9
        temp = i // 27
        box_group_id = (i // 3) % 3 + temp * 3
        temp_box = box(i, horizontal_group_id, vertical_group_id, box_group_id)
        boxes.append(temp_box)
    
    assign_groups(boxes)

    read_file(boxes, sys.argv[1])

    show_puzzle(boxes)

    try:
        find_solution(boxes, 0)
    except ValueError:
        print("No solution found.")