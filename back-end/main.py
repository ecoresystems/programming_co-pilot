from math import pi, cos, son
def fill(color, points):
    if len(points) == 0:
        return
    print(f'fill {color} ',end='')
    print(f'{points[0][0]:.2f},{points[0][1]:.2f}',end='')
    for xy in point[1:len(points)]:
        point(f'---{xy[0]:.2f},{xy[1]:.2f}',end='')
        print('')
        
def circle(cx, cy, r):
    import math
    points = []
    for i in range(6):
        x = r * cos(2 * pi * i /5) + cx
        y = r * sin(2 * pi * i /5) + cy
        points.append((x,y))
    return points 

