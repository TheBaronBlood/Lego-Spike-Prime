import color_sensor, motor, runloop
from hub import port

 
async def main():
    ###########
    Kp = 0
    Ki = 0
    Kd = 0 
    ###########

    L_ColorSensor_Reflection = color_sensor.reflection(port.E) # Hier Definieren wir den Linken Color Sensor
    R_ColorSensor_Reflection = color_sensor.reflection(port.F) # Hier Definierne wir den Rechten Color Sensor


    def LineFollow(Kp, Kd, Ki): # Hier Erstellen wir die Funktion, mit den Parametern Kp, Kd, Ki, die später aufgerufen wird

        P = 0
        I = 0
        D = 0
        error = 0
        last_error = 0

        DriveSpeed = 500 # Hier gen wir den Motor Geschwindigkeit an
    #############################

        error = (L_ColorSensor_Reflection - R_ColorSensor_Reflection) # Hier Definieren wir den Error

        P = error                   # Gibt an wie Schnell er auf den Error reagieren soll
        I = I + error               # Da der P-Regler den SOLLWERT erreichen kann Integrieren wir den Wert etwas Hoch und er erreicht nun den Wert 0 und drüber hinaus
        D = error - last_error      # Da aber wir so viele Abweichungen Drüber und Drunkter haben Merzen wir diese aus in dem Wir schauen Wie oft dies in den Letzen malen Passiert ist.

        PIDturn = (Kp * P) + (Ki * I) + (Kd * D) # Hier kommen die ganzen Reglern zusammen zu einem Regler, dem PID-Regler
        last_error = error # Hier sagen wir das der Aktuelle Error nun der letzt Error ist für den Nächsten Ablauf der Funktion

        L_Turn = PIDturn - DriveSpeed # Hier geben wir dem Motor an wie schnell er sich Drehen soll, von dem Ebend ausgerechneten PID
        R_Turn = PIDturn + DriveSpeed # Hier geben wir dem Motor an wie schnell er sich Drehen soll, von dem Ebend ausgerechneten PID
    ######################################
        # LEFT #
    # Hier sagen wir das die Geschwindigkeit niemals über 255 gehen soll und auch nicht unter 0
        if(L_Turn > 255):
            L_Turn = 255

        if(L_Turn < 0):
            L_Turn = 0

    ######################################
        # RIGHT #
    # Hier sagen wir das die Geschwindigkeit niemals über 255 gehen soll und auch nicht unter 0
        if(R_Turn > 255):
            R_Turn = 255

        if(R_Turn < 0):
            R_Turn = 0

    ######################################
        motor.run(port.A, L_Turn)
        motor.run(port.B, R_Turn)



    while True: # Hier sagen wir das das Untere Unendlich wiederholt werden soll 
        Kp = 0.0006                 # Hier wegenwir die Regler Werte
        Kd = 10 * Kp
        Ki = 0.0001
        LineFollow(Kp, Kd, Ki)      # Hier Führen wir die Funktion auf

runloop.run(main())
