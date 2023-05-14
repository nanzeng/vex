import math

from vex import *

# Brain should be defined by default
brain=Brain()

brain_inertial = Inertial()
left_front_motor = Motor(Ports.PORT1)
left_back_motor = Motor(Ports.PORT7)
right_front_motor = Motor(Ports.PORT6)
right_back_motor = Motor(Ports.PORT12)
controller = Controller()

# Begin project code
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

POWER_MAX = 100
POWER_MIN = 10
POWER = 50
DIRECTION = 0
ROTATION = FORWARD


class BotMotorGroup:
    def __init__(self, left_motor, right_motor) -> None:
        self._left_motor = left_motor
        self._right_motor = right_motor

    def move(self, direction):
        self._left_motor.spin(direction)
        self._right_motor.spin(direction)

    def update_velocity(self, left_motor_velocity, right_motor_velocity):
        sign = 1 if ROTATION == FORWARD else -1
        left_motor_velocity *= sign
        right_motor_velocity *= sign
        self._left_motor.set_velocity(left_motor_velocity * POWER, PERCENT)
        self._right_motor.set_velocity(right_motor_velocity * POWER, PERCENT)

    def turn(self, direction):
        self._left_motor.set_velocity(POWER, PERCENT)
        self._right_motor.set_velocity(POWER, PERCENT)
        if direction == RIGHT:
            self._left_motor.spin(FORWARD)
            self._right_motor.spin(FORWARD)
        elif direction == LEFT:
            self._left_motor.spin(REVERSE)
            self._right_motor.spin(REVERSE)

    def stop(self):
        self._left_motor.stop()
        self._right_motor.stop()


class Bot:
    def __init__(self, left_front_motor, left_back_motor, right_front_motor, right_back_motor):
        self._motor_group_a = BotMotorGroup(left_front_motor, right_back_motor)
        self._motor_group_b = BotMotorGroup(left_back_motor, right_front_motor)

        Thread(self._update_velocities)

    def move(self, direction):
        self._motor_group_a.move(direction)
        self._motor_group_b.move(direction)

    def turn(self, direction):
        self._motor_group_a.turn(direction)
        self._motor_group_b.turn(direction)

    def stop(self):
        self._motor_group_a.stop()
        self._motor_group_b.stop()

    def update_velocity(self):
        raise NotImplementedError

    def _update_velocities(self):
        while True:
            x = controller.axisC.position()
            if x == 0:
                self.update_velocity()
            wait(0.01, SECONDS)


class SwirlBot(Bot):
    def __init__(self, left_front_motor, left_back_motor, right_front_motor, right_back_motor):
        super().__init__(left_front_motor, left_back_motor, right_front_motor, right_back_motor)

    def update_velocity(self):
        theta = DIRECTION - brain_inertial.heading() / 180 * math.pi
        alpha2 = (math.pi/4 - theta) / 2
        alpha2_shift = (math.pi / 4 - alpha2)
        self._motor_group_a.update_velocity(math.cos(alpha2)**2, math.sin(alpha2)**2)
        self._motor_group_b.update_velocity(math.cos(alpha2_shift)**2, math.sin(alpha2_shift)**2)


class OmniBot(Bot):
    def __init__(self, left_front_motor, left_back_motor, right_front_motor, right_back_motor):
        super().__init__(left_front_motor, left_back_motor, right_front_motor, right_back_motor)

    def update_velocity(self):
        theta = DIRECTION - brain_inertial.heading() / 180 * math.pi
        alpha = math.pi/4 - theta
        self._motor_group_a.update_velocity(math.cos(alpha), -math.cos(alpha))
        self._motor_group_b.update_velocity(math.sin(alpha), -math.sin(alpha))


def console_print(s):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(s)


class ControllerConfig:
    def __init__(self, controller, bot):
        self._controller = controller
        self._bot = bot

        controller.axisA.changed(self.move)
        controller.axisB.changed(self.move)
        controller.buttonEUp.pressed(self.increase_power)
        controller.buttonEDown.pressed(self.decrease_power)

    def increase_power(self):
        global POWER
        POWER += 10
        if POWER > POWER_MAX:
            POWER = POWER_MAX
        console_print("Power changed to " + str(POWER))

    def decrease_power(self):
        global POWER
        POWER -= 10
        if POWER < POWER_MIN:
            POWER = POWER_MIN
        console_print("Power changed to " + str(POWER))

    def set_direction(self, x, y):
        global DIRECTION
        
        if y == 0 and x > 0:
            DIRECTION = math.pi / 2
        elif y == 0 and x < 0:
            DIRECTION = -math.pi / 2
        else:
            DIRECTION = math.atan2(x, y)

    def move(self):
        y = self._controller.axisA.position()
        x = self._controller.axisB.position()

        if x == 0 and y == 0:
            self._bot.stop()
            return

        self.set_direction(x, y)
        self._bot.move(ROTATION)

    def set_rotation(self):
        global ROTATION

        x = self._controller.axisC.position()

        if x > 0:
            ROTATION = FORWARD
        elif x < 0:
            ROTATION = REVERSE

    def turn(self):
        x = self._controller.axisC.position()
        if x > 0:
            self._bot.turn(RIGHT)
        elif x < 0:
            self._bot.turn(LEFT)
        else:
            self._bot.stop()
            

class SwirlControllerConfig(ControllerConfig):
    def __init__(self, controller, bot):
        super().__init__(controller, bot)        
        controller.axisC.changed(self.set_rotation)


class OmniControllerConfig(ControllerConfig):
    def __init__(self, controller, bot):
        super().__init__(controller, bot)        
        controller.axisC.changed(self.turn)


calibrate_drivetrain()
#swirlbot = SwirlBot(left_front_motor, left_back_motor, right_front_motor, right_back_motor)
#SwirlControllerConfig(controller, swirlbot)
omnibot = OmniBot(left_front_motor, left_back_motor, right_front_motor, right_back_motor)
OmniControllerConfig(controller, omnibot)