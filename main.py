from ballpaddle import Ball, Paddle
from brickmanager import BrickManager, ScoreBoard
from turtle import Screen
import time

screen = Screen()
screen.bgcolor("black")
screen.setup(width=900, height=800)
screen.title("Breakout")
screen.tracer(0)

bm = BrickManager()
sb = ScoreBoard()
ball = Ball()
paddle_1 = Paddle((50, -320))
paddle_1.paddle_2 = Paddle((-50, -320))

screen.listen()
screen.onkeypress(paddle_1.go_right, "Right")
screen.onkeypress(paddle_1.go_left, "Left")

bm.draw_walls()
bm.draw_bricks(bm.yellow, "yellow", -395, -100)
bm.draw_bricks(bm.green, "green", -395, -10)
bm.draw_bricks(bm.orange, "orange", -395, 80)
bm.draw_bricks(bm.red, "red", -395, 170)

game_ongoing = True
paddle_hit = False
lose_life = True
first_screen = True
can_wall_bounce = True

while game_ongoing:

    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Top wall bouncing - Removes double paddle when ball hits top wall
    if ball.ycor() >= 300:
        ball.bounce_y()
        if paddle_1.paddle_2:
            paddle_1.paddle_2.hideturtle()
            paddle_1.paddle_2.clear()
            paddle_1.paddle_2 = None

    # Left/Right wall bouncing
    if (ball.xcor() >= 400 or ball.xcor() <= -410) and can_wall_bounce:
        ball.bounce_x()
        can_wall_bounce = False

    if ball.xcor() > -380 or ball.xcor() < 370:
        can_wall_bounce = True


    # Detects collision with paddle, moves ball
    if paddle_hit == False:
        # Detection for double paddle - Detects left or right paddle hit for bouncing direction
        if paddle_1.paddle_2:
            # Right Paddle
            if ball.distance(paddle_1) < 20 or (ball.distance(paddle_1) < 50 and ball.ycor() < -290):
                ball.bounce_right()
                ball.bounce_y()
                paddle_hit = True
                can_wall_bounce = True
                if ball.left_hit_counter > 1:
                    ball.angle_counter -= 1
                    ball.left_hit_counter -= 1
                else:
                    ball.angle_counter += 1
                    ball.right_hit_counter += 1
            # Left Paddle
            elif ball.distance(paddle_1.paddle_2) < 20 or (ball.distance(paddle_1.paddle_2) < 50 and ball.ycor() < -290):
                ball.bounce_left()
                ball.bounce_y()
                paddle_hit = True
                can_wall_bounce = True
                if ball.right_hit_counter > 1:
                    ball.angle_counter -= 1
                    ball.right_hit_counter -= 1
                else:
                    ball.angle_counter += 1
                    ball.left_hit_counter += 1

        # Detection for single paddle - Detects left/right side for bouncing direction
        else:
            if ball.distance(paddle_1) < 50 and ball.ycor() < -290:
                # Left Side
                if (paddle_1.xcor()) > ball.xcor() > (paddle_1.xcor() - 50):
                    ball.bounce_left()
                    can_wall_bounce = True
                    if ball.right_hit_counter > 1:
                        ball.angle_counter -= 1
                        ball.right_hit_counter -= 1
                    else:
                        ball.angle_counter += 1
                        ball.left_hit_counter += 1
                # Right Side
                elif (paddle_1.xcor()) < ball.xcor() < (paddle_1.xcor() + 50):
                    ball.bounce_right()
                    can_wall_bounce = True
                    if ball.left_hit_counter > 1:
                        ball.angle_counter -= 1
                        ball.left_hit_counter -= 1
                    else:
                        ball.angle_counter += 1
                        ball.right_hit_counter += 1
                ball.bounce_y()
                paddle_hit = True

        # Reset angle_counter accordingly if it goes beyond 0 or 4
        if ball.angle_counter > 4:
            ball.angle_counter = 3
        elif ball.angle_counter < 0:
            ball.angle_counter = 1

    else:
        if ball.ycor() > -280:
            paddle_hit = False

    # Bottom wall, lose a life
    if ball.ycor() <= -350:
        if lose_life == True:
            sb.lives -= 1
            sb.update_scoreboard()
            lose_life = False
        if ball.ycor() <= -400:
            ball.angle_counter = 1
            ball.left_hit_counter = 0
            ball.right_hit_counter = 0
            ball.reset_position()
            ball.hit_counter = 0
            ball.move()
            lose_life = True
            time.sleep(3)


    # Game Over condition
    if sb.lives == 0:
        sb.game_over()
        screen.update()
        game_ongoing = False

    # Collision conditions with bricks - Increases speed if ball.hit_counter reaches 12
    y_collision = bm.detect_brick_collision(bm.yellow, ball)
    if y_collision:
        sb.score += 1
        sb.update_scoreboard()
        ball.hit_counter += 1
        can_wall_bounce = True
    g_collision = bm.detect_brick_collision(bm.green, ball)
    if g_collision:
        sb.score += 3
        sb.update_scoreboard()
        ball.hit_counter += 1
        can_wall_bounce = True
    o_collision = bm.detect_brick_collision(bm.orange, ball)
    if o_collision:
        sb.score += 5
        sb.update_scoreboard()
        ball.hit_counter = 12
        can_wall_bounce = True
    r_collision = bm.detect_brick_collision(bm.red, ball)
    if r_collision:
        sb.score += 7
        sb.update_scoreboard()
        ball.hit_counter = 12
        can_wall_bounce = True
        if paddle_1.paddle_2:
            paddle_1.paddle_2.hideturtle()
            paddle_1.paddle_2.clear()
            paddle_1.paddle_2 = None

    # Ball moves faster if counter is over 12
    if ball.hit_counter >= 12:
        ball.move_speed = .030
    else:
        ball.move_speed = .05


    # Win detection if player clears screen twice - Redraws bricks the first time player clears
    if bm.yellow == [] and bm.green == [] and bm.orange == [] and bm.red ==[]:
        if first_screen:
            bm.draw_bricks(bm.yellow, "yellow", -395, -100)
            bm.draw_bricks(bm.green, "green", -395, -20)
            bm.draw_bricks(bm.orange, "orange", -395, 60)
            bm.draw_bricks(bm.red, "red", -395, 140)
            first_screen = False
        else:
            sb.player_wins()
            game_ongoing = False



screen.exitonclick()