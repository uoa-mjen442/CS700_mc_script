Initial design

Model solar power readings as a sine wave with amplitude 200, +ve offset 200, generating only a live reading.
model prediction program readings as the same, but as an array of values over time.
battery charge is approximated as an int from 0 to 10,000. Once a second, we add power to it equal to the value of the solar power voltage reading at the time
and subtract power from it equal to the output voltage at the time
the battery output voltage can be chosen from 0 to x where x is the current battery charge time. 

the objective of the program is to try to make a program using conventional/functional logic that adjusts the battery output voltage based on the conditions
in such a way that the output remains as smooth as possible, and the battery is never overcharged or undercharged.

Bonus points for maintaining the battery voltage within 80-90% of capacity
Optional addition: add some soft randomness to prediction values and try to keep the output waveform smooth.
