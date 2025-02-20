from turtle import Turtle

class BrickManager:
    def __init__(self):
        self.red = []
        self.orange = []
        self.green = []
        self.yellow = []

    def draw_bricks(self, list, color, start_x, start_y):
        first_row_x = start_x
        second_row_x = start_x
        y = start_y
        for i in range(28):
            brick = Turtle()
            brick.shape("square")
            brick.shapesize(stretch_wid=1, stretch_len=2)
            brick.penup()
            brick.color(color)
            if i > 13:
                y = start_y + 45
                brick.goto(second_row_x, y)
                second_row_x += 60
            else:
                brick.goto(first_row_x, y)
                first_row_x += 60
            list.append(brick)

    def draw_walls(self):
        ceiling = Turtle()
        ceiling.color("white")
        ceiling.shape("square")
        ceiling.penup()
        ceiling.shapesize(stretch_wid=1, stretch_len=43)
        ceiling.goto(-10, 320)
        left_wall = Turtle()
        left_wall.color("white")
        left_wall.shape("square")
        left_wall.penup()
        left_wall.shapesize(stretch_wid=40, stretch_len=1)
        left_wall.goto(-440, -70)
        right_wall = Turtle()
        right_wall.color("white")
        right_wall.shape("square")
        right_wall.penup()
        right_wall.shapesize(stretch_wid=40, stretch_len=1)
        right_wall.goto(430, -70)

    # Checks for collision with a brick - Returns True when detected
    def detect_brick_collision(self, list, ball):
        for brick in list:
            collision = False
            if ball.distance(brick) < 40:
                if ((brick.ycor() - 11) > ball.ycor() or ball.ycor() > (brick.ycor() + 11)) and (brick.xcor() - 21) < ball.xcor() < (brick.xcor() + 21):
                    ball.bounce_y()
                    collision = True
                elif ((brick.xcor() - 21) > ball.xcor() or ball.xcor() > (brick.xcor() + 21)) and (brick.ycor() - 11) < ball.ycor() < (brick.ycor() + 11):
                    ball.bounce_x()
                    collision = True
                elif ball.distance(brick) < 25:
                    ball.bounce_x()
                    ball.bounce_y()
                    collision = True
                if collision:
                    brick.hideturtle()
                    list.remove(brick)
                return collision


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.score = 0
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, 360)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}         Lives: {self.lives}", align="center", font=("Verdana", 20, "bold"))

    def game_over(self):
        self.clear()
        self.write(f"GAME OVER! Score: {self.score}", align="center", font=("Verdana", 20, "bold"))

    def player_wins(self):
        self.clear()
        self.write(f"YOU WIN! Score: {self.score}", align="center", font=("Verdana", 20, "bold"))