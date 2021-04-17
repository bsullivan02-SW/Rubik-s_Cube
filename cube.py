from random import randint
import tkinter as tk
import copy, webbrowser, os
from tkinter import *
import util

#
#This is the Cube Solver
#This version contains a GUI
#Last Edited on: 12/5/2014
#Written by: Lucas Liberacki & Tom Brannan


#globals
moves_list = []
#list_of_leagal_moves[]
last_scramble = []
f2l_list = []
step_moves_list = []
solution_length = 0
possibleMoves = ["u","u2","ui","f","f2","fi","r","r2","ri","l","l2","li","b","b2","bi","d","d2","di","x","x2","xi","y","y2","yi","z","z2",
"zi","uw","uw2","uwi","m","mi","m2","rw","rwi","rw2","fw","fwi","fw2","lw","lwi","lw2","bw","bwi","bw2","dw","dwi","dw2"]

#creates a 3d list representing a solved cube
def make_cube():
    global step_moves_list, f2l_list, moves_list
    step_moves_list = [0,0,0,0]
    f2l_list = []
    moves_list = []
    return [   [['W', 'W', 'W'],
                ['W', 'W', 'W'],
                ['W', 'W', 'W']], #Up/white
               
               [['G', 'G', 'G'],
                ['G', 'G', 'G'],
                ['G', 'G', 'G']], #front/green
               
               [['R', 'R', 'R'],
                ['R', 'R', 'R'],
                ['R', 'R', 'R']], #right/red
               
               [['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O']], #left/orange
               
               [['Y', 'Y', 'Y'],
                ['Y', 'Y', 'Y'],
                ['Y', 'Y', 'Y']], #down/yellow
               
               [['B', 'B', 'B'],
                ['B', 'B', 'B'],
                ['B', 'B', 'B']]] #back/blue

a = make_cube()
#print ("make cube" , a )

#prints a string representation of the cube to the interpreter
def print_cube():
    print('\t\t'+str(a[5][0])+'\n\t\t'+str(a[5][1])+'\n\t\t'+str(a[5][2]))   
    print(str(a[3][0])+' '+str(a[0][0])+' '+str(a[2][0]))
    print(str(a[3][1])+' '+str(a[0][1])+' '+str(a[2][1]))   
    print(str(a[3][2])+' '+str(a[0][2])+' '+str(a[2][2]))
    print('\t\t'+str(a[1][0])+'\n\t\t'+str(a[1][1])+'\n\t\t'+str(a[1][2]))
    print('\t\t'+str(a[4][0])+'\n\t\t'+str(a[4][1])+'\n\t\t'+str(a[4][2]))

'''
THIS IS OUR GROUP'S CODE
'''
'''
class State:
    def __innit__(self, UF, FF, RF, LF, DF, BF):
        self.UF = UF
        self.FF = FF
        self.RF = RF
        self.LF = LF
        self.DF = DF
        self.BF = BF

    def isEqual(self, currentState):
        
        
        What we need to do is set up both cubes using the "setup" function to face the same way. Then we can check face
        equality without worrying about 6x the number of possible states. Afterwards, we can undo the setup, exactly the way he deals
        with making moves. What I'm wondering now is we can only call setup() on the cube a. There is no parameter to specifiy "which cube".
        Furthermore, the "currentState" we pass here is not a cube, just a "State". We have to find some way to face them both the same way:
        1. Can make a match the orientation of currentState (how do we find that?)
        2. Can copy a into a temp cube, transfer currentState into a and deal with all the setup exclusively in a
           (I don't think there's even a way to transfer or manually specify what a cube is)
        3. We'll probably have to edit either our code or his for this. Maybe we can make our currentState a cube and make his code
           specify which cube to setup.
        I feel like the easiest thing to do would be to setup a to face the same way as currentState, but how do we find that?
        

        setup("l")

        isEqual = False
        for currentRow in self.UF:
            for currentColumn in currentRow:
                if self.UF[currentRow][currentColumn] != currentState.UF[currentRow][currentColumn]:
                    return isEqual

        for currentRow in self.FF:
            for currentColumn in currentRow:
                if self.UF[currentRow][currentColumn] != currentState.UF[currentRow][currentColumn]:
                    return isEqual
        
        for currentRow in self.RF:
            for currentColumn in currentRow:
                if self.UF[currentRow][currentColumn] != currentState.UF[currentRow][currentColumn]:
                    return isEqual

        for currentRow in self.LF:
            for currentColumn in currentRow:
                if self.UF[currentRow][currentColumn] != currentState.UF[currentRow][currentColumn]:
                    return isEqual

        for currentRow in self.DF:
            for currentColumn in currentRow:
                if self.UF[currentRow][currentColumn] != currentState.UF[currentRow][currentColumn]:
                    return isEqual

        for currentRow in self.BF:
            for currentColumn in currentRow:
                if self.UF[currentRow][currentColumn] != currentState.UF[currentRow][currentColumn]:
                    return isEqual
        
        return True
'''   




#simplifies the list of moves and returns a string representation of the moves
def get_moves():
    simplify_moves()
    s = ""
    for i in moves_list:
        s += str(i) + " "
    s = str.replace(s, "i", "'")[:-1] 
    return s

#returns a string representation of the last scramble
def get_scramble():
    s = ""
    for i in last_scramble:
        s += str(i) + " "
    s = str.replace(s, "i", "'")[:-1]
    return s

#helper function: returns True if all elements in a set are equal
def all_same(items):
    return all(x == items[0] for x in items)

#Transforms a given move into the corresponding move after a Y-rotation
def yTransform(move):
    if move[0] in ["U", "D"]:
        return move
    if move[0] == "F":
        return "R" + move[1:]
    if move[0] == "R":
        return "B" + move[1:]
    if move[0] == "B":
        return "L" + move[1:]
    if move[0] == "L":
        return "F" + move[1:]
    raise Exception("Invalid move to yTransform: " + move)

#modifies the global moves list by removing redundancies
def simplify_moves():
    global moves_list, solution_length
    new_list = []
    prev_move = ""
    yCount = 0
    for move in moves_list:
        if move == "Y":
            yCount += 1
            yCount %= 4
            continue
        if move == "Yi":
            yCount += 3
            yCount %= 4
            continue
        if move == "Y2":
            yCount += 2
            yCount %= 4
            continue
        if yCount > 0:
            for i in range(yCount):
                move = yTransform(move)
        if prev_move == "" or prev_move == '':
            prev_move = move
            new_list.append(move)
            continue
        if move[0] == prev_move[0]:
            if len(move) == 1:
                if len(prev_move) <= 1:
                    del new_list[-1]
                    mv = move[0] + "2"
                    new_list.append(mv)
                    prev_move = mv
                    continue
                if prev_move[1] == "i":
                    del new_list[-1]
                    prev_move = new_list[-1] if len(new_list) > 0 else ""
                    continue
                if prev_move[1] == "2":
                    del new_list[-1]
                    mv = move[0] + "i"
                    new_list.append(mv)
                    prev_move = mv
                    continue
            if move[1] == "i":
                if len(prev_move) == 1:
                    del new_list[-1]
                    prev_move = new_list[-1] if len(new_list) > 0 else ""
                    continue
                if prev_move[1] == "i":
                    del new_list[-1]
                    mv = move[0] + "2"
                    new_list.append(mv)
                    prev_move = mv
                    continue
                if prev_move[1] == "2":
                    del new_list[-1]
                    mv = move[0]
                    new_list.append(mv)
                    prev_move = mv
                    continue
            if move[1] == "2":
                if len(prev_move) == 1:
                    del new_list[-1]
                    mv = move[0] + "i"
                    new_list.append(mv)
                    prev_move = mv
                    continue
                if prev_move[1] == "i":
                    del new_list[-1]
                    mv = move[0]
                    new_list.append(mv)
                    prev_move = mv
                    continue
                if prev_move[1] == "2":
                    del new_list[-1]
                    prev_move = new_list[-1] if len(new_list) > 0 else ""
                    continue
        new_list.append(move)
        prev_move = move
    solution_length = len(new_list)
    moves_list = new_list

#sets up the cube to perform a move by rotating that face to the top
def setup(face):
    face = str.lower(face)
    if face == "f":
        move("X")
    elif face == "r":
        move("Zi")
    elif face == "l":
        move("Z")
    elif face == "d":
        move("X2")
    elif face == "b":
        move("Xi")
    else:
        raise Exception("Invalid setup; face: " + face)
    

#performs the inverse of setup to restore the cube's previous orientation
def undo(face):
    face = str.lower(face)
    if face == "f":
        move("Xi")
    elif face == "r":
        move("Z")
    elif face == "l":
        move("Zi")
    elif face == "d":
        move("X2")
    elif face == "b":
        move("X")
    else:
        raise Exception("Invalid undo; face: " + face)
#:)
#Tokenizes a string of moves 	
def m(s):
    s = str.replace(s, "'", "i")
    k = s.split(' ')
    global moves_list, solution_length
    solution_length += len(k)
    for word in k:
        moves_list.append(word)
        move(word)

#performs a move by setting up, performing U moves, and undoing the setup
# This is what we can call to choose what move we need to proform
def move(mv):
    mv = str.lower(mv)
    if mv == "u":
        U()
    elif mv == "u2":
        move("U"); move("U")
    elif mv == "ui":
        move("U"); move("U"); move("U")
    elif mv == "f":
        setup("F"); U(); undo("F")
    elif mv == "f2":
        move("F"); move("F")
    elif mv == "fi":
        move("F"); move("F"); move("F")
    elif mv == "r":
        setup("R"); U(); undo("R")
    elif mv == "r2":
        move("R"); move("R")
    elif mv == "ri":
        move("R"); move("R"); move("R")
    elif mv == "l":
        setup("L"); U(); undo("L")
    elif mv == "l2":
        move("L"); move("L")
    elif mv == "li":
        move("L"); move("L"); move("L")
    elif mv == "b":
        setup("B"); U(); undo("B")
    elif mv == "b2":
        move("B"); move("B")
    elif mv == "bi":
        move("B"); move("B"); move("B")
    elif mv == "d":
        setup("D"); U(); undo("D")
    elif mv == "d2":
        move("D"); move("D")
    elif mv == "di":
        move("D"); move("D"); move("D")
    elif mv == "x":
        rotate("X")
    elif mv == "x2":
        move("X"); move("X")
    elif mv == "xi":
        move("X"); move("X"); move("X")
    elif mv == "y":
        rotate("Y")
    elif mv == "y2":
        move("Y"); move("Y")
    elif mv == "yi":
        move("Y"); move("Y"); move("Y")
    elif mv == "z":
        rotate("Z")
    elif mv == "z2":
        move("Z"); move("Z")
    elif mv == "zi":
        move("Z"); move("Z"); move("Z")
    elif mv == "uw":
        move("D"); move("Y")
    elif mv == "uw2":
        move("UW"); move("UW")
    elif mv == "uwi":
        move("UW"); move("UW"); move("UW")
    elif mv == "m":
        move("Li"); move("R"); move("Xi")
    elif mv == "mi":
        move("M"); move("M"); move("M")
    elif mv == "m2":
        move("M"); move("M")
    elif mv == "rw":
        move("L"); move("X")
    elif mv == "rwi":
        move("RW"); move("RW"); move("RW")
    elif mv == "rw2":
        move("RW"); move("RW")
    elif mv == "fw":
        move("Bi"); move("Z")
    elif mv == "fwi":
        move("FW"); move("FW"); move("FW")
    elif mv == "fw2":
        move("FW"); move("FW")
    elif mv == "lw":
        move("R"); move("Xi")
    elif mv == "lwi":
        move("LW"); move("LW"); move("LW")
    elif mv == "lw2":
        move("LW"); move("LW")
    elif mv == "bw":
        move("F"); move("Zi")
    elif mv == "bwi":
        move("BW"); move("BW"); move("BW")
    elif mv == "bw2":
        move("BW"); move("BW")
    elif mv == "dw":
        move("U"); move("Yi")
    elif mv == "dwi":
        move("DW"); move("DW"); move("DW")
    elif mv == "dw2":
        move("DW"); move("DW")
    else:
        raise Exception("Invalid Move: " + str(mv))

#rotates the entire cube along a particular axis
def rotate(axis):
    axis = str.lower(axis)
    if axis == 'x': #R
        temp = a[0]
        a[0] = a[1]
        a[1] = a[4]
        a[4] = a[5]
        a[5] = temp
        rotate_face_counterclockwise("L")
        rotate_face_clockwise("R")
    elif axis == 'y': #U
        temp = a[1]
        a[1] = a[2]
        a[2] = a[5]
        a[5] = a[3]
        a[3] = temp
        #after swaps,
        rotate_face_clockwise("L")
        rotate_face_clockwise("F")
        rotate_face_clockwise("R")
        rotate_face_clockwise("B")
        rotate_face_clockwise("U")
        rotate_face_counterclockwise("D")
    elif axis == 'z': #F
        temp = a[0]
        a[0] = a[3]
        a[3] = a[4]
        a[4] = a[2]
        a[2] = temp
        rotate_face_clockwise("L"); rotate_face_clockwise("L")
        rotate_face_clockwise("D"); rotate_face_clockwise("D")
        rotate_face_clockwise("F")
        rotate_face_counterclockwise("B")
    else:
        raise Exception("Invalid rotation: " + axis)

#performs a U move  a U move is  ##########################
def U():
    #rotate U face
    temp = a[0][0][0]
    a[0][0][0] = a[0][2][0]
    a[0][2][0] = a[0][2][2]
    a[0][2][2] = a[0][0][2]
    a[0][0][2] = temp
    temp = a[0][0][1]
    a[0][0][1] = a[0][1][0]
    a[0][1][0] = a[0][2][1]
    a[0][2][1] = a[0][1][2]
    a[0][1][2] = temp

    #rotate others
    temp = a[5][2][0]
    a[5][2][0] = a[3][2][2]
    a[3][2][2] = a[1][0][2]
    a[1][0][2] = a[2][0][0]
    a[2][0][0] = temp
    temp = a[5][2][1]
    a[5][2][1] = a[3][1][2]
    a[3][1][2] = a[1][0][1]
    a[1][0][1] = a[2][1][0]
    a[2][1][0] = temp
    temp = a[5][2][2]
    a[5][2][2] = a[3][0][2]
    a[3][0][2] = a[1][0][0]
    a[1][0][0] = a[2][2][0]
    a[2][2][0] = temp

#Rotates a particular face counter-clockwise
def rotate_face_counterclockwise(face):
    rotate_face_clockwise(face)
    rotate_face_clockwise(face)
    rotate_face_clockwise(face)

#Rotates a particular face clockwise
def rotate_face_clockwise(face):
    f_id = -1
    face = str.lower(face)
    if face == "u":
        f_id = 0
    elif face == "f":
        f_id = 1
    elif face == "r":
        f_id = 2
    elif face == "l":
        f_id = 3
    elif face == "d":
        f_id = 4
    elif face == "b":
        f_id = 5
    else:
        raise Exception("Invalid face: " + face)


     ########################## this is changing th cube ##############
    temp = a[f_id][0][0] 
    a[f_id][0][0] = a[f_id][2][0]
    a[f_id][2][0] = a[f_id][2][2]
    a[f_id][2][2] = a[f_id][0][2]
    a[f_id][0][2] = temp
    temp = a[f_id][0][1]
    a[f_id][0][1] = a[f_id][1][0]
    a[f_id][1][0] = a[f_id][2][1]
    a[f_id][2][1] = a[f_id][1][2]
    a[f_id][1][2] = temp

#Randomly scrambles the cube given a number of moves, or given a list of moves
def scramble(moves):     # we can change this to whatever we want but it dosent seem to work
    global last_scramble, moves_list, solution_length, a
    a = make_cube()
    if hasattr(moves, '__iter__'): #scramble given a list of moves
        m(moves)
        moves_list = []
        solution_length = 0
        temp = moves.split(' ')
        last_scramble = temp
    else: #scramble randomly a certain number of times
        moves_list = [] #reset moves_list
        last_scramble = [] #reset last scramble
        prevMove = ""
        i=0
        for i in range(moves):
            while True:
                thisMove = ""
                r = randint(0, 5)
                if r == 0:
                    thisMove += "U"   # If there is say a U2 it would move U two times but only count as 1 move
                elif r == 1:
                    thisMove += "F"
                elif r == 2:
                    thisMove += "R"
                elif r == 3:
                    thisMove += "L"
                elif r == 4:
                    thisMove += "D"
                elif r == 5:
                    thisMove += "B"
                if thisMove == "U" and prevMove != "U" and prevMove != "D": # this makes sure that while we scramble we wont unscramble
                    break
                if thisMove == "F" and prevMove != "F" and prevMove != "B":
                    break
                if thisMove == "R" and prevMove != "R" and prevMove != "L":
                    break
                if thisMove == "L" and prevMove != "L" and prevMove != "R":
                    break
                if thisMove == "D" and prevMove != "D" and prevMove != "U":
                    break
                if thisMove == "B" and prevMove != "B" and prevMove != "F":
                    break
            r = randint(0, 3)
            if r == 1:
                move(thisMove + "i")
                last_scramble.append(thisMove + "i")
            elif r == 2:
                move(thisMove + "2")
                last_scramble.append(thisMove + "2")
            else:
                move(thisMove)
                last_scramble.append(thisMove)
            prevMove = thisMove

def isSolved():
    uside = a[0][0][0] == a[0][0][1] == a[0][0][2] == a[0][1][0] == a[0][1][1] == a[0][1][2] == a[0][2][0] == a[0][2][1] == a[0][2][2]
    fside = a[1][0][0] == a[1][0][1] == a[1][0][2] == a[1][1][0] == a[1][1][1] == a[1][1][2] == a[1][2][0] == a[1][2][1] == a[1][2][2]
    rside = a[2][0][0] == a[2][0][1] == a[2][0][2] == a[2][1][0] == a[2][1][1] == a[2][1][2] == a[2][2][0] == a[2][2][1] == a[2][2][2]
    lside = a[3][0][0] == a[3][0][1] == a[3][0][2] == a[3][1][0] == a[3][1][1] == a[3][1][2] == a[3][2][0] == a[3][2][1] == a[3][2][2]
    dside = a[4][0][0] == a[4][0][1] == a[4][0][2] == a[4][1][0] == a[4][1][1] == a[4][1][2] == a[4][2][0] == a[4][2][1] == a[4][2][2]
    bside = a[5][0][0] == a[5][0][1] == a[5][0][2] == a[5][1][0] == a[5][1][1] == a[5][1][2] == a[5][2][0] == a[5][2][1] == a[5][2][2]
    return uside and fside and rside and lside and dside and bside

# ANDRES, BRADY, TIANNA CODE GOES HERE


#class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    You do not need to change anything in this class, ever.
    """

def getStartState():
    """
    Returns the start state for the search problem.
    """
    
    currentCube = a

    return currentCube

def isGoalState(state):
    """
        state: Search state
    Returns True if and only if the state is a valid goal state.
    """
    isgState = False
    goalState = make_cube()
    if state == goalState:
        isgState = True
    return isgState

def getSuccessors(state):

    '''
    4/3/2021 7:32 PM: latest session (Tianna/Andres)
    If we get this to work with the code we may be able to get it to solve. Hopefully.
    '''

    """
        state: Search state
    For a given state, this should return a list of triples, (successor,
    action, stepCost), where 'successor' is a successor to the current
    state, 'action' is the action required to get there, and 'stepCost' is
    the incremental cost of expanding to that successor.
    """
    successors = []
    
    for currentMove in possibleMoves:
        saveA = a
        move(currentMove)
        successors.append(a)
        a = saveA
    return successors #return a list of successsors (states)

'''
# this if for only one move
def getMove(tate):
    themovelist = ["u","u2","ui","f","f2","fi","r","ri","l","l2","li","b","d","d2","di","x","x2","xi","y","y2","yi","z","z2","zi","uw","uw2","uwi","m","mi","m2","rw","rwi","rw2","fw","fwi","fw2","lw","lwi","lw2","bw","bwi","bw2","dw","dwi","dw2"]
    bestMove = ""
    for mv in moves_list:
        succState =  move(mv) # state after the move is applied to the move
        if isGoalState(succState): # true (succState is the goal state)
            bestMove = mv # this is the move that got us to the goal state
            break
    return bestMove
    '''





'''

NEXT STEP:
Make Tianna's BFS code and graphSearch code work with my idea of a rubrik's cube state representation.
For example, problem isn't defined in this repository. I think if we just copy the problem class
over to this repository and incorporate my state representation we might be able to straight up make this work.

'''

'''
def graphSearch(frontier, problem):
    explored = set() #Initialize explored to be empty
    while(not frontier.isEmpty()): #While the frontier is not empty
        (nextNode, actions, cost) = frontier.pop() #Remove a leaf node from the frontier
        if nextNode not in explored:
            if(problem.isGoalState(nextNode)): #If the leaf node contains a goal state
                explored.add(nextNode) #add the goal state onto explored
                return actions #Return the solution
            else: #The leaf node is not a goal state 
                explored.add(nextNode) #add the leaf node onto explored
                successors = problem.getSuccessors(nextNode) # get successors
                for (state, action, costOfAction) in successors :
                    frontier.push((state, actions + [action], cost + costOfAction))
'''

def graphSearch(frontier):
    explored = set() #Initialize explored to be empty
    while(not frontier.isEmpty()): #While the frontier is not empty
        (nextNode, cost) = frontier.pop() #Remove a leaf node from the frontier
        t = tuple(nextNode)
        if t not in explored:
            if(isGoalState(nextNode)): #If the leaf node contains a goal state
                explored.add(nextNode) #add the goal state onto explored
                return 0 #Return the solution
            else: #The leaf node is not a goal state 
                explored.add(nextNode) #add the leaf node onto explored
                successors = getSuccessors(nextNode) # get successors
                for (state, costOfAction) in successors :
                    frontier.push((state, cost + costOfAction))
                   
    return print('Failure!') #If the frontier is empty return failure

def BFS():    
    frontier = util.Queue()
    frontier.push((getStartState(), 0))
    return graphSearch(frontier)
# this is only for one move scrambels

def solve():
    
    '''
    ORIGINAL SOLVE CODE
    
    
    cross()
    simplify_moves()
    step_moves_list[0] = solution_length
    f2l()
    simplify_moves()
    step_moves_list[1] = solution_length - step_moves_list[0]
    topCross()
    getfish()
    bOLL()
    simplify_moves()
    step_moves_list[2] = solution_length - step_moves_list[1] - step_moves_list[0]
    bPLL()
    simplify_moves()
    step_moves_list[3] = solution_length - step_moves_list[2] - step_moves_list[1] - step_moves_list[0]
    assert(isSolved())
    '''

    

    BFS()
    simplify_moves()
    step_moves_list[0] = solution_length
    assert(isSolved())

    '''
    DFS()
    simplify_moves()
    step_moves_list[0] = solution_length
    assert(isSolved())

    A*()
    simplify_moves()
    step_moves_list[0] = solution_length
    assert(isSolved())
    '''

    


#Performs solve simulations, will return a list with the number of moves, which one was the best
# and the scramble used to get the best. The worst, which one was the worst, and the scramble
# used to get the worst. scimNum is the number of simulations to perform, it is an IntVar()
def simulation(simNum):
    global a
    bestScram = []
    worstScram = []
    best = 200
    worst = 0
    Bestnumber = 0
    WorstNumber = 0
    if simNum.get() >= 50000:
        print("Don't do over 50,000 solves at once")
        return
    for i in range(simNum.get()):
        a = make_cube()
        step_moves_list = [0,0,0,0]
        f2l_list = []
        moves_list = []
        last_scramble=[]
        scramble(25)
        solve()
        simplify_moves()
        if solution_length < best:
            best = solution_length
            bestScram = get_scramble()
            BestNumber = i
        if solution_length > worst:
            worst = solution_length
            worstScram = get_scramble()
            WorstNumber = i
    return [best, BestNumber, bestScram, worst, WorstNumber, worstScram]
   

############################################################# GUI #########################################################################
######################################################################################################
#Below is all the work for the GUI portion of the Cube Solver     
######################################################################################################
#These are all the globals used for the GUI
root = None
frame = None
canvas = None
ScrambleLabel = None
SolutionLabel = None
SolutionNumberLabel = None
isTransparent = None
F2LNumberLabel = None
CrossNumberLabel = None
OLLNumberLabel = None
PLLNumberLabel = None
SimulateBestLabel = None
SimulateWorstLabel = None

#cubePoints are all of the x and y coordinates for the polygons used for the tiles
def cubePoints():
    #h and w may be changed to allow the cube to be moved around the screen
    h = 125
    w = 115
    #right face
    #layer 1
    r00p = [0+w, 0+h, 0+w, 50+h, 33+w, 30+h, 33+w, -20+h]
    r01p = [33+w, -20+h, 33+w, 30+h, 66+w, 10+h, 66+w, -40+h]
    r02p = [66+w, -40+h, 66+w, 10+h, 99+w, -10+h, 99+w, -60+h]
    #layer 2
    r10p = [0+w, 50+h, 0+w, 100+h, 33+w, 80+h, 33+w, 30+h]
    r11p = [33+w, 30+h, 33+w, 80+h, 66+w, 60+h, 66+w, 10+h]
    r12p = [66+w, 10+h, 66+w, 60+h, 99+w, 40+h, 99+w, -10+h]
    #layer 3
    r20p = [0+w, 100+h, 0+w, 150+h, 33+w, 130+h, 33+w, 80+h]
    r21p = [33+w, 80+h, 33+w, 130+h, 66+w, 110+h, 66+w, 60+h]
    r22p = [66+w, 60+h, 66+w, 110+h, 99+w, 90+h, 99+w, 40+h]
    #left face (left face will be front face, however called l face to distinguish between the left and right)
    #layer 1
    l00p = [-66+w, -40+h, -66+w, 10+h, -99+w, -10+h, -99+w, -60+h]
    l01p = [-33+w, -20+h, -33+w, 30+h, -66+w, 10+h, -66+w, -40+h]
    l02p = [0+w, 0+h, 0+w, 50+h, -33+w, 30+h, -33+w, -20+h]
    #layer 2
    l10p = [-66+w, 10+h, -66+w, 60+h, -99+w, 40+h, -99+w, -10+h]
    l11p = [-33+w, 30+h, -33+w, 80+h, -66+w, 60+h, -66+w, 10+h]
    l12p = [0+w, 50+h, 0+w, 100+h, -33+w, 80+h, -33+w, 30+h]
    #layer 3
    l20p = [-66+w, 60+h, -66+w, 110+h, -99+w, 90+h, -99+w, 40+h]
    l21p = [-33+w, 80+h, -33+w, 130+h, -66+w, 110+h, -66+w, 60+h]
    l22p = [0+w, 100+h, 0+w, 150+h, -33+w, 130+h, -33+w, 80+h]
    #up face
    #layer 1
    u00p = [0+w, -75+h, -33+w, -94+h, 0+w, -111+h, 33+w, -94+h]
    u01p = [36+w, -57+h, 0+w, -75+h, 33+w, -94+h, 69+w, -76+h]
    u02p = [66+w, -40+h, 36+w, -57+h, 69+w, -76+h, 99+w, -60+h]
    #layer 2
    u10p = [-33+w, -57+h, -66+w, -77+h, -33+w, -94+h, 0+w, -75+h]
    u11p = [0+w, -38+h, -33+w, -57+h, 0+w, -75+h, 36+w, -57+h]
    u12p = [33+w, -20+h, 0+w, -38+h, 36+w, -57+h, 66+w, -40+h]
    #layer 3
    u20p = [-66+w, -40+h, -99+w, -60+h, -66+w, -77+h, -33+w, -57+h]
    u21p = [-33+w, -20+h, -66+w, -40+h, -33+w, -57+h, 0+w, -38+h]
    u22p = [0+w, 0+h, -33+w, -20+h, 0+w, -38+h, 33+w, -20+h]

    dh = h + 200
    dw = w
    #d face
    #layer 1
    d00p = [0+dw, -75+dh, -33+dw, -94+dh, 0+dw, -111+dh, 33+dw, -94+dh]
    d01p = [36+dw, -57+dh, 0+dw, -75+dh, 33+dw, -94+dh, 69+dw, -76+dh]
    d02p = [66+dw, -40+dh, 36+dw, -57+dh, 69+dw, -76+dh, 99+dw, -60+dh]
    #layer 2
    d10p = [-33+dw, -57+dh, -66+dw, -77+dh, -33+dw, -94+dh, 0+dw, -75+dh]
    d11p = [0+dw, -38+dh, -33+dw, -57+dh, 0+dw, -75+dh, 36+dw, -57+dh]
    d12p = [33+dw, -20+dh, 0+dw, -38+dh, 36+dw, -57+dh, 66+dw, -40+dh]
    #layer 3
    d20p = [-66+dw, -40+dh, -99+dw, -60+dh, -66+dw, -77+dh, -33+dw, -57+dh]
    d21p = [-33+dw, -20+dh, -66+dw, -40+dh, -33+dw, -57+dh, 0+dw, -38+dh]
    d22p = [0+dw, 0+dh, -33+dw, -20+dh, 0+dw, -38+dh, 33+dw, -20+dh]
    
    return [    [[u00p, u01p, u02p],
                 [u10p, u11p, u12p],
                 [u20p, u21p, u22p]], #Upside

                [[l00p, l01p, l02p],
                 [l10p, l11p, l12p],
                 [l20p, l21p, l22p]], #front face (used l to denote the left showing face)

                [[r02p, r12p, r22p],
                 [r01p, r11p, r21p],
                 [r00p, r10p, r20p]], # right face (different than other faces because it is formatted differently)

                [[d20p, d21p, d22p],
                 [d10p, d11p, d12p],
                 [d00p, d01p, d02p]]] #downside

def clickCanvas(canvas):
    global isTransparent
    isTransparent = not isTransparent
    canvas.delete(ALL)
    drawCube()


#DrawCanvas will take the root and draw a new canvas, also returning it.
def drawCanvas(root):
    canvas=tk.Canvas(root, width=225, height=330, background='white')
    canvas.grid(row=0,column=0)
    canvas.bind("<Button-1>", lambda e: clickCanvas(canvas))
    return canvas

#Used to get the word for each color, used in drawCube(canvas()
def getColor(element):
    if element == 'B':
        return "#06F" #Nice shade of blue
    elif element == 'W':
        return "white"
    elif element == 'G':
        return "green"
    elif element == 'Y':
        return "yellow"
    elif element == 'O':
        return "orange"
    elif element == 'R':
        return "#D11"

#drawCube() will take the already created canvas and draw the cube with polygons whose points are defined in cubePoints()
def drawCube():
    global isTransparent, canvas
    pts = cubePoints()
    for j in range(3):
        for k in range(3):
            canvas.create_polygon(pts[3][j][k], fill=getColor(a[4][j][k]), outline="#000", width=2)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if isTransparent:
                    frontTiles = (i == 1) and ((j == 1 and k == 2) or (j == 2 and k == 2) or (j == 2 and k == 1))
                    rightTiles = (i == 2) and ((j == 1 and k == 2) or (j == 2 and k == 2) or (j == 2 and k == 1))
                    if  frontTiles or rightTiles:
                        canvas.create_polygon(pts[i][j][k], fill="", outline="#000", width=2)
                    else:
                        canvas.create_polygon(pts[i][j][k], fill=getColor(a[i][j][k]), outline="#000", width=2)
                else:
                    canvas.create_polygon(pts[i][j][k], fill=getColor(a[i][j][k]), outline="#000", width=2)

# Used to create a new instance of a cube to be solved, changes scramble and solution labels as well
def GUInewCube():
    global canvas, ScrambleLabel, SolutionLabel, SolutionNumberLabel, a, step_moves_list
    global PLLNumberLabel,F2LNumberLabel, CrossNumberLabel,OLLNumberLabel, f2l_list, moves_list
    step_moves_list = [0,0,0,0]
    a = make_cube()
    f2l_list = []
    moves_list = []
    ScrambleLabel.configure(text="Scramble will be displayed here")
    SolutionLabel.configure(text="Solution will be displayed here")
    SolutionNumberLabel.configure(text=0)
    CrossNumberLabel.configure(text=step_moves_list[0])
    F2LNumberLabel.configure(text=step_moves_list[1])
    OLLNumberLabel.configure(text=step_moves_list[2])
    PLLNumberLabel.configure(text=step_moves_list[3])
    canvas.delete(ALL)
    drawCube()

#GUImakeMove is used to make moves based on what is in the EntryBox. After clicking Draw, it will redraw the canvas with the updated cube
def GUImakeMove(move):
    global canvas
    if move.get() == "":
        return
    m(move.get())
    canvas.delete(ALL)
    drawCube()

#GUIScramble will do a scramble of 25 on the cube, then update the canvas with the new cube
def GUIScramble():
    global ScrambleLabel, canvas
    #scramble(25)
    scramble(1)
    ScrambleLabel.configure(text=get_scramble())
    canvas.delete(ALL)
    drawCube()

#Used to allow user to enter in their own scramble in the Entry, will display scramble in scramble label as well
def GUIcustomScramble(scram):
    global ScrambleLabel, canvas
    if scram.get() == "":
        ScrambleLabel.configure(text="Scramble will be displayed here")
        return
    scramble(scram.get())
    ScrambleLabel.configure(text=get_scramble())
    canvas.delete(ALL)
    drawCube()

#GUISolve will wolve the cube using the solve function, then update the canvas with the new, solved, cube
def GUISolve():
    global canvas, SolutionLabel, SolutionNumberLabel, step_moves_list
    global PLLNumberLabel,F2LNumberLabel, CrossNumberLabel,OLLNumberLabel
    solve()
    SolutionLabel.configure(text=get_moves())
    SolutionNumberLabel.configure(text=solution_length)
    CrossNumberLabel.configure(text=step_moves_list[0])
    F2LNumberLabel.configure(text=step_moves_list[1])
    OLLNumberLabel.configure(text=step_moves_list[2])
    PLLNumberLabel.configure(text=step_moves_list[3])
    canvas.delete(ALL)
    drawCube()

# This will allow the user to go through the solve one step at a time, the parameter step should be
#either cross, f2l, OLL, or PLL. Depending on it, it will do a different step
def GUIsetSolve(step):
    global SolutionLabel, SolutionNumberLabel, canvas, step_moves_list
    global PLLNumberLabel,F2LNumberLabel, CrossNumberLabel,OLLNumberLabel
    if step == "cross":
        cross()
        simplify_moves()
        step_moves_list[0] = solution_length
    elif step == "f2l" or step == "F2L":
        f2l()
        simplify_moves()
        step_moves_list[1] = solution_length - step_moves_list[0]
    elif step == "OLL":
        topCross()
        getfish
        bOLL()
        simplify_moves()
        step_moves_list[2] = solution_length - step_moves_list[1] - step_moves_list[0]
    elif step == "PLL":
        bPLL()
        simplify_moves()
        step_moves_list[3] = solution_length - step_moves_list[2] - step_moves_list[1] - step_moves_list[0]
        assert(isSolved())
        
    SolutionLabel.configure(text=get_moves())
    SolutionNumberLabel.configure(text=solution_length)
    CrossNumberLabel.configure(text=step_moves_list[0])
    F2LNumberLabel.configure(text=step_moves_list[1])
    OLLNumberLabel.configure(text=step_moves_list[2])
    PLLNumberLabel.configure(text=step_moves_list[3])
    canvas.delete(ALL)
    drawCube()

#This is used to copy the given string to the users clipboard
def GUItoClipboard(word):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(word)
    r.destroy()
'''
This was the attempt at using a timer to automate a solve, to use, be sure to reactivate the button and import time
#This is used to the a slow, but automatic solve. It uses the timer features to do a couple moves per second or so
def GUIautomateSolve():
    global canvas, a
    b = copy.deepcopy(a)
    solve()
    simplify_moves()
    a = b
    for i in moves_list:
        move(i)
        canvas.after(200, drawCube())
'''

#This is used to export the solve and solution to alg.cubing.net. It will check if it can open with
#Google Chrome, if it can't, it will try firefox, otherwise it will use the default web browser on the system        
def GUIexportSolve():
    sCopy = copy.deepcopy(get_scramble())
    mCopy = copy.deepcopy(get_moves())

    sCopy = str.replace(sCopy, "'", "-")
    sCopy = str.replace(sCopy, " ", "_")
    mCopy = str.replace(mCopy, "'", "-")
    mCopy = str.replace(mCopy, " ", "_")
    
    url = "alg.cubing.net/?setup=" + sCopy + "&alg=" + mCopy
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    firefox_path = "C:/Program Files/Mozilla Firefox/Firefox.exe"
    if os.path.exists(chrome_path):
        webbrowser.get(chrome_path + " %s").open(url)
    elif os.path.exists(firefox_path):
        webbrowser.get(firefox_path + " %s").open(url)
    else:
        webbrowser.open_new(url)

#This is used for the rotation of the cube with buttons. It takes in either a Yi or Y move to be executed
def GUIyRotation(given):
    global canvas
    if given == "Y" or given == "y":
        move('y')
    elif given == "Yi" or given == "Y'" or given == "yi" or given == "y'":
        move('yi')
    canvas.delete(ALL)
    drawCube()

#This will create a new Information GUI, after it is closed, the main GUI() is ran
def InfoGUI():
    rt = tk.Tk()
    rt.geometry("550x135+50+50") #size of the starting frame
    rt.wm_title("Cube Solver Info")
    rt.resizable(False, True) #Only allows the height to be resized, not the width
    InfoGUIy(rt)
    rt.mainloop()
    GUI()

#This will be called within InfoGUI(), it will create a nice GUI with instructions
def InfoGUIy(rt):
    frame = Frame(rt)
    frame.grid(row=0,column=0)
    wel = "\t\t\tWelcome to the cube solver, here are some features:"
    instruct1 = "* Enter in your own moves, then click 'execute' to execute them"
    instruct2 = "* Click scramble to generate a scramble, or make your own and select 'custom scramble'"
    instruct3 = "* Click the two solve buttons to solve, or solve it step by step with the blue buttons"
    instruct4 = "* You can copy the scramble or solution to the clipboard, or export to alg.cubing.net for viewing"
    instruct5 = "* Run some simulations by entering the number of scrambles to simulate"
    InfoLabel = Label(frame, text=wel +"\n"+instruct1+"\n"+instruct2+"\n"+instruct3+"\n"+instruct4+"\n"+instruct5, justify=LEFT)
    InfoLabel.grid(row=0, column=0)
    InfoQuitButton = Button(frame,text="Start Cubing", fg="red",command=lambda: rt.destroy())
    InfoQuitButton.grid(row=1,column=0)

#This is used to run simulations, uses the simulation function. this is the GUI portion of the simulations
def GUISimulation(simNum):
    global SimulateBestLabel, SimulateWorstLabel
    simResults = simulation(simNum)
    s = StringVar(value=simResults[2])
    GUIcustomScramble(s)
    GUISolve()
    SimulateBestLabel.configure(text = str(simResults[1] + 1) + " out of " + str(simNum.get()) + " with " + str(solution_length) + " moves")
    SimulateWorstLabel.configure(text = str(simResults[4] +1) + " out of " + str(simNum.get()) + " with " + str(simResults[3]) + " moves")

#GUI is the main GUI that will be created, it calls GUIy which actually does all the work for the GUI
def GUI():
    global root
    root = tk.Tk()
    root.geometry("550x550+50+50") #size of the starting frame
    root.wm_title("Cube Solver")
    root.resizable(True, True) #Only allows the height to be resized, not the width
    GUIy()
    root.mainloop()
 
#GUIy, after the GUI itself is created with GUI(), this will create all the buttons, labels, etc.. and add them into a frame. This is the behind the
#scenes work for the GUI itself.
def GUIy():
    global root, canvas, ScrambleLabel, SolutionLabel, SolutionNumberLabel, frame,isTransparent
    global PLLNumberLabel,F2LNumberLabel, CrossNumberLabel,OLLNumberLabel, SimulateBestLabel, SimulateWorstLabel
    
    isTransparent = False
    canvas = drawCanvas(root)
    drawCube()

    #locals
    move = StringVar(value="")
    scram = StringVar(value="Enter Scramble Here")
    simNum = IntVar()#Simulation Number
    
    #Frame for controls
    frame = Frame(root)
    frame.grid(row=0,column=1, sticky="n")

    #Frame for cube rotations
    Rframe = Frame(root)
    Rframe.grid(row=0, column=0, sticky = "n")

    #row 1 - welcome label and new cube button
    Welcome = Label(frame, text = "Welcome to the Cube Solver").grid(row=1,column=0)
    NewCubeButton = Button(frame,text="New Cube", command = lambda: GUInewCube())
    NewCubeButton.grid(row=1, column=1)
    #row 2 - label to tell you to enter a move for execution
    EnterMove = Label(frame, text ="Enter move(s):").grid(row=2,column=0)
    #row 3 - Has entry for custom moves as well as button to execute them
    MoveEntry = Entry(frame, textvariable=move).grid(row = 3, column=0)
    DrawCubeButton=Button(frame,text="Execute", command = lambda: GUImakeMove(move)).grid(row = 3,column = 1, sticky="w")
    #row 4 - The label that will print out the current scramble after generation
    ScrambleLabel = Label(frame, text="Scramble will be displayed here",wraplength=180, justify=CENTER, height = 2)
    ScrambleLabel.grid(row=4,column=0, columnspan=2)
    #row 5 - The scramble button to generate new scramble and copy scramble to clipboard
    ScrambleButton = Button(frame, text="Scramble",bg="lightgreen", command = lambda: GUIScramble()).grid(row = 5, column = 0)
    CopyScrambleButton = Button(frame, text="Copy Scramble",bg="#EF9", command = lambda: GUItoClipboard(get_scramble())).grid(row = 5, column = 1)
    #row 6 - entry for custom scramble and button to apply custom scramble to cube
    CustomScramEntry = Entry(frame, textvariable=scram)
    CustomScramEntry.grid(row=6,column=0,sticky="w")
    CustomScramButton = Button(frame,text="Custom Scramble",bg="lightgreen", command = lambda: GUIcustomScramble(scram))
    CustomScramButton.grid(row=6,column=1)
    #row 7 - Slow solve (using timer to do it slowly), instant solve(quick and instant solution), copy solution to clipboard buttons
    #SolveTimerButton = Button(frame, text="Slow Solve", bg="#D53", command = lambda: GUIautomateSolve()).grid(row=7, column=0, sticky="w", pady=5)
    SolveButton = Button(frame, text="Solve Cube",bg="#D53",command = lambda: GUISolve()).grid(row = 7, column = 0) #sticky="e" if using timer button as well
    CopyScrambleButton = Button(frame, text="Copy Solution",bg="#EF9", command = lambda: GUItoClipboard(get_moves())).grid(row = 7, column = 1)
    #row 8 -Solve buttons to do steps independantly
    CrossButton = Button(frame, text="Cross",bg="lightblue", command = lambda: GUIsetSolve("cross"))
    CrossButton.grid(row=8, column=0)
    F2LButton = Button(frame, text="F2l",bg="lightblue", command = lambda: GUIsetSolve("F2L"))
    F2LButton.grid(row=8, column=0, sticky="e", padx= 15)
    OLLButton = Button(frame, text="OLL",bg="lightblue", command = lambda: GUIsetSolve("OLL"))
    OLLButton.grid(row=8, column=1, sticky = "w")
    PLLButton = Button(frame, text="PLL",bg="lightblue", command = lambda: GUIsetSolve("PLL"))
    PLLButton.grid(row=8, column=1, sticky = "e", padx=30)
    #row 9 - the label that contains the solution that will be generated
    SolutionLabel = Label(frame, text="Solution will be displayed here", wraplength = 250, justify=CENTER, height = 8)
    SolutionLabel.grid(row=9, column=0, columnspan=2)
    #row 10 - Labels for number of moves needed to solve 
    SolutionNumberInfoLabel = Label(frame, text="Total number of moves used:")
    SolutionNumberInfoLabel.grid(row=10, column=0,sticky="e")
    SolutionNumberLabel = Label(frame, text="0")
    SolutionNumberLabel.grid(row=10, column=1,sticky="w")
    #row 11, 12, 13, 14 - Labels for number of moves for the different steps
    CrossInfoLabel = Label(frame, text="Moves needed for Cross:")
    CrossInfoLabel.grid(row=11,column=0,sticky="e")
    CrossNumberLabel = Label(frame,text="0")
    CrossNumberLabel.grid(row=11, column=1,sticky="w")
    F2LInfoLabel = Label(frame, text= "Moves needed for F2L:")
    F2LInfoLabel.grid(row = 12, column=0,sticky="e")
    F2LNumberLabel = Label(frame,text="0")
    F2LNumberLabel.grid(row=12, column=1,sticky="w")
    OLLInfoLabel = Label(frame,text="Moves needed for OLL:")
    OLLInfoLabel.grid(row=13, column=0,sticky="e")
    OLLNumberLabel = Label(frame,text="0")
    OLLNumberLabel.grid(row=13, column=1,sticky="w")
    PLLInfoLabel = Label(frame,text="Moves needed for PLL:")
    PLLInfoLabel.grid(row=14, column=0,sticky="e")
    PLLNumberLabel = Label(frame, text="0")
    PLLNumberLabel.grid(row=14, column=1,sticky="w")
    #row 15 - Exporting to alg.cubing.net
    ExportSolveButton = Button(frame, text="Export to alg.cubing.net", command = lambda: GUIexportSolve())
    ExportSolveButton.grid(row=15,column=0)
    #row 16 - Simulations for Best solve
    SimulateEntry = Entry(frame, textvariable = simNum)
    SimulateEntry.grid(row=16, column=0)
    SimulateButton = Button(frame, text="Start Simulations", command = lambda: GUISimulation(simNum))
    SimulateButton.grid(row=16,column=1)
    #row 17 - Which best was found
    SimulateBestInfo = Label(frame, text="Best Simulation: ")
    SimulateBestInfo.grid(row=17,column=0)
    SimulateBestLabel = Label(frame,text="")
    SimulateBestLabel.grid(row=17,column=1,sticky="w")
    #row 18 Which worst was found
    SimulateWorstInfo = Label(frame, text="Worst Simulation: ")
    SimulateWorstInfo.grid(row=18, column=0)
    SimulateWorstLabel = Label(frame,text="")
    SimulateWorstLabel.grid(row=18, column=1)
    
    #In Rframe, buttons for rotation
    RotationLabel = Label(Rframe,text="Use the buttons below to rotate the cube").grid(row=0,column=0, columnspan=2)
    YrotationButton = Button(Rframe, text="<---- Y", command = lambda: GUIyRotation("Y"))
    YrotationButton.grid(row=1, column=0)
    YirotationButton = Button(Rframe, text="Y' ---->", command = lambda: GUIyRotation("Yi"))
    YirotationButton.grid(row=1, column=1)
      
InfoGUI()
