#import neural network
import panda as pd

class QLearning():
    def __init__(self, data_path, learning_rate=0.001, reward_decay=0.9, e_greedy=0.9):
        self.learning_rate = learning_rate
        self.gamma = reward_decay
        self.features = pd.read_csv(data_path, sep=',')#need preprocess
        self.epsilon = e_greedy
        self.step_index = 0
        self.cost = []
        self.memory_count = 0
        self.INITIAL_EPSILION = e_greedy
        self.FINAL_EPSILON = 0.01
        self.BATCHSIZE = 20
        self.EXPLORE = 300000
        self.OBSERVE = 1000
        self.MAXSTEP = 100000
        self.MAXSIZE = 9000
        self.DEPTH = 3
        self.replay_buffer = deque()
        self.q_table[0] = pd.Dataframe()
        self.q_table[1] = pd.Dataframe()

    def get_reward(self, gameState, who):
        my_team = gameState.get_team(who)
        opp_team = gameState.get_team(1-who)

        if gameState.isOver == 0:
            my_team_alive = len([x for x in my_team.poke_list if x.alive])
            opp_team_alive = len([x for x in opp_team.poke_list if x.alive])
            return my_team_alive * 100 - opp_team_alive * 100
        else:
            if my_team.alive():
                return 1000000
            else:
                return -1000000

    def step(self, gameState, action, who):
        gameState_new = self.simulator.simulate(gameState, actions, who)
        reward = self.getReward(gameState_new, who)
        self.save(gameState, action, reward, who)

    def perceive(self, gameState, action, reward, gameState_new):
        self.replay_buffer.append((gameState, action, reward, gameState_new, who)
        if len(self.replay_buffer) > self.MAXSIZE:
            self.replay_buffer.popleft()
        if len(self.replay_buffer) > self.OBSERVE:
            self.replay(gameState, action, reward, gameState_new)
        return gameState_new, reward

    def choose_action(self, gameState, who):
        legal_actions = gameState.get_legal_actions(who)
        #choose action with max Q-value
        #NN
        if np.random.uniform() > self.epsilon:
            state_action = self.q_table[who].ix[gameState, :]
            for action in state_action.columns:
                if action not in legal_actions:
                    state_action = state_action.drop(action, axis=1)
            current_action = state_action.argmax()
        else:
            current_action = np.random.choice(legal_actions, size=1)

        if self.step_index > self.OBSERVE and self.epsilon > self.FINAL_EPSILON:
            self.epsilon -= (self.INITIAL_EPSILION - self.FINAL_EPSILON) / self.EXPLORE

        return current_action

    def replay(self, gameState, action, reward, gameState_new, who):
        self.save(gameState, action, reward, who)
        q_predict = self.q_table[who].ix[gameState, :]
        #q_predict = NN
        if gameState_new.is_over() == False:
            q_target = self.q_table[who].ix[gameState_new, :].max()
        else:
            q_target = reward
        self.q_table[who].ix[gameState, action] = self.learning_rate * (reward + self.gamma * q_target - q_predict)
        '''
        #obtain random minibatch from replay memory
        minibatch = random.sample(self.replay_buffer, BATCHSIZE)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = [data[3] for data in minibatch]
        who = [data[4] for data in minibatch]

        #calculate y
        y_batch = []
        #NN
        Q_value_batch = self.Q_value.eval(feed_dict={self.state_input:next_state_batch})
        for i in range(BATCHSIZE):
            if gameState_new.is_over == True:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + self.gamma * np.max(Q_value_batch[i]))

        #optimizer
        '''

    def save(gameState, action, reward, who):
        if gameState not in self.q_table[who].index:
            self.q_table[who] = self.q_table[who].append(
                pd.Series(
                    [0] * self.q_table[who].columns.size,
                    index = self.q_table[who].columns,
                    name = gameState
                )
        self.memory_count += 1
        self.q_table[who][gameState][action] = reward


    def train(self, gameState):
        self.epsilon = self.INITIAL_EPSILION
        for who in [0,1]
            my_team = gameState.get_team(who)
            column_list = []
            for poke in my_team.poke_list
                column_list.append(poke.moveset.moves)
            pokemon = range(len(my_team.poke_list))
            column_list.append([Action("switch", switch_index=i, backup_switch=j) for i in pokemon for j in pokemon if j != i and i is not None])
            self.q_table[who] = pd.Dataframe(columns=column_list)

        while self.step_index < self.MAXSTEP:
            self.step_index += 1
            gameState_new = None
            for who in [0,1]:
                #action = Oracle action
                action = self.choose_action(gameState, who)
                gameState_new, reward = self.step(gameState, action, who)
                self.perceive(gameState, action, reward, gameState_new)
                gameState = gameState_new
            if gameState.isOver():
                print("train finished")
                break

            #test

if __name__ == '__main__':
    ql = QLearning()
    train(gamestate)#need gamestate
