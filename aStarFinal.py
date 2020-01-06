import random  # for random
import matplotlib.pyplot as plt  # for plotting graphs
import time

walls = []  # empty list for the walls
matrix = [[0 for x in range(101)] for y in range(101)]
backward_path = []
adaptive_path = []
previous_goal_g = 0
previous_closed = {}
is_adaptive = False
should = False


class minQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == []

        # for inserting an element in the queue

    def size(self):
        return len(self.queue)

    def insert(self, data: object) -> object:
        self.queue.append(data)

        # for popping an element based on Priority

    def delete(self):
        item = []
        try:
            minIndex = 0
            otherIndex = 1000000
            minF = 10000
            for i in range(len(self.queue)):
                if self.queue[i][1] < self.queue[minIndex][1]:
                    minIndex = i
            minF = self.queue[minIndex][1]
            item.append(self.queue[minIndex])
            del self.queue[minIndex]
            for i in range(len(self.queue)):
                if self.queue[i][1] == minF:
                    otherIndex = i
            if otherIndex != 1000000:
                item.append(self.queue[otherIndex])
                del self.queue[otherIndex]
            return item
        except IndexError:
            print()
            exit()


def blocks(current):  # return nodes that are not in the walls
    return current not in walls


def grid_bounds(position):  # return nodes that are within the 2D matrix
    (x, y) = position
    return 0 <= x < 101 and 0 <= y < 101


def neighbors(current):  # return the neighbors of the current node
    (i, j) = current  # get the i and j value of the current node
    results = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]  # get the up, left, down, right nodes of current node
    results = filter(grid_bounds, results)  # filter them so that they are not out of the 2D matrix
    results = filter(blocks, results)  # filter them so that they are not in the walls
    return results


def heuristic(goal_coordinate, current_coordinate):
    if is_adaptive and should:
        if current_coordinate in previous_closed:
            heuristics = previous_goal_g - previous_closed[current_coordinate]
        else:
            (current_i, current_j) = current_coordinate  # i and j of the current node
            (goal_i, goal_j) = goal_coordinate  # i and j of the goal node
            heuristics = abs(current_i - goal_i) + abs(current_j - goal_j)
    else:
        (current_i, current_j) = current_coordinate  # i and j of the current node
        (goal_i, goal_j) = goal_coordinate  # i and j of the goal node
        heuristics = abs(current_i - goal_i) + abs(current_j - goal_j)
    return heuristics  # return the distance between the 2 points


def generate_maze(txt):
    f = open(txt, 'r')
    start_file = f.readline()
    start_file = start_file.split()  # reads the line for the first and splits into list of strings

    goal_file = f.readline()
    goal_file = goal_file.split()

    start_file_x = int(start_file[0])
    start_file_y = int(start_file[1])
    start = (start_file_x, start_file_y)
    plt.scatter(start_file_x, start_file_y, marker='o', color='b')

    goal_file_x = int(goal_file[0])
    goal_file_y = int(goal_file[1])
    goal = (goal_file_x, goal_file_y)
    plt.scatter(goal_file_x, goal_file_y, marker='o', color='g')

    i = 0
    for line in f:
        line = line.replace(" ", "")
        for j, v in enumerate(line):
            if v == '1':
                colum = (i, j)
                walls.append(colum)
                plt.scatter(i, j, marker='s', color='r')
        i += 1
    '''
    for i in range(100):  # generate walls
        for j in range(100):
            current = (i, j)
            if current != start and current != goal:
                v = random.randint(1, 100)
                if v <= 30:
                    matrix[i][j] = 1
                    plt.scatter(i, j, marker='s', color='r')  # mark it red
    '''
    f.close()
    return start, goal


def are_neighbors_walls(current):
    (i, j) = current
    if i - 1 >= 0 and matrix[i - 1][j] == 1 and (i - 1, j) not in walls:
        insert = (i - 1, j)
        walls.append(insert)
    if i + 1 <= 100 and matrix[i + 1][j] == 1 and (i + 1, j) not in walls:
        insert = (i + 1, j)
        walls.append(insert)
    if j - 1 >= 0 and matrix[i][j - 1] == 1 and (i, j - 1) not in walls:
        insert = (i, j - 1)
        walls.append(insert)
    if j + 1 <= 100 and matrix[i][j + 1] == 1 and (i, j + 1) not in walls:
        insert = (i, j + 1)
        walls.append(insert)


def a_star(start, goal, ties):
    border = minQueue()
    reconst_path = []
    border.insert([start, 0])
    came_from = {}  # these are dictionaries not lists
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    found = 0

    while border.size() != 0:
        current = border.delete()
        if len(current) > 1:
            if ties == 'l':
                if cost_so_far[current[0][0]] < cost_so_far[current[1][0]]:
                    border.insert(current[1])
                    current = current[0][0]
                else:
                    border.insert(current[0])
                    current = current[1][0]
            else:
                if cost_so_far[current[0][0]] > cost_so_far[current[1][0]]:
                    border.insert(current[1])
                    current = current[0][0]
                else:
                    border.insert(current[0])
                    current = current[1][0]
        else:
            current = current[0][0]
        previous_closed[current] = cost_so_far[current]

        if current == goal:
            found = 1
            while current != start:  # the animation is only showing the reconstruction of the path backwards
                reconst_path.append(current)
                current = came_from[current]
            reconst_path.append(current)
            reconst_path.reverse()
            break

        for next in neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                newEntry = [next, priority]
                border.insert(newEntry)
                came_from[next] = current
    if found == 0:
        print("Path does not exist")
        return reconst_path
    else:

        global previous_goal_g
        previous_goal_g = cost_so_far[goal]
        return reconst_path


def forward_a_star(starting, goaling, color, ties):
    forward_path = []
    are_neighbors_walls(starting)
    path = a_star(starting, goaling, ties)
    index = 0
    while index < len(path):
        current = path[index]
        (i, j) = current
        if matrix[i][j] == 0:
            if current not in forward_path:
                forward_path.append(current)
            plt.scatter(i, j, marker=">", color=color)
            are_neighbors_walls(current)
            index += 1
        else:
            current = forward_path[-1]
            path = a_star(current, goaling, ties)
            if is_adaptive:
                global should
                should = True
            index = 0
    return forward_path


txt = input("Enter a Grid World in range GW1.txt - GW50.txt: ")
print("converting text file to grid...")
print("")
start, goal = generate_maze(txt)  # generate a maze
ties = input("How would you like to break ties?: (l for low g values, h for high g values) ")
print("")
switcher = input("Which method would you like to use?: (type f for forward, b for backward, a for adaptive, or q to quit) ")
print("finding path... ")
print("")
if switcher == "f":
    color = 'g'
    now = time.time()
    forward_a_star(start, goal, color, ties)
    finish = time.time()
    print("completed in " + str(finish - now) + " seconds")
    walls.clear()
    plt.show()
elif switcher == "b":
    color = 'blue'
    now = time.time()
    forward_a_star(goal, start, color, ties)
    finish = time.time()
    print("completed in " + str(finish - now) + " seconds")
    walls.clear()
    plt.show()
elif switcher == "a":
    is_adaptive = True
    color = 'yellow'
    now = time.time()
    forward_a_star(start, goal, color, ties)
    finish = time.time()
    print("completed in " + str(finish - now) + " seconds")
    walls.clear()
    plt.show()
else:
    quit()

