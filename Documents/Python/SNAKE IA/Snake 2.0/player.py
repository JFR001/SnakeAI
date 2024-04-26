from game import Game

class Player(Game):
  def __init__(self):
    super().__init__()
    self.x = 3
    self.y = 4
    self.tail = []
    self.score = 0
    self.last_pos = []
    """
    Left : 0
    Top : 1
    Right : 2
    Bottom : 3
    """
    self.direction = {'x' : 1, 'y': 0}
    self.actions = [
      {'x' : -1, 'y': 0},
      {'x' : 0, 'y': -1},
      {'x' : 1, 'y': 0},
      {'x' : 0, 'y': 1}
    ]
    self.update_grid([self.x, self.y], self.tail)

  def handle_tail(self):
    self.tail = self.tail[:self.score]
    
  def step(self):
    reward = -0.1
    
    self.tail.insert(0, [self.x, self.y])
    self.x += self.direction['x']
    self.y += self.direction['y']
    
    is_apple_eaten = self.is_apple_eaten([self.x, self.y])
    has_lost = self.has_lost()
    has_win = self.has_win()
    if has_win:
      super().__init__()
      return 5
    elif has_lost:
      return -5
    elif is_apple_eaten:
      reward = 2
      self.score += 1
      self.generate_apple()
    
    self.handle_tail()
    self.update_grid([self.x, self.y], self.tail)
    
    return reward

  def take_action(self, action):
    current_index = self.actions.index(self.direction)
    action3_index = current_index + 1 if current_index < len(self.actions) - 1 else 0
    action2_index = current_index
    action1_index = current_index - 1
    
    actions_index = [action1_index, action2_index, action3_index]
    
    action = self.actions[actions_index[action]]
    
    if action['x'] ** 2 == 1 and action['x'] == -self.direction['x']:
      return 'Invalid action'
    elif action['y'] ** 2 == 1 and action['y'] == -self.direction['y']:
      return 'Invalid action'
    
    self.direction = action
    return self.direction

  def has_lost(self):
    is_in_map = 0 <= self.x < len(self.grid[0]) and 0 <= self.y < len(self.grid)
    is_touching_tail = [self.x, self.y] in self.tail
    
    if not is_in_map or is_touching_tail:
      return True
    else:
      return False

