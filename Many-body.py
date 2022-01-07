"""
A simulation using Tkinter of the manybody problem. The bodies are constrained to move on a two dimensional plane, 
which is our Tkinter window. The many body problem is solved by Euler integration. Remember that tkinter places the 
(0, 0) in the upper left corner
Video: https://www.youtube.com/watch?v=H8OBbCtSQnI
"""
import tkinter as tk
import numpy as np
from time import sleep

# Gravitational constant G in N·m^2·kg^(-2)
GRAVITATIONAL_CONSTANT = 0.01

class Body:
    """
    A class that defines a spherical body affected which defines several methods: one for calculating the gravitational force 
    a body suffers because other body other for calculating collisions with other bodies and solid edges. Has a mass, a position,
    a velocity and the height and width of the box the bodies are in.
    It is implied that its density is 1, thus its radius can be defined with the inverse of the volume formula of a sphere.
    """
    def __init__(self, mass: int, position: list, velocity: list, box_width=700, box_height=700): # self, mass: int, position: list, velocity: list, box_width=700, box_height=700
        self.mass = mass

        self.position = np.array(position, dtype=float)
        self.position_y = position[1]
        self.position_x = position[0]

        self.velocity = np.array(velocity, dtype=float)
        
        self.radius = (self.mass / np.pi)**(1/3)
        # List of positions of the body for animation purposes (currently not used)
        self.Logx = list()
        self.Logy = list()
        # The bodies will live in a box they cannot leave
        self.box_width = box_width
        self.box_height = box_height

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
        if self.position[0] > self.box_width - 5:
            self.velocity[0] *= -0.9
            self.position[0] -= 1
        # Check in y direction
        if self.position[1] < 5:
            self.velocity[1] *= -0.9
            self.position[1] += 1
        if self.position[1] > self.box_height - 5:
            self.velocity[1] *= -0.9
            self.position[1] -= 1

    def update_force_g_acceleration_velocity(self, other): 
        """
        When this function is called it updates the velocity and acceleration, using 
        the force of gravity against another body and some colision force.
        dv is the infinitesimal change in velocity, the acceleration
        """
        if self == other: 
            self.dv = np.array([0, 0], dtype=float)
        else:
            # Get the distance from one body to another
            self.dist = np.linalg.norm(self.position - other.position) # np.sqrt(sum((self.position - other.position)**2))
            self.dv = np.array([0, 0], dtype=float)
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


def main(user_width=700, user_height=700, number_bodies=25):
    """
    All inputs are integers. The width and height refer to the size of the window
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

    for i in range(0, number_bodies):
        new_body = Body(
            rng.integers(10, 500),
            (rng.integers(50, user_width), rng.integers(50, user_height)), # rng.integers(50, 650, size=2)
            rng.integers(-10, 10, size=2)/20,
            user_width,
            user_height
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

            # Create create a circle that will represent the body. It's center is the position of the body
            canvas.create_oval(
                body1.position[0] - body1.radius, body1.position[1] - body1.radius,
                body1.position[0] + body1.radius, body1.position[1] + body1.radius, 
                fill="yellow"
            )
        # Update the canvas with all the new circles
        canvas.update()
        # After a certain time stop the simulation
        if T == 100_000:
            flag = False
    tk.mainloop()

if __name__ == "__main__":
    import argparse

    # Construct an argument parser
    all_args = argparse.ArgumentParser()

    # Add arguments to the parser
    all_args.add_argument("-wi", "--width", required=False, help="The width of the window")
    all_args.add_argument("-he", "--height", required=False, help="The heigth of the window")
    all_args.add_argument("-nb", "--number_bodies", required=False, help="The number of bodies")
    all_args.add_argument("-default", "--default", required=False, help="True for default parameters")
    args = vars(all_args.parse_args())

    if args["default"] or args["default"].capitalize():
        main()
    else:
        main(int(args["width"]), int(args["height"]), int(args["number_bodies"]), )