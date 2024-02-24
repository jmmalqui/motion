# Animator 
Lightweight Animation Library


# Usage 
```py
import animator 
myanim = animator.Animator()

myanim.add_frame(start=[0,0],end=[10,10], duration_ms=200, easing_type=animator.curves.ease_in_sine)
"""
start, end = an int, float or a list that contains the two beforementioned
duration_ms: length in miliseconds between two keyframes
easing_type: an easing function, a custom one can be used as long as the range of it is [0,1]
"""
myanim.add_frame(start=[10,10],end=[20,20], duration_ms=300, easing_type=animator.curves.ease_in_out_sine)

myanim.play(loops=3,loop_type=LoopType.CLOSED)
"""
loops: the amount of loops the animation will perform, if set to 0 it will perform indefinitely
loop_type:  0 (LoopType.ONEWAY) makes the animation perform from frame 0 to the last frame, 
            then returning to frame 0 without going through the frames between
            1 (LoopType.CLOSED) makes the animation perform from frame 0 to the last frame, 
            then returning to frame 0 going through the frames between
"""

while True:
    myanim.update()
    value = myanim.get_value()
    """
    get_value() returns the current value the animation is in, if play() was not called before then it returns None
    """
```