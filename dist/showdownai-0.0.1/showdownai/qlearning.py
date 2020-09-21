class QLearning:
    def __init__(self, actions, rewards, learning_rate=0.001, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions
        self.learning_rate = learning_rate
        self.gamma = reward_decay
        self.rewards = rewards
        self.epsilon = e_greedy
        self.step_index = 0
        self.INITIAL_EPSILION = e_greedy
        self.FINAL_EPSILON = 0.01
        self.EXPLORE = 300000
        self.OBSERVE = 1000
        self.MAXSTEP = 100000
        self.MAXSIZE = 9000
        self.q_table = pd.DataFrame(columns=self.actions)
    #c
    def choose_action(self, gameState):
        if np.random.uniform() > self.epsilon:
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.argmax()
        else:
            action = np.random.choice(self.actions)

        if self.step_index > self.OBSERVE and self.epsilon > self.FINAL_EPSILON:
            self.epsilon -= (self.INITIAL_EPSILION - self.FINAL_EPSILON) / self.EXPLORE

        return action

    def learn(self, gameState, action, reward, gameState_new):
        self.save(gameState_new)
        q_predict = self.q_table.ix[gameState, action]
        if gameState_new.is_over() == False:
            q_target = self.q_table.ix[gameState_new, :].max()
        else:
            q_target = r
        self.q_table.ix[gameState, action] += self.learning_rate * (reward + self.gamma * q_target - q_predict)
        gameState = gameState_new

    def save(gameState, action, reward):
        if gameState not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index = self.q_table.columns,
                    name = state
                )
        self.q_table[gameState][action] = reward
    '''    if self.q_table.columns > self.MAXSIZE:
                self.q_table.drop()'''

    def train(self, gameState):
        self.epsilon = self.INITIAL_EPSILION

        while self.step_index < self.MAXSTEP:
            action = self.choose_action(gameState)
            gameState_new = self.simulator.simulate(state, actions, who)
            reward =  self.rewards[state][action]
            self.save(gameState, action, reward)

            if self.step_index > self.OBSERVE:
                self.learn(gameState, action, reward, gameState_new)

            if gameState.isOver():
                pass #load next
            else:
                gameState = gameState_new

            self.step_index += 1
