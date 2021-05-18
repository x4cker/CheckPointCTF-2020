from pwn import *
import re


class Node:
    def __init__(self, coord, parent=None): #Parent is none because i crack the parent in the script
        self.x = coord[0] #the left number is the x
        self.y = coord[1] #the right number is the y
        self.parent = parent

    def is_visited(self, stack):
        for visited in stack: #Check if cell is visited
            if self.x == visited.x and self.y == visited.y:
                return True
        return False

    def get_adjacent(self, directions):
        # [l,r,u,d]
        adjacent = list() #Could do it differently
        left = (self.x - 1, self.y)
        right = (self.x + 1, self.y)
        up = (self.x, self.y + 1)
        down = (self.x, self.y - 1)

        if directions[0] == 1: #if its 1 or 2 it takes the arguments exactly as if directions[0] == 1:
            adjacent.append(Node(left, self))
        if directions[1] == 1:
            adjacent.append(Node(right, self))
        if directions[2] == 1:
            adjacent.append(Node(up, self))
        if directions[3] == 1:
            adjacent.append(Node(down, self))
        return adjacent



def send_msg(conn, msg): #Regular message send through socket for sending and receiving
    conn.send(msg.encode() + b'\n')
    response = conn.recv(128).decode('utf-8')
    conn.recv(128, timeout=1)
    return response

def get_options(conn): #Finding options through the connections. using regex to dissect the directions recevied
    directions = send_msg(conn, 'i') #SENDING I to the server - to find available directions
    opts = re.findall(r'\w=(\d)', directions) #using regex to dissect the the directionss opts becomes a list of ['1', '1', '0', '1'] in the good case
    return list(map(int, opts)) #returing cleaner list [1,1,0,1]

def check_path(current, last):
    path = list()
    while current != last and last.parent: #testing nodes
        #current, last and and last.parent are nodes - the current the last and one before it.
        #each node has x and y from the class Node.
        #def __init__(self, coord, parent=None):
        # self.x = coord[0]
        # self.y = coord[1]
        # self.parent = parent
        if last.x + 1 == last.parent.x: #testing if node is available from the last options received if yes adding direction.
            path.append('l')
        if last.x - 1 == last.parent.x:
            path.append('r')
        if last.y - 1 == last.parent.y:
            path.append('u')
        if last.y + 1 == last.parent.y:
            path.append('d')
        last = last.parent
    if last == current:
        return True, path #returning true and available path.
    return False, [] #returning false and empty list if false.

def backtrack(conn, current, last): #backtracking everything - all actions are in the opposite directions.
    good, path = check_path(current, last)
    while not good and current.parent:
        # Opposite direction
        if current.x + 1 == current.parent.x:
            send_msg(conn, 'r')
        elif current.x - 1 == current.parent.x:
            send_msg(conn, 'l')
        elif current.y + 1 == current.parent.y:
            send_msg(conn, 'u')
        elif current.y - 1 == current.parent.y:
            send_msg(conn, 'd')
        current = current.parent
        good, path = check_path(current, last) #Doing another test with check_path before continuing to not get stuck finally
    while len(path) > 0:
        send_msg(conn, path.pop())

def intro(conn):
    what = b'> What is your command?\n'
    coord = conn.recvuntil(what).decode() #receive until the last byte
    starting_point = (int(re.search(r'\(([0-9]+),([0-9]+)\)', coord).group(1)), int(re.search(r'\(([0-9]+),([0-9]+)\)', coord).group(2)))
    # REGEX WAS PERFORM LIKE SO : #groups are used for putting matchs in place for regex
    # COORD VALUE IS (int, int)
    return starting_point #From the intro we can extract the starting point.



def main(conn):
    start_time = time.time()
    stack = list() #
    known = set() #To not add the same point milion times.
    starting_coord = intro(conn)
    root = Node(starting_coord)
    current_point = root
    stack.append(current_point)

    while len(stack) > 0:
        current_point = stack.pop() #LIST POP
        g = send_msg(conn, 'g')
        print("\ncurrent:", f"{current_point.x} ,{current_point.y}")

        if "far" not in g:
            print("---------------")
            print(g)
            print("Total time:", round(time.time() - start_time), 'seconds.')
            print("current:", "({}, {})".format(current_point.x, current_point.y))
            print("---------------")
            distance = int(re.search(r"(\d+)", g).group(1))
            print('Distance:', distance)
            solutions = []
            solutions_count = 0
            if distance <= 2000:
                for y_x in range(250):
                    for y_y in range(250):
                        if (current_point.x - y_x) ** 2 + (current_point.y - y_y) ** 2 == distance:
                            solutions_count += 1
                            solutions.append((y_x, y_y))
                print(f"Number of Solutions: {solutions_count}")
                if solutions_count <= 4:
                    for i in range(solutions_count):
                        print(f"SENDING POINT : {solutions[i]}")
                        conn.send('s'.encode())
                        conn.recv(224, timeout=1)
                        conn.send(f'{solutions[i]}'.encode())
                        A = (conn.recv(224, timeout=1))
                        if "CSA" in str(A):
                            print(A)
                            print(f"Flag Found : {A}")
                            exit()
                        else:
                            print(A)
                            pass
                else:
                    print("------ Too many Solutions skipping point ------")
                    pass

        directions_info = get_options(conn)
        print("directions", directions_info)
        #Get adjacents from getoptions(conn)
        adjacents = current_point.get_adjacent(directions_info)
        for adjacent in adjacents:
            #PRINTING NEXT POSSIBLE ADJACENT POINT
            #print(adjacent.x, adjacent.y)

            if not adjacent.is_visited(known): #This function returns True or false if not True then lets go else its backtracking
                #CHECKING IF THIS ADJACENT IS NOT IN THE IS_VISITED LIST BECAUSE IF IT DOES WE NEED TO BACKTRACK DUH
                print("adding:", f'({adjacent.x}, {adjacent.y})')
                known.add(adjacent) #ADDING THE KNOWN POINTS TO THE SET

                stack.append(adjacent)
        # IF it didnt work we backtrack - we backtrack anyway to know known points.
        backtrack(conn, current_point, stack[-1]) #back tracking with latest stack, if bcaktracking without it takes way more time.
        # Anyway most of the time the backtrack doesnt have output.


def maze():
    while True:
        try:
            host, port = 'maze.csa-challenge.com', 80
            with remote(host, port) as s:
                main(s)
        except EOFError:
            s.close()
            print("Restarting")

print(chr(65))
print(ord('A'))
maze()
