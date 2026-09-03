from random import randint, uniform
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Original Not-Working Code
"""
class Intersection():
    def __init__(self, road_n, n_cars, light_phase):
        self.road_n = road_n
        self.n_cars = n_cars
        self.light_phase = light_phase

    def __len__(self):
        return self.n_cars

    def switch(self, light_phase):
        match light_phase:
            case 0:
                light_phase = 1
            case 1:
                light_phase = 2
            case 2:
                light_phase = 0
        return light_phase

#Roads:          Light_phase:            Direction:
#0 = North       0 = North_South         0 = Straight
#1 = South       1 = West_East           1 = Left
#2 = East        2 = Left_Turn           
#3 = West

class Car(Intersection):
    def __init__(self, road_n, desired_direction, t_waiting):
        super().__init__(road_n)
        self.direction = desired_direction
        self.t_waiting = t_waiting

    def update(self):
        match self.direction:
            case 0:
                match self.road_n:
                    case 0|1:
                        match light_phase:
                            case 0:
                                return 1
                    case 2|3:
                        match light_phase:
                            case 1:
                                return 1
            case 1:
                match light_phase:
                    case 2:
                        return 1
        return 0

light_phase = 0
north_road = Intersection(0, 4, light_phase)
south_road = Intersection(1, 3, light_phase)
east_road = Intersection(2, 2, light_phase)
west_road = Intersection(3, 1, light_phase)
roads = [north_road, south_road, east_road, west_road]

for road in roads:
    for car in range(len(road)):
        car = Car(road.road_n, light_phase, randint(0, 1), 0)

time_passed = 0
while True:
    sleep(1)
    time_passed += 1
    if time_passed % 5 == 0:
        for road in roads:
            road.switch(light_phase)
    for road in roads:
        road.n_cars += randint(1, 4)
        for car in range(len(road)):
            if car.update() == 1:
                car.destroy()
            if not isinstance(car, Car):
                car = Car(road.road_n, light_phase, randint(0, 1), 0)
    upstate = "open" if light_phase == 0 else "closed"
    sidestate = "open" if light_phase == 1 else "closed"
    leftstate = "open" if light_phase == 2 else "closed"
    n_cars = north_road.n_cars
    s_cars = south_road.n_cars
    w_cars = west_road.n_cars
    e_cars = east_road.n_cars
    print(f {upstate}
                |  |  |
                |     |
                |  |  |
             |  {n_cars} |
{sidestate}     |  |  |       {sidestate}
----------------+-----+------------------
                |     |    
{w_cars} - - - - - - - |     |- - - - - - - - {e_cars}
                |     |     
----------------+-----+------------------
            {leftstate}|  |  |
                |     |
                |  |  |
             |  {s_cars} |
                |  |  |
               {upstate}) # I put three " originally here, removing to actually embrace working code
"""

# Bug Fixed Working Code
def bug_fixed():
    class Intersection():
        def __init__(self, road_n, n_cars, light_phase):
            self.road_n = road_n
            self.cars = [Car(road_n, 1 if randint(1, 6) == 6 else 0, 0) for _ in range(n_cars)]
            self.light_phase = light_phase

        def __len__(self):
            return len(self.cars)

        def switch(self, light_phase):
            match light_phase:
                case 0:
                    light_phase = 1
                case 1:
                    light_phase = 2
                case 2:
                    light_phase = 0
            return light_phase

    #Roads:          Light_phase:            Direction:
    #0 = North       0 = North_South         0 = Straight
    #1 = South       1 = West_East           1 = Left
    #2 = East        2 = Left_Turn
    #3 = West

    class Car():
        def __init__(self, road_n, desired_direction, t_waiting):
            self.road_n = road_n
            self.direction = desired_direction
            self.t_waiting = t_waiting

        def update(self, light_phase):
            match self.direction:
                case 0:
                    match self.road_n:
                        case 0|1:
                            match light_phase:
                                case 0:
                                    return 1
                        case 2|3:
                            match light_phase:
                                case 1:
                                    return 1
                case 1:
                    match light_phase:
                        case 2:
                            return 1
            self.t_waiting += 1
            return 0

    light_phase = 0
    north_road = Intersection(0,  4, light_phase)
    south_road = Intersection(1,  4, light_phase)
    east_road = Intersection(2,  4, light_phase)
    west_road = Intersection(3,  4, light_phase)
    roads = [north_road, south_road, east_road, west_road]

    time_passed = 0
    while True:
        sleep(1)
        time_passed += 1
        if time_passed % 5 == 0:
            for road in roads:
                light_phase = road.switch(light_phase)
        for road in roads:
            for car in range(randint(1, 3)):
                road.cars.append(Car(road.road_n, 1 if randint(1, 6) == 6 else 0, 0))

            for car in list(road.cars):
                if car.update(light_phase) == 1:
                    road.cars.remove(car) #.remove() instead of .destroy()

        upstate = "open  " if light_phase == 0 else "closed"
        sidestate = "open  " if light_phase == 1 else "closed"
        leftstate = "open  " if light_phase == 2 else "closed"
        n_cars = len(north_road)
        s_cars = len(south_road)
        w_cars = len(west_road)
        e_cars = len(east_road)
        #system("cls" if name == "nt" else "clear") # Clears terminal
        print("\n" * 50)
        print(f"""                  {upstate}
                    |  |  |
                    |     |
                    |  |  |
                    |  {n_cars}  |
                    |  |  |       
    ----------------+-----+------------------
                    |     |    
    {w_cars} / {sidestate} - - -|     | - - - - - {sidestate} / {e_cars}
                    |     |     
    ----------------+-----+------------------
              {leftstate}|  |  |
                    |     |
                    |  |  |
                    |  {s_cars}  |
                    |  |  |
                      {upstate}""")

# Q-Learning code
def q_learning():
    class Intersection():
        def __init__(self, road_n, n_cars, light_phase):
            self.road_n = road_n
            self.cars = [Car(road_n, 1 if randint(1, 6) == 6 else 0, 0) for _ in range(n_cars)]
            self.light_phase = light_phase

        def __len__(self):
            return len(self.cars)

    #Roads:          Light_phase:            Direction:
    #0 = North       0 = North_South         0 = Straight
    #1 = South       1 = West_East           1 = Left
    #2 = East        2 = Left_Turn
    #3 = West

    class Car():
        def __init__(self, road_n, desired_direction, t_waiting):
            self.road_n = road_n
            self.direction = desired_direction
            self.t_waiting = t_waiting

        def update(self, light_phase):
            match self.direction:
                case 0:
                    match self.road_n:
                        case 0|1:
                            match light_phase:
                                case 0:
                                    return 1
                        case 2|3:
                            match light_phase:
                                case 1:
                                    return 1
                case 1:
                    match light_phase:
                        case 2:
                            return 1
            self.t_waiting += 1
            return 0

    # RL CONFIG
    # State dimensions: 4 roads (capped at max 0 - 15 cars for tabular size) + 1 light phase
    # Total dimensions: (6, 6, 6, 6, 3) for states, and an extra (3) for actions
    q_table = np.zeros((11, 11, 11, 11, 3, 3))

    # Hyperparameters
    alpha = 0.1 # lr
    gamma = 0.95 # discount factor (short term x long term)
    epsilon = 1 # exploration (greedy x random)
    epsilon_decay = 0.9975
    epsilon_min = 0.05

    def get_state_tuple(roads, current_phase): # Caps cars and bounds Q-Table
        n = min(len(roads[0]), 10)
        s = min(len(roads[1]), 10)
        e = min(len(roads[2]), 10)
        w = min(len(roads[3]), 10)
        return (n, s, e, w, current_phase)

    # Training Loop
    rewards_history = []
    for episode in range(5000):
        light_phase = 0
        north_road = Intersection(0, 2, light_phase)
        south_road = Intersection(1, 2, light_phase)
        east_road = Intersection(2, 2, light_phase)
        west_road = Intersection(3, 2, light_phase)
        roads = [north_road, south_road, east_road, west_road]

        episode_reward = 0

        for step in range(200):
            current_state = get_state_tuple(roads, light_phase)

            if uniform(0, 1) < epsilon:
                action = randint(0, 2)
            else:
                action = np.argmax(q_table[current_state])

            light_phase = action

            reward = 0
            for road in roads:
                for car in range(randint(1, 4)):
                    road.cars.append(Car(road.road_n, 1 if randint(1, 6) == 6 else 0, 0))

                for car in list(road.cars):
                    if car.update(light_phase) == 1:
                        road.cars.remove(car)  # .remove() instead of .destroy()

                    reward -= car.t_waiting

            next_state = get_state_tuple(roads, light_phase)

            # Bellman
            old_q_value = q_table[current_state][action]
            max_future_q = np.max(q_table[next_state])

            q_table[current_state][action] = old_q_value + alpha * (reward + gamma * max_future_q - old_q_value)
            episode_reward += reward

        epsilon = max(epsilon * epsilon_decay, epsilon_min)
        rewards_history.append(episode_reward)

    # Showing graph
    plt.figure(figsize=(10, 5))
    plt.plot(rewards_history)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.grid(True)
    plt.show()

    # LIVE TEST
    print("\nTraining complete! Launching live visualization...")
    sleep(2)

    # Reset environment one last time for the visual presentation
    light_phase = 0
    north_road = Intersection(0, 2, light_phase)
    south_road = Intersection(1, 2, light_phase)
    east_road = Intersection(2, 2, light_phase)
    west_road = Intersection(3, 2, light_phase)
    roads = [north_road, south_road, east_road, west_road]

    # Force epsilon to 0 so the agent only uses its learned intelligence
    epsilon = 0.0

    while True:
        sleep(2)
        current_state = get_state_tuple(roads, light_phase)

        # AI looks at the grid queues and makes the optimal decision
        light_phase = np.argmax(q_table[current_state])

        # Environment simulation mechanics
        for road in roads:
            for car in range(randint(1, 4)):
                road.cars.append(Car(road.road_n, 1 if randint(1, 6) == 6 else 0, 0))
            for car in list(road.cars):
                if car.update(light_phase) == 1:
                    road.cars.remove(car)  # .remove() instead of .destroy()


        upstate = "OPEN  " if light_phase == 0 else "CLOSED"
        sidestate = "OPEN  " if light_phase == 1 else "CLOSED"
        leftstate = "OPEN  " if light_phase == 2 else "CLOSED"
        n_cars = len(north_road)
        s_cars = len(south_road)
        w_cars = len(west_road)
        e_cars = len(east_road)

        print("\n" * 50)
        print(f"""                  {upstate}
                        |  |  |
                        |     |
                        |  |  |
                        |  {n_cars}  |
                        |  |  |       
        ----------------+-----+------------------
                        |     |    
        {w_cars} / {sidestate} - - -|     | - - - - - {sidestate} / {e_cars}
                        |     |     
        ----------------+-----+------------------
                  {leftstate}|  |  |
                        |     |
                        |  |  |
                        |  {s_cars}  |
                        |  |  |
                          {upstate}""")

# Has a bug with n. episodes and alpha calculation that could be better based on bucket logic but I'm not going to fix now
def optimized_q_learning(max_cars, avg_cars, range_cars):
    class Intersection():
        def __init__(self, road_n, n_cars, light_phase):
            self.road_n = road_n
            self.cars = [Car(road_n, 1 if randint(1, 6) == 6 else 0, 0) for _ in range(n_cars)]
            self.light_phase = light_phase

        def __len__(self):
            return len(self.cars)

    #Roads:          Light_phase:            Direction:
    #0 = North       0 = North_South         0 = Straight
    #1 = South       1 = West_East           1 = Left
    #2 = East        2 = Left_Turn
    #3 = West

    class Car():
        def __init__(self, road_n, desired_direction, t_waiting):
            self.road_n = road_n
            self.direction = desired_direction
            self.t_waiting = t_waiting

        def update(self, light_phase):
            match self.direction:
                case 0:
                    match self.road_n:
                        case 0|1:
                            match light_phase:
                                case 0:
                                    return 1
                        case 2|3:
                            match light_phase:
                                case 1:
                                    return 1
                case 1:
                    match light_phase:
                        case 2:
                            return 1
            self.t_waiting += 1
            return 0

    if max_cars < 1 | avg_cars <= 0 | range_cars < 0:
        print("Not valid parameters")

    # RL CONFIG
    # State dimensions: 4 roads (capped at max 0 - 15 cars for tabular size) + 1 light phase
    # Total dimensions: (6, 6, 6, 6, 3) for states, and an extra (3) for actions
    q_table = np.zeros((6, 6, 6, 6, 3, 3))

    # Hyperparameters
    alpha = 1/(max_cars * 3) # lr
    gamma = 0.95 # discount factor (short term x long term)

    def get_state_tuple(roads, current_phase): # Caps cars and bounds Q-Table
        def buckets(n_cars):
            if n_cars == 0: return 0
            elif n_cars <= max_cars/5: return 1
            elif n_cars <= 2 * max_cars/5: return 2
            elif n_cars <= 3 * max_cars/5: return 3
            elif n_cars <= 4 * max_cars/5: return 4
            return 5

        n = buckets(len(roads[0]))
        s = buckets(len(roads[1]))
        e = buckets(len(roads[2]))
        w = buckets(len(roads[3]))
        return (n, s, e, w, current_phase)

    # Training Loop
    rewards_history = []
    for episode in tqdm(range(max_cars * 100), desc="Episode"):
        light_phase = 0
        north_road = Intersection(0, 2, light_phase)
        south_road = Intersection(1, 2, light_phase)
        east_road = Intersection(2, 2, light_phase)
        west_road = Intersection(3, 2, light_phase)
        roads = [north_road, south_road, east_road, west_road]

        episode_reward = 0

        for step in range(max_cars * 10):
            current_state = get_state_tuple(roads, light_phase)

            if np.all(q_table[current_state] == 0):
                action = randint(0, 2)
            else:
                action = np.argmax(q_table[current_state])

            light_phase = action

            reward = 0
            for road in roads:
                for car in range(randint(int(avg_cars - range_cars/2), int(avg_cars + range_cars/2))):
                    road.cars.append(Car(road.road_n, 1 if randint(1, 6) == 6 else 0, 0))

                for car in list(road.cars):
                    if car.update(light_phase) == 1:
                        road.cars.remove(car)  # .remove() instead of .destroy()

                    reward -= car.t_waiting

            next_state = get_state_tuple(roads, light_phase)

            # Bellman
            old_q_value = q_table[current_state][action]
            max_future_q = np.max(q_table[next_state])

            q_table[current_state][action] = old_q_value + alpha * (reward + gamma * max_future_q - old_q_value)
            episode_reward += reward

        rewards_history.append(episode_reward)

    # Showing graph
    plt.figure(figsize=(10, 5))
    plt.plot(rewards_history)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.grid(True)
    plt.show()

    # LIVE TEST
    print("\nTraining complete! Launching live visualization...")
    sleep(2)

    # Reset environment one last time for the visual presentation
    light_phase = 0
    north_road = Intersection(0, 2, light_phase)
    south_road = Intersection(1, 2, light_phase)
    east_road = Intersection(2, 2, light_phase)
    west_road = Intersection(3, 2, light_phase)
    roads = [north_road, south_road, east_road, west_road]

    # Force epsilon to 0 so the agent only uses its learned intelligence
    epsilon = 0.0

    while True:
        sleep(2)
        current_state = get_state_tuple(roads, light_phase)

        # AI looks at the grid queues and makes the optimal decision
        light_phase = np.argmax(q_table[current_state])

        # Environment simulation mechanics
        for road in roads:
            for car in range(randint(int(avg_cars - range_cars/2), int(avg_cars + range_cars/2))):
                road.cars.append(Car(road.road_n, 1 if randint(1, 6) == 6 else 0, 0))
            for car in list(road.cars):
                if car.update(light_phase) == 1:
                    road.cars.remove(car)  # .remove() instead of .destroy()


        upstate = "OPEN  " if light_phase == 0 else "CLOSED"
        sidestate = "OPEN  " if light_phase == 1 else "CLOSED"
        leftstate = "OPEN  " if light_phase == 2 else "CLOSED"
        n_cars = len(north_road)
        s_cars = len(south_road)
        w_cars = len(west_road)
        e_cars = len(east_road)

        print("\n" * 50)
        print(f"""                  {upstate}
                        |  |  |
                        |     |
                        |  |  |
                        |  {n_cars}  |
                        |  |  |       
        ----------------+-----+------------------
                        |     |    
        {w_cars} / {sidestate} - - -|     | - - - - - {sidestate} / {e_cars}
                        |     |     
        ----------------+-----+------------------
                  {leftstate}|  |  |
                        |     |
                        |  |  |
                        |  {s_cars}  |
                        |  |  |
                          {upstate}""")

bug_fixed()