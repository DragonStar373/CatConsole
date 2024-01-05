import maze_tools

def left(heading):
  if heading=="N":
    new_heading = "W"
  elif heading=="W":
    new_heading = "S"
  elif heading=="S":
    new_heading = "E"
  elif heading=="E":
    new_heading = "N"
  return new_heading
    
def right(heading):
  if heading=="N":
    new_heading = "E"
  elif heading=="E":
    new_heading = "S"
  elif heading=="S":
    new_heading = "W"
  elif heading=="W":
    new_heading = "N"
  return new_heading

def solve_maze(maze, n):
  # start in cell [0,0]
  row = 0
  col = 0
  cell = maze_tools.cell_find(maze, row, col)
  path = [cell]
  heading = "E"
  
  finished = False
  # loop until we finish by finding cell (n-1, n-1)
  while not finished:
    # Find direction to move next
    # if we can turn to the right, we should
    if cell[right(heading)]:  
      heading = right(heading)
    # otherwise, we will turn left as many times as it takes
    # to find an unblocked direction (possibly zero times)
    else:
      while not cell[heading]:
        heading = left(heading)
        
    # move in the heading direction
    if heading=="N":
      row = row + 1
    elif heading=="S":
      row = row - 1
    elif heading=="E":
      col = col + 1
    else:
      col = col - 1
      
    cell = maze_tools.cell_find(maze, row, col)
    path.append(cell)
    if row==n-1 and col==n-1:
      finished = True
    
  return path
    

if __name__=="__main__":
  n = 20
  maze = maze_tools.make_maze(n,n)
  path = solve_maze(maze, n)
  maze_tools.animate_maze_and_path(maze, path, n, n)
      
      
      
      
      
      
      
      
      
      
      
      
      
