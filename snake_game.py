"""

This is a snake game programmed in python on a Raspberry Pi, making use of the SenseHat add-on board.

"""


#--- Import packages.
from sense_hat import SenseHat
from time import sleep
from random import randint

#--- RGB color variables.
snake_color = (0, 74, 9)
food = (180, 0,  15)
game_over_color = (118, 60, 69)

#--- Snake class.
class Snake:

    #--- Assign initial values to the x and y coordinates of the snake.
    def __init__(self, pos_x, pos_y):
        
        #--- Instance attributes
        self.snake_pos_x = [pos_x]                  # List of snake position x coordinates
        self.snake_pos_y = [pos_y]                  # List of snake position y coordinates
        self.MovtX = -1                             # Default movement in x axis, -1 signifies the snake is moving to the left
        self.MovtY = 0                              # Default movement in y axis, 0 signifies no movement
        self.MATRIX_MAX = 7                         # Maximum size of the LED matrix coordinates
        self.MATRIX_MIN = 0                         # Minimum size of the LED matrix coordinates
        self.generateFood = False                   # Generate food flag
        self.gameOver = False                       # Game over flag
        self.snakeMovementDelay = 0.75              # Initial delay for the snake's movement [seconds]
        self.speedUpSnakeMovement = -0.032          # Time deducted to speed up snake's movment [seconds]
        self.sense = SenseHat()                     # Initialize SenseHat class
    
    #--- Method to spawn food coordinates on the LED matrix.
    def spawn_food(self):
        while 1:
            # Generate random x and y coordinates - within the bounds of the led matrix - for the food location.
            self.food_x = randint(0, self.MATRIX_MAX)
            self.food_y = randint(0, self.MATRIX_MAX)

            # Check if any conflicts - snake and food coordinates coinciding - exists.
            self.conflicts =  [(x,y) for x, y in zip(self.snake_pos_x, self.snake_pos_y) if x == self.food_x and y == self.food_y]

            # If no conflicts exist, the food coordinates are valid, exit the loop. Otherwise the process is repeated.
            if len(self.conflicts) == 0:
                self.generateFood = False
                return False

    #--- Method to check if the food has been eaten by the snake.
    def food_check(self):
        if self.snake_pos_x[0] == self.food_x and self.snake_pos_y[0] == self.food_y:
            # Add a new element to snake position lists, then set generateFood flag to true.
            self.snake_pos_x.append(0)
            self.snake_pos_y.append(0)
            self.generateFood = True

            # Speed up the snake movement to make the game more challenging.
            self.snakeMovementDelay += self.speedUpSnakeMovement 

    #--- Method to check if the snake has bitten itself.
    def death_check(self):
        for i in range(1, len(self.snake_pos_x)): # starts at 1 because the snake can't bite its own head
            # The game is over if the snake bites itself
            if self.snake_pos_x[i] == self.snake_pos_x[0] and self.snake_pos_y[i] == self.snake_pos_y[0]:
                self.sense.show_message("Game Over :(", text_colour = game_over_color, back_colour= (0,0,0))
                self.sense.clear()
                self.gameOver = True

    #--- Method to ensure that snake remains within the LED matrix bounds.
    def border_control(self):
        if self.snake_pos_y[0] < self.MATRIX_MIN:
            self.snake_pos_y[0] = self.MATRIX_MAX
        elif self.snake_pos_y[0] > self.MATRIX_MAX:
            self.snake_pos_y[0] = self.MATRIX_MIN
        elif self.snake_pos_x[0] < self.MATRIX_MIN:
            self.snake_pos_x[0] = self.MATRIX_MAX
        elif self.snake_pos_x[0] > self.MATRIX_MAX:
            self.snake_pos_x[0] = self.MATRIX_MIN
    
    #--- Method to link the joystick movement to the snake movement.
    def joystick_movement(self, direction):
        """
        You can't move left then right or up then down, and vice versa.

        The following designates the direction the snake moves with each led pixel:
            up = -1
            down = 1
            left = -1
            right = 1
        A zero signifies no movement in the respective direction.
        """
        if self.MovtY != 1 and direction == "up":
            self.MovtX = 0
            self.MovtY = -1
        elif self.MovtY != -1 and direction == "down":
            self.MovtX = 0
            self.MovtY = 1
        elif self.MovtX != 1 and direction == "left":
            self.MovtX = -1
            self.MovtY = 0
        elif self.MovtX != -1 and direction == "right":
            self.MovtX = 1
            self.MovtY = 0

#--- Main function
def main():

    pos_x, pos_y = 4, 3 # Default x and y snake coordinates
    snake = Snake(pos_x, pos_y) # Initialize snake with default coordinates
    snake.sense.clear() # Clear LED matrix
    
    # Set pixel of the default snake coordinates with the snake color.
    snake.sense.set_pixel(pos_x, pos_y, snake_color)
    sleep(0.5)
    
    # Spawn food coordinates.
    snake.spawn_food() 

    # Set pixel of the food coordinates to food color.
    snake.sense.set_pixel(snake.food_x, snake.food_y, food)
    
    # Main loop.
    while not snake.gameOver:
        # Check if snake has eaten food.
        snake.food_check()

        # Assign the penultimate (from the tail) coordinates to be the tail's coordinates, then assign coordinates of the snake element before the penultimate element to be the 
        # coordinates of the penultimate element. Do this all the way to the snake's head.        
        for i in range((len(snake.snake_pos_x) - 1), 0, -1):
            snake.snake_pos_x[i] = snake.snake_pos_x[i - 1]
            snake.snake_pos_y[i] = snake.snake_pos_y[i - 1]
        
        # Update the coordinates of the head of the snake, as the other part of the snake have been updated; these coordinate updates move the snake.
        snake.snake_pos_x[0] += snake.MovtX
        snake.snake_pos_y[0] += snake.MovtY
        snake.border_control()

        # Check if the joystick was moved in any direction.
        for event in snake.sense.stick.get_events():
            if event.action == "pressed":
                snake.joystick_movement(event.direction)

        # Update/refresh LED matrix.
        snake.sense.clear()
        for x, y in zip(snake.snake_pos_x, snake.snake_pos_y):
            # Set pixels of the snake coordinates to snake color.
            snake.sense.set_pixel(x, y, snake_color)
        if snake.generateFood:
            snake.spawn_food()

        # Set pixels of the food coordinates to food color.
        snake.sense.set_pixel(snake.food_x, snake.food_y, food)

        # Snake movement delay before the next loop iteration.
        sleep(snake.snakeMovementDelay) 

        # Check if snake has bitten itself.
        snake.death_check()

if __name__ == "__main__":
    # Run main function
    main()
