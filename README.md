# Animator 
Lightweight Animation Library


# Usage 
```py
import animator 
myanim = animator.animator()
myanim.add_frame(start=[0,0],end=[10,10], duration_ms=200, easing_type=animator.curves.ease_in_sine)
myanim.add_frame(start=[10,10],end=[20,20], duration_ms=300, easing_type=animator.curves.ease_in_out_sine)
myanim.play(loops=3,looptype=LoopType.CLOSED)
while True:
    myanim.update()
    value = myanim.get_value()
```