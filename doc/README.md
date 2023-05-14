# Omnibot
## Introduction
This bot is built with Vex IQ 2nd generation components. Most of the parts are available from the competition kit. I also borrowed some beams and shafts from Hexbug build blitz. Here is a picture of it. <img src="omnibot.jpg" height="300" width="400"> It uses 4 omni-directional wheels, which are located on the 4 corners of the bot.

## Moving modes
### Omni-directional move
In this mode, the bot can move in any direction without changing its brain's heading direction. It is like sliding on the ice. To achieve this behavior, let's first work out some mathematics. Assuming all the wheels moving in the same direction, we have the following vectors to represent the wheel velocities:
|Wheel|Vector|
|--|--|
|Left front wheel|$$\vec{v_1}$$|
|Right front wheel|$$\vec{v_2}$$|
|Right back wheel|$$\vec{v_3}$$|
|Left back wheel|$$\vec{v_4}$$|

Let $\vec{v_1}$ has an angle $\alpha$ with $y$ axis. Then $\vec{v_2}$ angle is $\alpha + \frac{\pi}{2}$. $\vec{v_3}$ angle is $\alpha + \pi$. $\vec{v_4}$ angle is $\alpha + \frac{3\pi}{2}$. So we have the following equations:

$$v_1\cos\alpha + v_2\cos(\alpha+\frac{\pi}{2}) + v_3\cos(\alpha+\pi) + v_4\cos(\alpha+\frac{3\pi}{2}) = v_y$$

$$v_1\sin\alpha + v_2\sin(\alpha+\frac{\pi}{2}) + v_3\sin(\alpha+\pi) + v_4\sin(\alpha+\frac{3\pi}{2}) = v_x$$

Using the following trignometry relations:

$$\cos(\alpha+\frac{\pi}{2}) = - \sin\alpha$$

$$\cos(\alpha+\pi) = - \cos\alpha$$

$$\cos(\alpha+\frac{3\pi}{2}) = \sin\alpha$$

we have

$$v_1\cos\alpha - v_2\sin\alpha - v_3\cos\alpha + v_4\sin\alpha = v_y$$

$$v_1\sin\alpha + v_2\cos\alpha - v_3\sin\alpha - v_4\cos\alpha = v_x$$

which is

$$(v_1 - v_3)\cos\alpha - (v_2 - v_4)\sin\alpha = v_y$$

$$(v_1 - v_3)\sin\alpha + (v_2 - v_4)\cos\alpha = v_x$$

which gives

$$v_1 - v_3 = v_y\cos\alpha + v_x\sin\alpha$$

$$v_2 - v_4 = v_x\cos\alpha - v_y\sin\alpha$$

With above equations, if we want the bot to move on a straight line, we can set $v_x = 0$, which gives

$$v_1 - v_3 = v_y\cos\alpha$$

$$v_4 - v_2 = v_y\sin\alpha$$

Notice that $v_1$ and $v_3$ works as a group and $v_2$ and $v_4$ works as a group. The velocity can be arbitrary as long as the total velocity fulfills the equation specified. In general, even though $v_x$ is zero, which means the robot cann't move sideways. There can be still a rotation force along its vertical axis. Thus the bot will rotate along its vertical axis while moving in a straight line. We can make sure both wheels in the same motor group moving with same velocity, which will remove this rotation force. In this case, the velocities are

$$v_1 = -v_3 = \frac{1}{2}v_y\cos\alpha$$

$$v_4 = -v_2 = \frac{1}{2}v_y\sin\alpha$$

The negative sign means that the wheels rotate in different directions.
If we want the bot to rotate along its axis, with the following equations

$$\cos{2\alpha} = \cos^2\alpha - \sin^2\alpha$$

$$\sin\alpha = \cos(\frac{\pi}{2}-\alpha)$$

We have 

$$v_1 - v_3 = v_y(\cos^2\frac{\alpha}{2} - \sin^2\frac{\alpha}{2})$$

$$v_4 - v_2 = v_y(\cos^2(\frac{\pi}{4}-\frac{\alpha}{2}) - \sin^2(\frac{\pi}{4}-\frac{\alpha}{2}))$$

Thus we have

$$v_1 = v_y\cos^2\frac{\alpha}{2}$$

$$v_2 = v_y\sin^2(\frac{\pi}{4} - \frac{\alpha}{2})$$

$$v_3 = v_y\sin^2\frac{\alpha}{2}$$

$$v_4 = v_y\cos^2(\frac{\pi}{4} - \frac{\alpha}{2})$$

This is just one of the solutions. We choose these formulas so that the velocity has a maximum value of $v_y$.

