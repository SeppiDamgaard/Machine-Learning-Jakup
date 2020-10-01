import gym  
import random
from statistics import mean, median
from collections import Counter
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import TensorBoard
from keras.models import load_model
from keras import optimizers
import numpy as np
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from pathlib import Path

global lastRun
lastRun = 0
gg = 10

def intial_population():
   traning_data = []
   scores = []
   accepted_scores = [] #En liste som holder skoren af de spil som klarede det, så vi kan udskrive disse.
   for _ in range(initial_games):
      score = 0
      game_memory = []
      prev_observation = []
      observation = env.reset() # spil nullstilles
      for _ in range(goal_steps):
            #----------------viser spil på skærmen--------------------------------
            env.render()      
            #----------------viser spil på skærmen-------------------------------
            action = random.randrange(0,2)# tal fra 0-1 "0 <=x < 2"
            observation, reward, done, info = env.step(action) # kører ét Timestep i spillet
            
            if len(prev_observation) > 0:
               #obs. som var lige før er den vi reagerer på nu (action), derfor denne forskudthed.
               game_memory.append([prev_observation, action])
            prev_observation = observation
            score += reward
            if done: #Pinden er faldet for meget ned til en af siderne, og spillet stoppes.
               break
      
      if score >= score_requirement: #Hvis et spil klarer sig godt nok, gemmes det.
            accepted_scores.append(score) #liste til udskrivning af skoringen.
            for data in game_memory: #Tager alle data ud af game_memory og lægger dem i traning_data
               if data[1] == 1:
                  output = [0,1] #laver data om til One-Hot encoding.
               elif data[1] == 0:
                  output = [1,0] #laver data om til One-Hot encoding.
               traning_data.append([data[0].tolist(), output]) #Denne liste gemmer vi til fil. 
      env.reset() #Rester spil.
      scores.append(score) #gemmer score, selv om den ikke kom med i træningssættet.
      np.save('saved.npy', np.array(traning_data)) #Gemmer de udvalgte til fil.
      print('-----------------------------------------------')
      print('Number of accepted score: ' + str(len(accepted_scores)))
      print('Number of traning_data: ' + str(len(traning_data)))
      print('Average accepted score: ' + str(mean(accepted_scores)))
      print('Average  score: ' + str(mean(scores)))
      print('Median  score: ' + str(median(scores)))
      print('Max  score: ' + str(max(scores)))
      print('Min  score: ' + str(min(scores)))
      print('-----------------------------------------------')
      return traning_data
         
for _ in range(gg):
   if lastRun == 0:
      #1
      LR = 1e-3
      env = gym.make('CartPole-v0')
      env.reset()
      goal_steps = 200 #Timesteps a game runs
      score_requirement = 10 #Timesteps a game needs to be accepted in to training set. 50 er gott
      initial_games = 10  #1000 er godt
      numberOfData = 0 #Bare bruges for at undersøge antal data

      train = intial_population()


      #se hvad der er gemt i traning_data
      traningData = np.load('saved.npy', allow_pickle=True)
      inputData =  traningData[:,0].tolist()
      outputData =  traningData[:,1].tolist()
      print('-----------------------------------------------')
      print('See one input data: ' + str( inputData[0]))
      print('See one output data: ' + str( outputData[0]))
      print('-----------------------------------------------')
      # For at forstå inputData, se her: https://gym.openai.com/docs/ 
      lastRun = 1

   elif lastRun == 1 or lastRun == 3:
      #2
      traningData = np.load('saved.npy', allow_pickle=True)
      inputData =  traningData[:,0].tolist()
      outputData =  traningData[:,1].tolist()
      #print(inputData)

      my_file = Path("a.h5")
      if my_file.is_file():
         # Henter allerede trænet model  
         model = load_model('a.h5')
         print('Model fundet')
      else:
         # laver ny model om den ikke allerede eksisterer
         model = Sequential()
         model.add(Dense(10, input_dim=4, activation='tanh'))
         model.add(Dense(64, activation='tanh'))
         model.add(Dense(2, activation='softmax'))
         model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])
         print('Ny model lavet, ingen model fundet...')

      print(model.input)
      #callback = TensorBoard(log_dir='./graphs', update_freq='epoch') 
      history = model.fit(inputData, outputData, verbose=2, epochs=20) #, callbacks=[callback])
      #print(history.history['acc']) # samme data som verbose=2 viser
      model.save('a.h5')
      lastRun = 2







   elif lastRun == 2:
   #3
      #Load
      model = load_model('a.h5')

      env = gym.make('CartPole-v0')

      env.reset()
      goal_steps = 3000
      env._max_episode_steps = 200 #Default er 200

      action = random.randrange(0,2) #Den første action er random.
      scores = []
      score = 0
      traning_data = []
      numberOfGames = 10
      score_requirement = 20 #Denne flyttes op skridt vis, for at lave modellen stærkere
      count = 0        

      for x in range(numberOfGames):
         env.reset()
         score = 0
         game_memory = []

         for t in range(goal_steps):
            env.render() # viser spil på skærmen 
            observation, reward, done, info = env.step(action) #første gang random, resten fra model.
            prediction = model.predict(np.array([observation])).tolist() #henter prediction fra model, skal bruger næste gang.
            # print(prediction) # [[0.48285746574401855, 0.5171425938606262]]
            indexOfGuess = prediction[0].index(max(prediction[0]))
            #print(indexOfGuess) # 1
            score += reward
            if (indexOfGuess == 0):
                  action = 0
                  output = [1,0]
            elif (indexOfGuess == 1):
                  action = 1
                  output = [0,1]
            if done:
                  scores.append(score)            
                  env.close()
                  break
            game_memory.append([observation, output]) 
            count = count + 1
            print(count)
            print (x)

         print (game_memory)
         if score >= score_requirement: #Hvis et spil klarer sig godt nok, gemmes det.
            for data in game_memory: #Tager alle data ud af game_memory og lægger dem i traning_data
                  print(data[0])
                  print(data[1])
                  traning_data.append([data[0].tolist(), data[1]]) #Denne liste gemmer vi til fil. 
                     
      np.save('saved.npy', np.array(traning_data))

      print('Average score', mean(scores))
      print('Median score', median(scores))
      print('Min score', min(scores))
      print('Max score', max(scores))
      print('Number of traning_data: ' + str(len(traning_data)))
      lastRun = 3

