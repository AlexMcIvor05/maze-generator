from tkinter import *
import time
import random
import pyautogui
import threading

root=Tk()
#make func check if box intersects/ gets out of window

coord_list = []

def motion(event):
    #(event)->
    global coord_list
    x, y = event.x, event.y
    #print('{}, {}'.format(x, y))
    inBorders(event.x, event.y, rectangle_group)
    coord_list.append((x,y))
    
    #reset list if in starting zone 
    if intersect(rectangle_group[1], [[x,y,x,y]]):
        coord_list = []
    
    #Winning condition
    if intersect(rectangle_group[0], [[x,y,x,y]]):
        print(len(coord_list))
        win(coord_list)
    
      
def win(lst):
    #The if statement below is a preventive mesureme to make it harder to cheat by moving your cursor from the start
    #straight to the end. for each square that makes up a path, the number below can be +100
    
    if len(coord_list) >  400:
        reset("<space>")     
    
    
def move_mouse_to(x, y):
    '''
    (int,int)-> None
    position cursor at coords (x,y)
    '''
    pyautogui.moveTo(width//2, height-40)



def escape(event):
    exit() 
    
    
    
def inBorders(x, y, lst):
    '''
    (int,int,list)-> bool
    Precondition: lst is a list of rectangles
    
    checks if cursor is contained in one of the rectangles
    '''
    
    flag = False
    
    for rectangle in lst:
        #Check if mouse is in rectangle
        rectangle = re_orient(rectangle)

        #if rectangle is a connecting rectangle
        if abs(rectangle[0]-rectangle[2]) == 0:#vertical line
            if x >= rectangle[0]-6 and y >= height - rectangle[3]-6 and x <= rectangle[2]+6 and y <= height - rectangle[1]-6:
                flag = True
        elif abs(rectangle[1] - rectangle[3]) == 0:#horizontal line
            if x >= rectangle[0]+6 and y >= height - rectangle[1]-6 and x <= rectangle[2]-6 and y <= height - rectangle[3]+6:
                flag = True
       
       
        #for normal rectangles
        if x-6 >   rectangle[0] and y+6 < height-rectangle[1] and x+6 < rectangle[2] and y-6 > height-rectangle[3]: 
            flag = True
            
            
    if flag == False:#Move cursor back to start
        move_mouse_to(width//2,height-40)
    

        
def path_orientation(rectangle):
    '''
    (list)->str
    Precondition: rectangle is a list [x1,y1,x2,y2]
    
    returns what orientation the path is facing
    '''
    
    if abs(rectangle[3] - rectangle[1]) == 30:#horizontal
        if rectangle[2] - rectangle[0] >0:
            
            return "right"
        else:
            
            return "left"
    else:#vertical
        if rectangle[1] - rectangle[3] > 0:
            
            return "up"
        else:
            
            return "down"
        
        
def create_path(rectangle, orientation):
    '''
    (list, str)-> list
    Precondition: rectangle is a list [x1,y1,x2,y2] and orientation is path_orientation(rectangle)
    
    randomly generates a new pathway base on the position of the of the previous pathway(rectangle)
    '''
    
    
    #decide which direction this path will go
    direction = random.randint(1,6)
    rectangle = blTr(rectangle)
    
    
    #this changes how long the rectangle is
    rand1 = random.randint(100,150)
    
    
    if orientation == "up":
        
        if direction == 1:
            return blTr([rectangle[2], rectangle[3], rectangle[2] + 30, rectangle[3] + rand1])
        
        elif direction == 2:
            return blTr([rectangle[0], rectangle[3], rectangle[0] - 30, rectangle[3] + rand1])

        elif direction == 3 or direction == 4:
            return blTr([rectangle[0], rectangle[3], rectangle[0] - rand1, rectangle[3]+30])
            
        else:
            return blTr([rectangle[2], rectangle[3], rectangle[2] + rand1, rectangle[3]+30])
        
        
    elif orientation == "down":
        
        if direction == 1:
            return blTr([rectangle[2], rectangle[3], rectangle[2] - 30, rectangle[3] - rand1])
        
        elif direction == 2:
            return blTr([rectangle[0], rectangle[3], rectangle[0] + 30, rectangle[3] - rand1])
        
        elif direction == 3 or direction == 4:
            return blTr([rectangle[2], rectangle[3], rectangle[2] - rand1, rectangle[3] - 30])   
        else:
            return blTr([rectangle[0], rectangle[3], rectangle[2] + rand1, rectangle[3] - 30 ])
        
    elif orientation == "left":
       
        if direction == 1:
            return blTr([rectangle[2], rectangle[3], rectangle[2] + rand1, rectangle[3] - 30])
        elif direction == 2:
            return blTr([rectangle[2], rectangle[1], rectangle[2] + rand1, rectangle[1] + 30])
        
        elif direction == 3 or direction == 4:
            return blTr([rectangle[2], rectangle[3], rectangle[2] + 30, rectangle[3] - rand1])
        else:
            return blTr([rectangle[2], rectangle[1], rectangle[2]+30, rectangle[1] + rand1])
        
    else:#right
        
        if direction == 1:
            return blTr([rectangle[2], rectangle[3], rectangle[2] - rand1, rectangle[3] + 30])
        elif direction == 2:
            return blTr([rectangle[2], rectangle[1], rectangle[2] - rand1, rectangle[1] - 30])
        elif direction == 3 or direction == 4:
            return blTr([rectangle[2], rectangle[3], rectangle[2] - 30, rectangle[3] + rand1])
        else:
            return blTr([rectangle[2], rectangle[1], rectangle[2] - 30, rectangle[1] - rand1])
            
    
def blTr(rectangle):
    """
    (list)->list
    Precondition : rectangle is [x1,y1,x2,y2]
    
    bl = bottom left tr = top right
    orient rectangle so that the top right coord of the rectangle is the end of the path and the top 
    left is the start coord
    
    up |  | tr   down|   |bl
       |  |          |   |
    bl |  |        tr|   |
    
    """
    orientation = path_orientation(rectangle)      
    
    if orientation == "up":
        if rectangle[2] > rectangle[0]:
            return rectangle
        else:
            return [rectangle[2], rectangle[1], rectangle[0], rectangle[3]]
    
    
    if orientation == "down":
        if rectangle[2] < rectangle[0]:
            return rectangle
        else:
            return [rectangle[2], rectangle[1], rectangle[0], rectangle[3]]
        
    if orientation == "left":
        if rectangle[3] < rectangle[1]:
            return rectangle
        else:
            return [rectangle[0], rectangle[3], rectangle[2], rectangle[1]]
    
    if orientation == "right":
        if rectangle[3] > rectangle[1]:
            return rectangle
        else:
            return [rectangle[0], rectangle[3], rectangle[2], rectangle[1]]
        
   
    
def make_connection(rectangle1, rectangle2):
    '''
    (list,list)-> rectangle
    Precondition : rectangle is a list [x1,y1,x2,y2], rectangle2 is a path made from rectangle1
    
    Connects the two pathways 
    '''
    orientation1 = path_orientation(rectangle1)
        
    if orientation1 == "up":
        if rectangle1[2] > rectangle2[0] or rectangle1[2] > rectangle2[2]:    
            canvas.create_line(rectangle1[0], rectangle1[3]+1, rectangle1[0], rectangle1[3]+30, fill = "white")
            return [rectangle1[0], rectangle1[3]+1, rectangle1[0], rectangle1[3]+30]
        
        else:
            canvas.create_line(rectangle1[2], rectangle1[3]+1, rectangle1[2], rectangle1[3] + 30, fill = "white")
            return [rectangle1[2], rectangle1[3]+1, rectangle1[2], rectangle1[3] + 30]
        
    elif orientation1 == "down":
        if rectangle1[2] > rectangle2[0] or rectangle1[2] > rectangle2[2]:    
            canvas.create_line(rectangle1[2], rectangle1[3]-1, rectangle1[2], rectangle1[3] - 30, fill = "white")
            return [rectangle1[2], rectangle1[3]-1, rectangle1[2], rectangle1[3] - 30]
        
        else:  
            canvas.create_line(rectangle1[0], rectangle1[3]-1, rectangle1[0], rectangle1[3]-30, fill = "white")
            return [rectangle1[0], rectangle1[3]-1, rectangle1[0], rectangle1[3]-30]
        
    elif orientation1 == "left":
        if rectangle1[3] > rectangle2[3] or rectangle1[3] > rectangle2[1]:    
            canvas.create_line(rectangle1[2]+1, rectangle1[3], rectangle1[2]+30, rectangle1[3], fill = "white")
            return [rectangle1[2]+1, rectangle1[3], rectangle1[2]+30, rectangle1[3]]
        
        else: 
            canvas.create_line(rectangle1[2]+1, rectangle1[1], rectangle1[2]+30, rectangle1[1], fill = "white")
            return [rectangle1[2]+1, rectangle1[1], rectangle1[2]+30, rectangle1[1]]
        
    else:#right
        if rectangle1[3] > rectangle2[3] or rectangle1[3] > rectangle2[1]:    
            canvas.create_line(rectangle1[2]-1, rectangle1[1], rectangle1[2]-30, rectangle1[1], fill = "white")
            return [rectangle1[2]-1, rectangle1[1], rectangle1[2]-30, rectangle1[1]]
            
        else: 
            canvas.create_line(rectangle1[2]-1, rectangle1[3], rectangle1[2]-30, rectangle1[3], fill = "white")
            return [rectangle1[2]-1, rectangle1[3], rectangle1[2]-30, rectangle1[3]]
       
       
            
def re_orient(rectangle):
    '''
    (list)->list
    Precondition rectangle is a list [x1,y1,x2,y2]
    ''' 
    
    orientation = path_orientation(rectangle)
    rectangle = blTr(rectangle)
    
    
    if orientation == "down":
        return [rectangle[2],height-rectangle[3],rectangle[0],height-rectangle[1]]
    elif orientation == "left":
        return [rectangle[2],height-rectangle[1],rectangle[0],height-rectangle[3]]
    elif orientation == "right":
        return [rectangle[0],height-rectangle[3],rectangle[2],height-rectangle[1]]
    else:
        return [rectangle[0], height-rectangle[1], rectangle[2], height-rectangle[3]]
    
    
def intersect(rectangle, lst):
    '''
    (list,list)->
    Precondition : rectangle is a list [x1,x2,y1,2] and lst is a list of rectangles
    
    find if rectangles intersects with anything in lst
    '''
       
    
    #Check if rectangle is within the borders of the window
    if (min(rectangle[0], rectangle[1], rectangle[2], rectangle[3]) < 0
        or max(rectangle[0], rectangle[2]) > width or max(rectangle[1], rectangle[3]) > height):
        return True      
        
    rectangle = re_orient(rectangle)    
    
    for rectangle2 in lst: 
        
        rectangle2 = re_orient(rectangle2)
        
        
        if not (rectangle[0] >= rectangle2[2]
                or rectangle[2] <= rectangle2[0]
                or rectangle[1] >= rectangle2[3]
                or rectangle[3] <= rectangle2[1]):
            return True
    return False


'''
def addFalsePaths(rectangle_group):
    rectangle_group
''' 

def timer():
    
    global t
    global item

    while t:
        canvas.itemconfig(item, text = str(t))
        print(t)
        time.sleep(1)
        
        t -= 1
    
    reset("<space>")        
     


def reset(event):
    '''
    (event)-> None
    
    
    
    '''
    
    global rectangle_group
    global t
    global item
    t = 30
    

    
    canvas.delete("all")
    canvas.create_text(900, 50, text="Esc - quit                                                M - Reset  ", fill="black")
    item = canvas.create_text(100, 100, text = t)

    
    
    
    rectangle_group = []
    
    while len(rectangle_group) < 15:#This number changes what the minimum rectangles that can be in a group
        #anything >50 starts to have a noticable delay. anything >100 may cause crashes as it gets exponetially harder to find space
         
        rectangle= blTr([width//2-15, height-20, width//2+15, height-60])
        rectangle_group = []
        canvas.create_rectangle(rectangle, fill="red")
        rectangle_group.append(rectangle)
        
        
        
        potential_rectangle = create_path(rectangle, path_orientation(rectangle))
        
        for i in range(200):
            if intersect(potential_rectangle, rectangle_group) == False:
                rectangle = potential_rectangle
                rectangle_group.append(rectangle)
            potential_rectangle = create_path(rectangle, path_orientation(rectangle))

    
    #Draws all the rectangles
    for i in range(len(rectangle_group)-1):      
        canvas.create_rectangle(rectangle_group[i])
            
    #creates a green rectangle as the end of the maze
    canvas.create_rectangle(rectangle_group[-1][0], rectangle_group[-1][1], rectangle_group[-1][2], rectangle_group[-1][3], fill = "green")
    
    #add a list of connecting rectangles
    rectangle_group_extra = []
    
    for i in range(len(rectangle_group)-1):
        rectangle_group_extra.append(make_connection(rectangle_group[i],rectangle_group[i+1]))
    
    
    #Move the finish to the start of the list to make it easier to access in other functions
    rectangle_group.insert(0, rectangle_group.pop(len(rectangle_group)-1))
    
    #Add connecting hitboxes
    rectangle_group = rectangle_group + rectangle_group_extra
    
    
###################################################
#main
###################################################

    
root.title('Maze Rush')

width= root.winfo_screenwidth()               
height= root.winfo_screenheight()


root.attributes('-fullscreen',True)
root.config(cursor="circle #FF00FF")


canvas = Canvas(root, width = width, height = height, bd = 0)
canvas.pack()
   
canvas.configure(bg="white")


root.bind("<Escape>", escape)
root.bind("<space>", reset)
root.bind('<Motion>', motion)



reset("<Motion>")



move_mouse_to(width//2,height-40)


threading.Thread(None, timer).start()

root.mainloop()

