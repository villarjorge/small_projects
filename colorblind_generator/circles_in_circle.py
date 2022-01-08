"""Creates a window with circles that do not overlap. 
My good intention is to create a colorblind test generator in which you can take 
any word and hide it in there
"""
import numpy as np
import tkinter as tk
from time import sleep
from PIL import Image

from numpy.core.fromnumeric import size
# This is the RNG generator
rng = np.random.default_rng()
# https://tkdocs.com/shipman/colors.html
basic_colors = ('white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta')
colorblind_colors = ("#B5CA8D", "#F7A278", "#B09C88")

class Circle:
    def __init__(self, position, radius, color) -> None:
        self.position = np.array(position, dtype=float)
        self.radius = radius
        self.color = color
    
    def is_overlapping(self, _o) -> bool:
        """A function to determine if two circle objects are overlapping"""
        distance = np.linalg.norm(self.position - _o.position)
        if distance <= self.radius + _o.radius:
            return True
        else:
            return False
    def is_any_overlapping(self, _o_list: list) -> bool:
        """A funciton to determine if the circle is overlapping with any of a list of circles provided. 
        If it does overlap with at least one it will return true
        """
        for _o in _o_list:
            distance = np.linalg.norm(self.position - _o.position)
            if distance <= self.radius + _o.radius:
                return True
        return False

def get_array_from_image():
    """Looks at the current directory for map_colorblind.png to create an array
    """
    img = Image.open("map_colorblind.png")
    return np.array(img)

def main_init():
    # Generate the circle objects
    circle_obj_list = list()
    number_of_circles = 1000
    # Invisible circle in which all the circles are going to live
    big_circle = Circle((450, 450), 400, "white")
    # Count how many times do we fail
    fails = 0
    current_radius = 10

    while number_of_circles > 0:
        # Choose a random point within the big circle
        r = big_circle.radius*np.sqrt(rng.random())
        theta = 2*np.pi*rng.random()
        random_point = (big_circle.position[0] + r*np.cos(theta), big_circle.position[1] + r*np.sin(theta))
        new_circle = Circle(
            position=random_point,
            radius=current_radius, #radius=rng.integers(10, 15), 
            color=colorblind_colors[rng.integers(0, 2)]#color=basic_colors[rng.integers(1, 7)]
            )
        #print("     ", new_circle.position)
        # If the circle is overlapping or too far away repeat
        if len(circle_obj_list) == 0:
            circle_obj_list.append(new_circle)
            number_of_circles -= 1
            #print(f"First time. Added circle, circles left to be drawn: {number_of_circles}")
        # Check if any of the circles that we already have overlap with the new one
        elif new_circle.is_any_overlapping(circle_obj_list):
            #print(f"    Unsuitable position for the new circle, current radius {current_radius}")
            fails += 1
        else:
            circle_obj_list.append(new_circle)
            number_of_circles -= 1
            #print(f"Added circle, circles left to be drawn: {number_of_circles}, fails: {fails}, current radius: {current_radius}")
            # Reset fails and radius. Test what is the difference with reseting and not reseting the radius
            fails = 0
            #current_radius = 19
        # if it fails alot reduce the size of the circle
        if fails >= 500:
            current_radius -= 1
            fails = 0
            #print(f"     Radius reduced, new radius {current_radius}")
            #if fails >= 1000:
                #print("Can't make it, door stuck!")
                #break
        # We do not want a radius that is less than zero
        if current_radius <= 2:
            print("Radius got too small")
            break
    # Loop through the circles to determine which to change their color
    img_array = get_array_from_image()
    for circle in circle_obj_list:
        # If we go to the image provided and there is black, the circle will be another color
        # We suppose that there is only black and white in the image
        if img_array[int(circle.position[1])][int(circle.position[0])][0] == 0:
            circle.color = "#B5CA9D"
    print("Colors updated")
    print(f" Final number of circles: {len(circle_obj_list)}")
    return circle_obj_list

def main_tk_loop(objs):
    # Create the Tkinter window and give a title
    root = tk.Tk()
    root.wm_title("Circles :-------(")
    # Create the canvas, white
    canvas = tk.Canvas(root, width=900, height=900, bg="white")
    canvas.grid(row=0, column=0) 
    # Loop through the objects and draw them
    for circle in objs:
        canvas.create_oval(
            #circle.position[0] + np.sqrt(2)*circle.radius, circle.position[1] + np.sqrt(2)*circle.radius,
            #circle.position[0] - np.sqrt(2)*circle.radius, circle.position[1] - np.sqrt(2)*circle.radius,
            circle.position[0] + circle.radius, circle.position[1] + circle.radius,
            circle.position[0] - circle.radius, circle.position[1] - circle.radius,
            fill=circle.color
        )
    canvas.update()

    tk.mainloop()
    
if __name__ == "__main__":
    circle_obj_list = main_init()
    main_tk_loop(circle_obj_list)
