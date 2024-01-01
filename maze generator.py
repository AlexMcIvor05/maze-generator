from tkinter import *
import time
import random

root=Tk()
#make func check if box intersects/ gets out of window

def motion(event):
    #(event)->
    x, y = event.x, event.y
    #print('{}, {}'.format(x, y))
    inBorders(event.x, event.y, [[100, 200, 300, 400],[200,400,300,700]])


# Moves the mouse to an absolute location on the screen
def move_mouse_to(x, y):
    '''
    (int,int)-> None
    position cursor at coords (x,y)
    '''
    temp_root = Tk()
    temp_root.overrideredirect(True)
    temp_root.update()
    temp_root.event_generate("<Motion>", warp=True, x=x, y=y)
    temp_root.update()
    temp_root.destroy()


def inBorders(x, y, lst):
    '''
    (int,int,list)-> bool
    Precondition: lst is a list of rectangles
    
    checks if cursor is contained in one of the rectangles
    '''
    flag = False
    
    for rectangle in lst:
        #Check if mouse is in rectangle
        if x >= rectangle[0] and y >= rectangle[1] and x <= rectangle[2] and y <= rectangle[3]: 
            flag = True
    print(flag)
    return flag

        
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
        

def make_path(rectangle):
    """
    (list)->None
    Precondition : rectangle is a list [x1,y1,x2,y2]
    ####useless####
    Creates a pathway
    """
    
    if abs(rectangle[0]-rectangle[2]) == 30:#vertical path
        canvas.create_line(rectangle[0],rectangle[1],rectangle[0],rectangle[3])
        canvas.create_line(rectangle[2],rectangle[1],rectangle[2],rectangle[3])
    
    else:#horizontal path
        canvas.create_line(rectangle[0],rectangle[1],rectangle[2],rectangle[1])
        canvas.create_line(rectangle[0],rectangle[3],rectangle[2],rectangle[3])
    
    
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
        else:
            canvas.create_line(rectangle1[2], rectangle1[3]+1, rectangle1[2], rectangle1[3] + 30, fill = "white")
    elif orientation1 == "down":
        if rectangle1[2] > rectangle2[0] or rectangle1[2] > rectangle2[2]:    
            canvas.create_line(rectangle1[2], rectangle1[3]-1, rectangle1[2], rectangle1[3] - 30, fill = "white")
        else:  
            canvas.create_line(rectangle1[0], rectangle1[3]-1, rectangle1[0], rectangle1[3]-30, fill = "white")
    
    elif orientation1 == "left":
        if rectangle1[3] > rectangle2[3] or rectangle1[3] > rectangle2[1]:    
            canvas.create_line(rectangle1[2]+1, rectangle1[3], rectangle1[2]+30, rectangle1[3], fill = "white")
        else: 
            canvas.create_line(rectangle1[2]+1, rectangle1[1], rectangle1[2]+30, rectangle1[1], fill = "white")
    else:
        if rectangle1[3] > rectangle2[3] or rectangle1[3] > rectangle2[1]:    
            canvas.create_line(rectangle1[2]-1, rectangle1[1], rectangle1[2]-30, rectangle1[1], fill = "white")
            
        else: 
            canvas.create_line(rectangle1[2]-1, rectangle1[3], rectangle1[2]-30, rectangle1[3], fill = "white")
            
def re_orient(rectangle):
    '''
    (list)->list
    Precondition rectangle is a list [x1,y1,x2,y2]
    ''' 
    
    orientation = path_orientation(rectangle)
    rectangle = blTr(rectangle)
    
    
    if orientation == "down":
        return [rectangle[2],800-rectangle[3],rectangle[0],800-rectangle[1]]
    elif orientation == "left":
        return [rectangle[2],800-rectangle[1],rectangle[0],800-rectangle[3]]
    elif orientation == "right":
        return [rectangle[0],800-rectangle[3],rectangle[2],800-rectangle[1]]
    else:
        return [rectangle[0], 800-rectangle[1], rectangle[2], 800-rectangle[3]]
    
    
def intersect(rectangle, lst):
    '''
    (list,list)->
    Precondition : rectangle is a list [x1,x2,y1,2] and lst is a list of rectangles
    
    find if rectangles intersects with anything in lst
    '''
    '''
    for rectangles in lst:
        max(rectangle[0],rectangle[2],rectangles[0],rectangles[2])
        if (rectangle[0] > rectangles[0] and rectangle[0] > rectangle[2] or 
            rectangle[2] > rectangles[0] and rectangle[2] > rectangles[2]):#rectangle x is max
    '''     
    
    #Check if rectangle is within the borders of the window
    if (min(rectangle[0], rectangle[1], rectangle[2], rectangle[3]) < 0
        or max(rectangle[0], rectangle[1], rectangle[2], rectangle[3]) > 800):
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

def reset(event):
    canvas.delete("all")
    
    
    rectangle= blTr([485, 800, 515, 700])
    canvas.create_rectangle(rectangle, fill="red")
    rectangle_group= []
    rectangle_group.append(rectangle)
    
    potential_rectangle = create_path(rectangle, path_orientation(rectangle))
    
    for i in range(500):
        if intersect(potential_rectangle, rectangle_group) == False:
            rectangle = potential_rectangle
            rectangle_group.append(rectangle)
            canvas.create_rectangle(rectangle)
            #, fill=color[i]
         
        potential_rectangle = create_path(rectangle, path_orientation(rectangle))
    canvas.create_rectangle(rectangle_group[-1][0], rectangle_group[-1][1], rectangle_group[-1][2], rectangle_group[-1][3], fill = "green")
    for i in range(len(rectangle_group)-1):
        make_connection(rectangle_group[i],rectangle_group[i+1])
    
root.title('Maze Rush')
root.geometry("800x800")
root.config(cursor="circle #FF00FF")
root.configure(bg="white")

canvas = Canvas(root, width=1000, height = 800)
canvas.pack()
   
canvas.configure(bg="white")
   

#root.bind('<Motion>', motion)
             

######################################

'''
rectangle = []
for i in range(100):
    create_path(, orientation)
'''
#canvas.create_rectangle(385,740,415,640)
#rectangle = [385,740,415,640]
rectangle= blTr([485, 800, 515, 700])
canvas.create_rectangle(rectangle, fill="red")
rectangle_group= []
rectangle_group.append(rectangle)
color = ["blue","red","pink","brown","green","orange","yellow","cyan","lime","cyan","silver"]
potential_rectangle = create_path(rectangle, path_orientation(rectangle)) 
#canvas.create_rectangle(624, 300, 594, 185)
#canvas.create_rectangle(639, 118, 609, 250)
print(path_orientation(rectangle))
for i in range(500):
    if intersect(potential_rectangle, rectangle_group) == False:
        rectangle = potential_rectangle
        rectangle_group.append(rectangle)
        canvas.create_rectangle(rectangle)
        #, fill=color[i]
        
    potential_rectangle = create_path(rectangle, path_orientation(rectangle))
canvas.create_rectangle(rectangle_group[-1][0], rectangle_group[-1][1], rectangle_group[-1][2], rectangle_group[-1][3], fill = "green")

for i in range(len(rectangle_group)-1):
    make_connection(rectangle_group[i],rectangle_group[i+1])
###################################################

root.bind("<space>", reset)
#canvas.create_rectangle([200,400,230,600], fill="white")




move_mouse_to(500, 1000)
root.mainloop()

