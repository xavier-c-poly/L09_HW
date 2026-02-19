"""

MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME
MAKE SURE TO COMMIT ALL THE TIME

"""



from math import sin, cos, radians

import altair as alt
import pandas as pd
import streamlit as st
import random


## Represent a cannonball, tracking its position and velocity.
#
class Cannonball:
    ## Create a new cannonball at the provided x position.
    #  @param x the x position of the ball
    #
    def __init__(self, x):
        self._x = x
        self._y = 0
        self._vx = 0
        self._vy = 0
        self._print_iface = Print_Iface()

    ## Move the cannon ball, using its current velocities.
    #  @param sec the amount of time that has elapsed.
    #
    def move(self, sec, grav):
        dx = self._vx * sec
        dy = self._vy * sec

        self._vy = self._vy - grav * sec

        self._x = self._x + dx
        self._y = self._y + dy

    ## Get the current x position of the ball.
    #  @return the x position of the ball
    #
    def getX(self):
        return self._x

    ## Get the current y position of the ball.
    #  @return the y position of the ball
    #
    def getY(self):
        return self._y

    ## Shoot the canon ball.
    #  @param angle the angle of the cannon (radians)
    #  @param velocity the initial velocity of the ball
    #
    def shoot(self, angle, velocity, user_grav, step=0.1):
        self._vx = velocity * cos(angle)
        self._vy = velocity * sin(angle)
        self.move(step, user_grav)

        while self.getY() > 1e-14:
            self._print_iface.addX(self.getX())
            self._print_iface.addY(self.getY())
            self.move(step, user_grav)
    def getXs(self):
        return self._print_iface.getXsInterface()
    def getYs(self):
        return self._print_iface.getYsInterface()
    
    # Print the chart for the trajectory
    # @param app the streamlit app
    #
    def printChart(self, app):
        self._print_iface.printChartInterface(app)



class Crazyball(Cannonball):
    def __init__(self, x):
        super().__init__(x)
    
    ## Move the cannon ball, using its current velocities.
    #  @param sec the amount of time that has elapsed.
    #  @param grav the amount of gravity acting on the ball.
    #
    def move(self, sec, grav):
        # Generate the random gravity and determine if its applied
        self.rand_g = random.randrange(-10, 10)
        new_grav = grav
        if self.getX() < 150:
            if grav + self.rand_g < 15 and grav + self.rand_g > 0:
                new_grav += self.rand_g
            else:
                new_grav = grav

        dx = self._vx * sec
        dy = self._vy * sec

        self._vy = self._vy - new_grav * sec

        self._x = self._x + dx
        self._y = self._y + dy



class Print_Iface:
    def __init__(self):
        self._xs = []
        self._ys = []
    def addX(self, new_x):
        self._xs.append(new_x)
    def addY(self, new_y):
        self._ys.append(new_y)
    def getXsInterface(self):
        return self._xs
    def getYsInterface(self):
        return self._ys
    def printChartInterface(self, app):
        df = pd.DataFrame({"x": self._xs, "y": self._ys})
        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("x:Q", scale=alt.Scale(domain=[0, 400]), title="Distance (m)"),
                y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 200]), title="Height (m)")
            )
            .properties(width=700, height=400)
        )
        app.altair_chart(chart, use_container_width=True)



def run_app():
    st.title("Cannonball Trajectory")

    angle_deg = st.number_input(
        "Starting angle (degrees)", min_value=0.0, max_value=90.0, value=45.0
    )
    velocity = st.selectbox("Initial velocity", options=[15, 25, 40], index=1)

    gravity_options = {"Earth": 9.81, "Moon": 1.63}
    gravity_name = st.selectbox("Gravity", options=list(gravity_options.keys()), index=0)
    gravity = gravity_options[gravity_name]
    step = .1

    col1, col2 = st.columns(2)
    simulate = col1.button("Simulate")
    crazy_simulate = col2.button("Crazy Simulate")

    if simulate or crazy_simulate:
        angle_rad = radians(angle_deg)

        if simulate:
            ball = Cannonball(0)
        elif crazy_simulate:
            ball = Crazyball(0)

        ball.shoot(angle_rad, velocity, gravity, step)

        if not ball.getXs():
            st.warning("No trajectory points were generated.")
            return

        ball.printChart(st)


if __name__ == "__main__":
    run_app()
