from UpdatedMazeSolver import Maze
import sys


try:
  # takes file as input
  file = input("Please enter a file name with the maze: ")
except IndexError:
  file = input("Please enter a file name with the maze: ")

Maze(file)


