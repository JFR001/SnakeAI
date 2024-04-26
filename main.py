import tensorflow as tf
import numpy as np
import random as rd
from player import Player

class AI(Player):
  def __init__(self):
    super().__init__()
    self.model = tf.keras.models.Sequential()
    self.model.add(tf.keras.layers.InputLayer(input_shape=(91)))
    self.model.add(tf.keras.layers.Dense(256, activation='relu'))
    self.model.add(tf.keras.layers.Dense(128, activation='relu'))
    self.model.add(tf.keras.layers.Dense(3, activation='softmax'))
    self.buffer = [] # Will be shuffle with random.shuffle()
    
    self.gamma = 0.99
    self.eps = 1
    
    self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=["accuracy"])#loss='sparse_categorical_crossentropy')
    
    self.train()
            
  def normalize_for_input(self, grid, direction):
    direction_index = self.actions.index(direction)
    input = list(np.append(grid.flatten(), direction_index))
    return input

  def predict_action(self, input):
    prediction = self.model.predict([input])[0]
    predicted_action = int(np.where(prediction == max(prediction))[0][0])
    return predicted_action

  def fit_model(self):
    rd.shuffle(self.buffer)
    
    def get_Q_target(r, st1):
      Q_stp1 = self.model.predict([st1])[0]
      Q_target = r + max(Q_stp1) * self.gamma
      return Q_target

    x_train = []
    y_train = []
    
    for sars1 in self.buffer:
      target = [0, 0, 0]
      Q_target = get_Q_target(sars1['r'], sars1['st+1'])
      target[sars1['at']] = Q_target
      
      x_train.append(sars1['st'])
      y_train.append(target)
      
    self.model.fit(x_train, y_train, batch_size=32, epochs=100)
    loss, accuracy = self.model.evaluate(x_train, y_train)
    print('Loss : %s   Accuracy : %s' % (loss, accuracy))
    
  def shuffle_env(self):
    self.loop_punishment = 0
    self.tail = []
    self.x = rd.randint(0, 9)
    self.y = rd.randint(0, 8)
    self.direction = rd.choice(self.actions)
    self.generate_apple()
    self.update_grid([self.x, self.y], self.tail)
    
  def train(self):
    for epoch in range(401):
      step = 0
      while step < 200:
        st = self.normalize_for_input(self.grid, self.direction)
        at = self.predict_action(st)
        self.take_action(at)
        r = self.step()
        st1 = self.normalize_for_input(self.grid, self.direction)

        if r == -5:
          st1 = st
          self.shuffle_env()

        print('Reward : %s   Step : %s' % (r, step))

        self.buffer.append({'st': st, 'at': at, 'r': r, 'st+1': st1})

        if len(self.buffer) > 10000:
          self.buffer = self.buffer[1:]

        step += 1
        
      self.eps = max(0.1, self.eps*0.99)
        
      if epoch % 5 == 0 and epoch != 0:
        self.fit_model()
        
      self.shuffle_env()

AI()
