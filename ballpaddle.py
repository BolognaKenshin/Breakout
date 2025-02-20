from turtle import Turtle

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.angle_counter = 1
        self.shape("circle")
        self.color("white")
        # hit_counter is used for speed calculation
        self.hit_counter = 0
        # left/right counters are used to help calculate angle
        self.left_hit_counter = 0
        self.right_hit_counter = 0
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.05
        self.goto(0, -280)

    def move(self):
        if self.angle_counter > 1:
            new_x = self.xcor() + (self.x_move * (self.angle_counter / 2))
        else:
            new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def bounce_left(self):
        if self.x_move > 0:
            self.x_move *= -1

    def bounce_right(self):
        if self.x_move < 0:
            self.x_move *= -1

    def reset_position(self):
        self.goto(0, -140)
        self.bounce_x()


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(position)
        self.paddle_2 = None

    def go_right(self):
        new_x = self.xcor() + 40
        if new_x < 380:
            self.goto(new_x, self.ycor())
            if self.paddle_2:
                new_x = self.paddle_2.xcor() + 40
                self.paddle_2.goto(new_x, self.ycor())

    def go_left(self):
        new_x = self.xcor() - 40
        if self.paddle_2:
            if new_x > -320:
                self.goto(new_x, self.ycor())
                p2_new_x = self.paddle_2.xcor() - 40
                self.paddle_2.goto(p2_new_x, self.ycor())
        else:
            if new_x > -400:
                self.goto(new_x, self.ycor())

