
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy

def cell_find(cells, row, col):
  for cell in cells:
    if cell["row"]==row and cell["col"]==col:
      return cell

def make_maze(num_rows, num_cols):

  # Initialize all cells with impassable walls
  maze_cells = []
  for row in range(num_rows):
    for col in range(num_cols):
      maze_cells.append({"row":row,"col":col,"N":False,"E":False,"S":False,"W":False})

  # first cell
  frontier = [] # initialize list of frontier cells
  visited = [] # initialize list of visited cells
  random.seed() # seed random number generator
  firstrow = random.randrange(num_rows) # Choose a random row and
  firstcol = random.randrange(num_cols) # column index for the first cell
  this_cell = cell_find(maze_cells,firstrow,firstcol)
  # mark that we have visited this cell
  visited.append(this_cell)
  # mark that the orthogonally neighboring cells are now part of the frontier
  if firstrow>0:
    adjacent_cell = cell_find(maze_cells,firstrow-1,firstcol)
    frontier.append(adjacent_cell)
  if firstrow<num_rows-1:
    adjacent_cell = cell_find(maze_cells,firstrow+1,firstcol)
    frontier.append(adjacent_cell)
  if firstcol>0:
    adjacent_cell = cell_find(maze_cells,firstrow,firstcol-1)
    frontier.append(adjacent_cell)
  if firstcol<num_cols-1:
    adjacent_cell = cell_find(maze_cells,firstrow,firstcol+1)
    frontier.append(adjacent_cell)

  # loop over remaining maze cells
  for i in range(len(maze_cells)-1):
    # Choose a random frontier cell
    this_cell = frontier[random.randrange(len(frontier))]
    # Initialize list of candidate cells to join
    candidates = []
    
    # find which cells adjacent to this one have been visited
    # if they have been visited, add to the list of potential cells to join
    # if they have not been visited, add to frontier
    if this_cell["row"]>0:
      adjacent_cell = cell_find(maze_cells,this_cell["row"]-1,this_cell["col"])
      if adjacent_cell in visited:
        candidates.append(adjacent_cell)
      elif not adjacent_cell in frontier:
        frontier.append(adjacent_cell)
    if this_cell["row"]<num_rows-1:
      adjacent_cell = cell_find(maze_cells,this_cell["row"]+1,this_cell["col"])
      if adjacent_cell in visited:
        candidates.append(adjacent_cell)
      elif not adjacent_cell in frontier:
        frontier.append(adjacent_cell)
    if this_cell["col"]>0:
      adjacent_cell = cell_find(maze_cells,this_cell["row"],this_cell["col"]-1)
      if adjacent_cell in visited:
        candidates.append(adjacent_cell)
      elif not adjacent_cell in frontier:
        frontier.append(adjacent_cell)
    if this_cell["col"]<num_cols-1:
      adjacent_cell = cell_find(maze_cells,this_cell["row"],this_cell["col"]+1)
      if adjacent_cell in visited:
        candidates.append(adjacent_cell)
      elif not adjacent_cell in frontier:
        frontier.append(adjacent_cell)
        
    # Choose one of the candidate cells to join with this one
    join_cell = candidates[random.randrange(len(candidates))]
    
    # join cells
    if this_cell["row"]==join_cell["row"]:
      if this_cell["col"]==join_cell["col"]+1:
        this_cell["W"]=True
        join_cell["E"]=True
      else:
        this_cell["E"]=True
        join_cell["W"]=True
    else:
      if this_cell["row"]==join_cell["row"]+1:
        this_cell["S"]=True
        join_cell["N"]=True
      else:
        this_cell["N"]=True
        join_cell["S"]=True
    
    # Remove joined cell from frontier and add to visited list
    frontier.remove(this_cell)
    visited.append(this_cell)
    
  return maze_cells

def maze_raster(maze, num_rows, num_cols, cellsize):
  im_height = cellsize*num_rows
  im_width = cellsize*num_cols
  im = np.ones([im_height, im_width])
  for cell in maze:
    offset_x = cellsize*cell["col"]
    offset_y = cellsize*cell["row"]
    if not cell["N"]:
      for i in range(cellsize):
        im[offset_y+cellsize-1,offset_x+i] = 0
    if not cell["S"]:
      for i in range(cellsize):
        im[offset_y,offset_x+i] = 0
    if not cell["E"]:
      for i in range(cellsize):
        im[offset_y+i,offset_x+cellsize-1] = 0
    if not cell["W"]:
      for i in range(cellsize):
        im[offset_y+i,offset_x] = 0   
  return im
  
def print_maze(maze, num_rows, num_cols):
  im = maze_raster(maze, num_rows, num_cols, 10)
  plt.imshow(np.flipud(im), cmap='gray')
  plt.show()

def animate(i, raster, path, cellsize, ax):

  im = deepcopy(raster)

  n = 0
  for cell in path:
    if n==i:
      break
    offset_x = cellsize*cell["col"]
    offset_y = cellsize*cell["row"]
    for x in range(cellsize-4):
      for y in range(cellsize-4):
        im[offset_y+2+y,offset_x+2+x] = 0.75
    n = n + 1

    
  cell = path[i]
  offset_x = cellsize*cell["col"]
  offset_y = cellsize*cell["row"]
  for x in range(cellsize-4):
    for y in range(cellsize-4):
      im[offset_y+2+y,offset_x+2+x] = 0.25
  ax.clear()
  ax.set_xticks([])
  ax.set_yticks([])
  ax.imshow(np.flipud(im), cmap='gray')

  
def animate_maze_and_path(maze, path, num_rows, num_cols):
  cellsize = 10
  im = maze_raster(maze, num_rows, num_cols, cellsize)
  fig, ax = plt.subplots()
  ax.xaxis.set_tick_params(labelbottom=False)
  ax.yaxis.set_tick_params(labelleft=False)
  anim = FuncAnimation(fig, animate, frames = len(path), fargs=(im, path, cellsize, ax), interval=int(input("speed: ")))
  plt.show()
  

def print_maze_and_path(maze, path, num_rows, num_cols):
  cellsize = 10
  im = maze_raster(maze, num_rows, num_cols, cellsize)
  for cell in path:
    offset_x = cellsize*cell["col"]
    offset_y = cellsize*cell["row"]
    for x in range(cellsize-4):
      for y in range(cellsize-4):
        im[offset_y+2+y,offset_x+2+x] = im[offset_y+2+y,offset_x+2+x] - 0.33
  
  plt.imshow(np.flipud(im), cmap='gray')
  plt.show()

        
if __name__=="__main__":
  n = 10
  m = make_maze(n,n)
#  print(m)
  print_maze(m,n,n)
    
    
    
    
    
    

      
