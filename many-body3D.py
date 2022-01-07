"""
A simulation of the manybody problem in three dimensions. The spherical bodies are projected into a
two dimensional plane. The problem is solved using euler integration
"""

import tkinter as tk
import numpy as np
#from time import sleep
import argparse


# Gravitational constant G in N·m^2·kg^(-2)
GRAVITATIONAL_CONSTANT = 0.01

class Body3D:
    """
    A class that defines a spherical body affected which defines several methods: one for calculating the gravitational force 
    a body suffers because other body other for calculating collisions with other bodies and solid edges. Has a mass, a position,
    a velocity and the height and width of the box the bodies are in.
    It is implied that its density is 1, thus its radius can be defined with the inverse of the volume formula of a sphere.
    """
    def __init__(self, mass: int, position: list, velocity: list, box_x=700, box_y=700, box_z=700): 
        self.mass = mass

        self.position = np.array(position, dtype=float)
        self.position_x = position[0]
        self.position_y = position[1]
        self.position_z = position[2]

        self.velocity = np.array(velocity, dtype=float)
        
        self.radius = (self.mass / np.pi)**(1/3)
        # List of positions of the body for animation purposes (currently not used)
        self.position_x_list= list()
        self.position_y_list = list()
        self.position_Z_list = list()
        # The bodies will live in a box they cannot leave
        self.box_x = box_x
        self.box_y = box_y
        self.box_z = box_z

    def check_colision(self, other):
        """
        Checks if the body is sufficiently close to another to apply a colision algorithm
        """
        # We do not neet to check if the body is colisioning with itself
        if self == other:
            return
        # If the two bodies are sufficiently close, they will:
        if self.dist < self.radius + other.radius + 5:
            # repel in an imperfect inelastic colision fasion
            self.dv *= -0.5
            # one "absorbs" the other. This could be done better
            #self.position = other.position

        # Implement solid borders that the bodies will bounce off of. The bouncd is like a inelastic colision
        # Check in x direction
        if self.position[0] < 5:
            self.velocity[0] *= -0.9
            self.position[0] += 1
        if self.position[0] > self.box_x - 5:
            self.velocity[0] *= -0.9
            self.position[0] -= 1
        # Check in y direction
        if self.position[1] < 5:
            self.velocity[1] *= -0.9
            self.position[1] += 1
        if self.position[1] > self.box_y - 5:
            self.velocity[1] *= -0.9
            self.position[1] -= 1
        # Check in z direction
        if self.position[2] < 5:
            self.velocity[2] *= -0.9
            self.position[2] += 1
        if self.position[2] > self.box_z - 5:
            self.velocity[2] *= -0.9
            self.position[2] -= 1

    def update_force_g_acceleration_velocity(self, other): 
        """
        When this function is called it updates the velocity and acceleration, using 
        the force of gravity against another body and some colision force.
        dv is the infinitesimal change in velocity, the acceleration
        """
        if self == other: 
            self.dv = np.array([0, 0, 0], dtype=float)
        else:
            # Get the distance from one body to another
            self.dist = np.linalg.norm(self.position - other.position) # np.sqrt(sum((self.position - other.position)**2))
            self.dv = np.array([0, 0, 0], dtype=float)
            # With this we avoid a division by zero
            if self.dist == 0:
                self.dv = 0
            else:
                self.F = (-GRAVITATIONAL_CONSTANT * self.mass * other.mass) * (self.position - other.position) / self.dist**3
                self.dv = self.F / self.mass
                # The check for colision needs to be here and not in the main loop so the bodies do not get inside of eachother,
                # which sends them flying
                self.check_colision(other)
        # Update the velocity
        self.velocity += self.dv
        # Update the position. This does wierd things
        #self.position += self.velocity

def main(user_width=700, user_height=700, user_length=700, number_bodies=25):
    """
    All inputs are integers. The width and height refer to the size of the window, and with the lenght to the size of
    the box the bodies occupy (the x, y, z in that order)
    """
    # Create the Tkinter window and give a title
    root = tk.Tk()
    root.wm_title("Many body")
    # Create the canvas, black
    canvas = tk.Canvas(root, width=user_width, height=user_height, bg="black")
    canvas.grid(row=0, column=0)
    
    # Define a default RNG to handle all the random things
    rng = np.random.default_rng()
    # Create a list to be populated with the bodies to be simulated
    bodies = list()
    # Define the point of "light" that creates the beams used to project
    point_view = np.array([user_width/2, user_height/2, user_length*1.25], dtype=float)
    # Define the plane where the spheres will be projected. z - K = 0
    plane_project = np.array([0, 0, 1, -user_length])
    # Define a rotation matrix in the y axis
    rotation_y = lambda beta: np.array([
        [np.cos(beta), 0, -np.sin(beta)],
        [0, 1, 0], 
        [np.sin(beta), 0, np.cos(beta)]
    ])
    angles = np.linspace(0, 2*np.pi, 100_000)
    for i in range(0, number_bodies):
        # Since the size of the balls are going to change constatly is better to not randomize the mass (size)
        new_body = Body3D(
            250,
            (rng.integers(50, user_width), rng.integers(50, user_height), rng.integers(50, user_length)), # rng.integers(50, 650, size=2)
            rng.integers(-10, 10, size=3)/20,
            user_width,
            user_height,
            user_length
        )
        bodies.append(new_body)
        print("Body created", new_body)

    # Time of the simulation and main flag
    T = 0
    flag = True

    # Main loop of the program
    while flag == True:
        # Stop the simulation for a set time, this makes low body simulations work
        #sleep(0.01)
        # Update time, since we use a timestep of one, it is not necesary to multiply by it when we update the 
        # positions and velocities
        T += 1
        # Reset the canvas
        canvas.delete("all")
        # Loop over all the bodies, use the force calculating function to update the velocity
        for body1 in bodies:
            for body2 in bodies:
                body1.update_force_g_acceleration_velocity(body2)
            # Update the position of the body
            body1.position += body1.velocity
            # Calculate the vector from the center of the body to the view point
            from_body_to_point_view = body1.position - point_view
            # Calculate the two vectors needed to create a circle with tkinter. This are the vectors that define the line 
            # that will pass through the plane
            vector_director1 = from_body_to_point_view + np.sqrt(2)*body1.radius*np.array([1, 1, 0], dtype=float)
            vector_director2 = from_body_to_point_view - np.sqrt(2)*body1.radius*np.array([1, 1, 0], dtype=float)
            # Use a formula obtained by back substitution. I would also like to do it solving a system
            parameter1 = -(plane_project[3] + body1.position[2])/vector_director1[2]
            coords1 = [
                vector_director1[0]*parameter1 + body1.position[0],
                vector_director1[1]*parameter1 + body1.position[1],
                - plane_project[3] # obviusly duh
            ]
            projected_point1 = np.array(coords1, dtype=float)
            parameter2 = -(plane_project[3] + body1.position[2])/vector_director2[2]
            coords2 = [
                vector_director2[0]*parameter2 + body1.position[0],
                vector_director2[1]*parameter2 + body1.position[1],
                - plane_project[3] # obviusly duh
            ]
            projected_point2 = np.array(coords2, dtype=float)
            # Create create a circle that will represent the body. It's center is the position of the body
            #print(projected_point1, projected_point2)
            canvas.create_oval(
                projected_point1[0], projected_point1[1],
                projected_point2[0], projected_point2[1],
                fill="yellow"
            )
        # Rotate the point of view, afterthought: you have to rotate the point and the plane, 
        #point_view = rotation_y(angles[T]).dot(point_view)
        # Rotate the plane
        #plane_project[0:3] = rotation_y(angles[T]).dot(plane_project[0:3])
        # Update the canvas with all the new circles
        canvas.update()
        # After a certain time stop the simulation
        if T == 100_000:
            flag = False
    tk.mainloop()

if __name__ == "__main__":
    # Construct an argument parser
    all_args = argparse.ArgumentParser("If you are not sure of how to run this script try setting -default False. ")

    # Add arguments to the parser
    all_args.add_argument("-wi", "--width", required=False, help="The width of the window, integer")
    all_args.add_argument("-he", "--height", required=False, help="The heigth of the window, integer")
    all_args.add_argument("-nb", "--number_bodies", required=False, help="The number of bodies, integer. Lower numbers of bodies might make the simulation run too fast")
    all_args.add_argument("-default", "--default", required=False, help="True for default parameters")
    args = vars(all_args.parse_args())

    if args["default"] or args["default"].capitalize():
        main()
    else:
        main(int(args["width"]), int(args["height"]), int(args["number_bodies"]), )