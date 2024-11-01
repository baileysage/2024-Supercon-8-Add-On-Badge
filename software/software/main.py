from machine import I2C, Pin
import time

counter = 0
# Extraneous beginning byte so I don't have to re-index
led_state = bytearray(9)

## do a quick spiral to test
if petal_bus:
    for j in range(7):
        which_leds = (1 << (j+1)) - 1 
        for i in range(1,9):
            print(which_leds)
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
            time.sleep_ms(30)
    for i in range(1,9):
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([0x00]))
    
while True:

    ## display button status on RGB
    if petal_bus:
        if not buttonA.value():
            led_state[2] = led_state[2] | 0x80
        else:
            led_state[2] = led_state[2] & 0x7F

        if not buttonB.value():
            led_state[3] = led_state[3] | 0x80
        else:
            led_state[3] = led_state[3] & 0x7F

        if not buttonC.value():
            led_state[4] = led_state[4] | 0x80
        else:
            led_state[4] = led_state[4] & 0x7F

    ## see what's going on with the touch wheel
    if touchwheel_bus:
        tw = touchwheel_read(touchwheel_bus)

    ## display touchwheel on petal
    if petal_bus:
        if touchwheel_bus:
            if tw > 0:
                tw = (128 - tw) % 256 
                petal = int(tw/32) + 1
            else: 
                petal = 999
            for i in range(1,9):
                if i == petal:
                    led_state[i] = led_state[i] | 0x7F
                else:
                    led_state[i] = led_state[i] & 0x80
                
        # Write updated values to board.
        for i in range(1,9):
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([led_state[i]]))
        
    time.sleep_ms(20)
    bootLED.off()

