import sys
import re
import os.path  # used to check if file exists
import numpy as np


class Maze:
    # takes in a filepath and creates the self.matrix from the text file
    def __init__(self, filePath):
        matrix = []
        size = []
        struct = []
        while not os.path.exists(filePath):
            filePath = input("File Does not exist, Please enter again: ")

        for line in open(filePath):
            size, struct = (line.split('-'))
            self.row, self.col = re.findall('\d+', size)
            self.struct = re.findall('\d+', struct)
            a = np.array(self.struct)

            # Converts the array into matrix form
            matrix = (a.reshape((int(self.row), int(self.col))))
            self.size = size
            self.start = None
            self.matrix = matrix
            self.path = []
            self.charmatrix = []
            self.upopen = []
            self.rightopen = []
            self.leftopen = []
            self.downopen = []
            self.ismine = []
            self.isend = []
            self.isstart = []
            self.isvisited = []
            self.route = []
            self.life = 3
            self.up = False
            self.left = False
            self.down = False
            self.right = False
            self.start = False
            self.end = False
            self.mine = False
            self.visited = False
            self.pathdirection()

    # function to print the matrix form of the array
    def printMaze(self):
        matrix = self.matrix
        # print("Matrix is : \n", matrix)
        return matrix

    # Function to return matrix element and its row,column
    def coordmaze(self):
        coordmazestruct = []
        for i in range(int(self.row)):
            for j in range(int(self.col)):
                coordmazestruct.append((self.matrix[i][j], i, j))
        # print('check for coords ,',coordmazestruct)
        return coordmazestruct

    def createcharmaze(self):
        UP_MASK = 1
        RIGHT_MASK = 2
        DOWN_MASK = 4
        LEFT_MASK = 8
        START_MASK = 16
        END_MASK = 32
        MINE_MASK = 64

        x = int(self.row)
        y = int(self.col)

        self.upopen = []
        self.rightopen = []
        self.leftopen = []
        self.downopen = []
        self.ismine = []
        self.isend = []
        self.isstart = []
        struct = self.struct
        char_struct = []
        new_struct = self.coordmaze()

        # print('len is ',len(new_struct), new_struct)

        for k in range(len(new_struct)):
            # print('Here is something', k + 1, len(struct))
            charmaze = []
            mazestatus = []
            self.value = int(new_struct[k][0])
            value = self.value
            # print('value is',value)
            # print(value)

            if (value & START_MASK) == START_MASK:
                self.start = True
                # print(new_struct[k])
                self.isstart.append(new_struct[k])
                charmaze.append('Start is true')
            if (value & END_MASK) == END_MASK:
                self.end = True
                self.isend.append(new_struct[k])
                charmaze.append('End is true')
            if (value & MINE_MASK) == MINE_MASK:
                self.mine = True
                self.ismine.append(new_struct[k])
                charmaze.append('Mine is true')
            if (value & UP_MASK) == UP_MASK:
                self.up = True
                charmaze.append('Up is true')
                self.upopen.append(new_struct[k])

            if (value & RIGHT_MASK) == RIGHT_MASK:
                self.right = True
                self.rightopen.append(new_struct[k])
                charmaze.append('Right is true')
            if (value & DOWN_MASK) == DOWN_MASK:
                self.down = True
                self.downopen.append(new_struct[k])
                charmaze.append('Down is true')
            if (value & LEFT_MASK) == LEFT_MASK:
                self.left = True
                self.leftopen.append(new_struct[k])
                charmaze.append('Left is true')

            for status in range(len(charmaze)):
                # print('value is :', len(charmaze), value)
                if charmaze[status] == 'Start is true':
                    mazestatus.append('S')
                elif (charmaze[status] == 'End is true'):
                    mazestatus.append('E')
                elif (charmaze[status] == 'Mine is true'):
                    mazestatus.append('M')
                else:
                    mazestatus.append('O')
            char_struct.append(mazestatus[0])

    # function to return the cell as tuple, to maintain coordinates
    def dictofmatrix(self, i, j):
        directcell = (self.matrix[i][j], i, j)
        return directcell

    # function to restart solving the maze from start point, in case the path takes all lives
    def reset(self):
        self.route = []
        self.life = 3
        current = self.isstart[0]

        return self.solvemaze(self.matrix, current)



        #This function solves a maze by using recursive approach using backtracking, to return the shortest path.
        # This approach worked fine with all the small mazes, for example the maze listed in the 'textmaze,txt' file as well as with the mazes provided
        #in the 'mazes.txt' file in the coding challenge package



    # This function takes the input as the matrix and current position, which is intially the starting point of the maze

    def solvemaze(self, matrix, current):

        self.createcharmaze()
        current = current
        end = self.end
        mine = self.ismine
        uplist = self.upopen
        downlist = self.downopen
        rightlist = self.rightopen
        leftlist = self.leftopen

        # print('L:',leftlist )
        # print('R', rightlist)
        # print('D',downlist)
        # print('U',uplist)

        endnode = self.isend[0]
        # print('Start and end:', current, endnode)
        queue = [current]

        while queue:
            # print('q', queue)
            path = []
            path.append(queue.pop(0))
            node = (path.pop())
            queue = []

            if current == endnode:
                self.route.append(current)
                #print('found end')
                return self.route

            else:
                try:

                    # This is a empty list maintained to get out of the function in case the cell is blocked or has wall.

                    neighbours = []


                    # Checks the neighbour above // Up side of current cell

                    if ((current in uplist) and (self.life >= 1) and
                                (self.dictofmatrix((current[1] - 1), current[2])) not in self.isvisited):
                        try:
                            if (self.dictofmatrix((current[1] - 1), current[2])) in mine:
                                if self.life == 1:

                                    # cheks if only one life is remaining, if its last life, it will change the path by avoiding mine
                                    self.isvisited.append(current)
                                    self.isvisited.append(self.dictofmatrix((current[1] - 1), current[2]))
                                    current = self.route[-1]

                                    self.solvemaze(self.matrix, current)

                                else:
                                    self.life -= 1

                            #print('UP Wall:', current, self.dictofmatrix((current[1] - 1), current[2]))
                            neighbours.append(self.dictofmatrix((current[1] - 1), current[2]))

                            #marks the current cell as visited
                            self.isvisited.append(current)

                            #adds the cell to route
                            self.route.append(current)

                            current = self.dictofmatrix((current[1] - 1), current[2])

                            # print('Route is:', self.route)
                            # print('visited is:', self.isvisited)

                            return self.solvemaze(self.matrix, current)

                        except IndexError:
                            # print('Error in Up')
                            pass




                    # Checks the neighbour on the right // Right side of current cell

                    if ((current in rightlist) and (self.life >= 1) and (
                            self.dictofmatrix(current[1], (current[2] + 1))) not in self.isvisited):
                        try:
                            if (self.dictofmatrix(current[1], (current[2] + 1))) in mine:
                                if self.life == 1:
                                    self.isvisited.append(current)
                                    self.isvisited.append(self.dictofmatrix(current[1], (current[2] + 1)))
                                    current = self.route[-1]

                                    self.solvemaze(self.matrix, current)

                                else:
                                    self.life -= 1

                            # print('Right Wall:', current, self.dictofmatrix(current[1], (current[2] + 1)))
                            neighbours.append(self.dictofmatrix(current[1], (current[2] + 1)))
                            self.isvisited.append(current)
                            self.route.append(current)
                            current = self.dictofmatrix(current[1], (current[2] + 1))

                            # print('Route is:', self.route)
                            # print('visited is:', self.isvisited)

                            return self.solvemaze(self.matrix, current)

                        except IndexError:
                            # print('Error in Right')
                            pass

                    # Checks the neighbour below // Down side of current cell
                    if ((current in downlist) and (self.life >= 1) and (
                            self.dictofmatrix((current[1] + 1), current[2])) not in self.isvisited):
                        try:
                            if (self.dictofmatrix((current[1] + 1), current[2])) in mine:
                                if self.life == 1:
                                    self.isvisited.append(current)
                                    self.isvisited.append(self.dictofmatrix((current[1] + 1), current[2]))
                                    current = self.route[-1]

                                    self.solvemaze(self.matrix, current)

                                else:
                                    self.life -= 1

                            # print('Down Wall:', current, self.dictofmatrix((current[1] + 1), current[2]))
                            neighbours.append(self.dictofmatrix((current[1] + 1), current[2]))
                            self.isvisited.append(current)
                            self.route.append(current)
                            current = self.dictofmatrix((current[1] + 1), current[2])

                            # print('Route is:', self.route)
                            # print('visited is:', self.isvisited)

                            return self.solvemaze(self.matrix, current)
                        except IndexError:
                            # print('Error in Down')
                            pass



                            # Checks the neighbour on left // Left side of current cell

                    if ((current in leftlist) and (self.life >= 1) and (
                            self.dictofmatrix(current[1], current[2] - 1)) not in self.isvisited):
                        try:
                            if (self.dictofmatrix(current[1], current[2] - 1)) in mine:

                                if self.life == 1:
                                    self.isvisited.append(current)
                                    self.isvisited.append(self.dictofmatrix(current[1], current[2] - 1))
                                    current = self.route[-1]

                                    self.solvemaze(self.matrix, current)

                                else:
                                    self.life -= 1

                            # print('Left Wall:', current, self.dictofmatrix(current[1], current[2] - 1))
                            neighbours.append(self.dictofmatrix(current[1], current[2] - 1))
                            # self.isvisited.append(self.dictofmatrix(current[1], current[2] - 1))
                            self.isvisited.append(current)
                            self.route.append(current)

                            current = self.dictofmatrix(current[1], current[2] - 1)

                            # print('Route is:', self.route)
                            # print('visited is:', self.isvisited)

                            return self.solvemaze(self.matrix, current)

                        except IndexError:
                            # print('Error in Left')
                            pass

                    if neighbours == []:
                        if len(neighbours) == 0:

                            #checks if the current cell is already visited, and if its the starting of maze
                            if current in self.isvisited:
                                if current == self.isstart[0] and self.isvisited == []:
                                    # print('checking try1')
                                    pass
                                else:
                                    # checks if the cell is a mine and life is valid
                                    if current in mine and self.life in range(1, 4):
                                        self.life += 1

                                    current = self.route[-1]
                                    self.route.remove(current)

                            else:
                                self.isvisited.append(current)
                                current = self.route[-1]
                                self.route.remove(current)

                            # print('current at end of try', current)
                            return self.solvemaze(self.matrix, current)

                except IndexError:
                    # print('Error in main')

                    # This works if the matrix goes out of index, for corner cells and the side and top and bottom rows
                    if not neighbours:
                        if len(neighbours) == 0:
                            if current in self.isvisited:
                                if current == self.isstart[0] and self.isvisited == []:
                                    pass
                                else:
                                    if current in mine and self.life in range(1, 4):
                                        self.life += 1
                                    current = self.route[-1]
                                    self.route.remove(current)

                                    # print('current at start of main', current)
                                    # print('route in main 1', self.route)
                                    # print('visited is -1:', self.isvisited)


                            else:
                                self.isvisited.append(current)
                                current = self.route[-1]
                                self.route.remove(current)

                                # print('route in main 2',self.route)
                                # print('visited is -2:', self.isvisited)

                            # print('current at end of main:',current)
                            return self.solvemaze(self.matrix, current)
                    pass

        # print('life:', self.life)
        # print('route is', route)
        # print('Visited are:', self.isvisited)
        return self.route




    # This function converts the route into direction by checking the coordinates, and returns the list of movements in Direction
    def pathdirection(self):
        movements = []
        self.createcharmaze()
        current = self.isstart[0]
        direction = self.solvemaze(self.matrix, current)
        #print(direction)
        for i in range(len(direction) - 1):
            if direction[i][1] < direction[i + 1][1]:
                movements.append('Down')
            if direction[i][1] > direction[i + 1][1]:
                movements.append('Up')
            if direction[i][2] > direction[i + 1][2]:
                movements.append('Left')
            if direction[i][2] < direction[i + 1][2]:
                movements.append('Right')
        if len(movements)==0:
            print(['The Maze cannot be solved'])
        else:
            print(movements)
        return movements
