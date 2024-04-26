import numpy as np
import random as rd

class Game():
  def __init__(self):
    self.grid = np.zeros([9, 10])
    self.apple_position = [6, 4]
    
  def is_apple_eaten(self, position):
    is_eaten = position == self.apple_position
    
    if is_eaten:
      return True
    return False
    
  def get_empty_positions(self):
    empty_positions = []
    
    for y, row in enumerate(self.grid):
      for x, value in enumerate(row):
        empty_positions.append([x, y]) if value == 0 else False
        
    return empty_positions

  def generate_apple(self):
    empty_positions = self.get_empty_positions()
        
    is_grid_full = len(empty_positions) == 0
    if is_grid_full:
      return False
    
    random_index = rd.randint(0, len(empty_positions)-1)
    self.apple_position = empty_positions[random_index]
    return self.apple_position
    
  def update_grid(self, snake_pos, snake_tail):
    self.grid = np.zeros([9, 10])
    
    self.grid[snake_pos[1], snake_pos[0]] = 2
    for x, y in snake_tail:
      self.grid[y, x] = 1
    
    self.grid[self.apple_position[1], self.apple_position[0]] = 3

  def has_win(self):
    empty_positions = self.get_empty_positions()
    
    if len(empty_positions) == 0:
        return True
    return False
