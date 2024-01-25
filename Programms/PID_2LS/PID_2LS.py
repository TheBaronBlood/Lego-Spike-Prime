import color_sensor, motor, runloop
from hub import port, button
from app import linegraph
import asyncio

async def main():

    ############ Hier wegenwir die Regler Werte
    Kp = 2.2   # ROT
    Kd = 0.001  # GRÜN
    Ki = 0.001   
    ###########

    L = 0
    R = 0
    I = 0
    Error = 0
    a = 0
    Setpoint = 0
    Last_Error = 0
    DriveSpeed = 200

    linegraph.clear_all()

    while not button.pressed(button.LEFT):

        L = color_sensor.reflection(port.F)
        R = color_sensor.reflection(port.D)

        #await asyncio.sleep(0.1)# Add a small delay to avoid high-frequency printing

        ########## P I D ############

        Error = R - L # (LÖSUNG: war es einfach von L - R --> R - L)

        P = Error
        I = I + Error
        D = Last_Error

        PIDturn = (Kp * P) + (Ki * I) + (Kd * D)
        Last_Error = Error


        motor.run(port.B, int(PIDturn - DriveSpeed))
        motor.run(port.A, int(PIDturn + DriveSpeed))

    
        a += 1# Inkrementierung der Zählvariable

        linegraph.plot(0, x=a, y=0)
        linegraph.plot(9, x=a, y=Error)# Plotte den aktuellen PID-Wert        ROT
        linegraph.plot(3, x=a, y=PIDturn)# Plotte den aktuellen PID-Wert      BLAU
        linegraph.plot(6, x=a, y=D)# Plotte den aktuellen PID-Wert            GRÜN
        #await asyncio.sleep(0.1)
        linegraph.show(False)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
