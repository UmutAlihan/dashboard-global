import automagica as magic

#Mouse source: https://github.com/boppreh/mouse#mouse.move

x,y = 400,400
import mouse

xy = mouse.get_position()
mouse.(xy[0], xy[1], x, y, absolute=True, duration=3)
mouse.move(x, y, duration=3)