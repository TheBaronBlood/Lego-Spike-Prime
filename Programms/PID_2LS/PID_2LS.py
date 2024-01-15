import color_sensor, motor, runloop
from hub import port, button
import asyncio

async def main():

    ###########
    Kp = 0.9   # Hier wegenwir die Regler Werte
    Kd = 0.04
    Ki = 0.00005
    ###########


    L = 0
    R = 0
    I = 0
    Error = 0
    Last_Error = 0
    DriveSpeed = 150


    while not button.pressed(button.LEFT):

        L = color_sensor.reflection(port.F)
        R = color_sensor.reflection(port.D)

        #await asyncio.sleep(0.1)# Add a small delay to avoid high-frequency printing

        ########## P I D ############

        Error = R - L

        P = Error
        I = I + Error
        D = Last_Error

        PIDturn = (Kp * P) + (Ki * I) + (Kd * D)
        Last_Error = Error


        motor.run(port.B, int(PIDturn - DriveSpeed))
        motor.run(port.A, int(PIDturn + DriveSpeed))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
