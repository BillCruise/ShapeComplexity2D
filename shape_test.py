# Test several different shapes to see if their shape complexity passes
# a basic sanity test.  Regular shapes (circle, triangle, square) should
# score a relatively low complexity.

from shape_complexity_2d.shape_complexity_2d import *

def main():
  
    triangle = [ [ 0.0, 0.0 ], [ 1.0, 1.5 ], [ 2.0, 3.0 ], [ 3.0, 4.5 ],
                 [ 4.0, 6.0 ], [ 5.0, 7.5 ], [ 6.0, 9.0 ], [ 7.0, 10.5 ],
                 [ 8.0, 12.0 ], [ 9.0, 13.5 ], [ 10.0, 15.0 ], [ 11.0, 13.5 ],
                 [ 12.0, 12.0 ], [ 13.0, 10.5 ], [ 14.0, 9.0 ], [ 15.0, 7.5 ],
                 [ 16.0, 6.0 ], [ 17.0, 4.5 ], [ 18.0, 3.0 ], [ 18.0, 2.5 ],
                 [ 20.0, 0.0 ], [ 18.0, 0.0 ], [ 16.0, 0.0 ], [ 14.0, 0.0 ],
                 [ 12.0, 0.0 ], [ 10.0, 0.0 ], [ 8.0, 0.0 ], [ 6.0, 0.0 ],
                 [ 4.0, 0.0 ], [ 2.0, 0.0 ], [ 0.0, 0.0 ] ]

    print 'Triangle Points:', len(triangle)
    complexity = shape_complexity(triangle)
    print 'Triangle Complexity:', complexity

    rectangle = [ [ -10.0, 10.0 ], [ -8.0, 10.0 ], [ -6.0, 10.0 ], [ -4.0, 10.0 ],
                  [ -2.0, 10.0 ], [  0.0, 10.0 ], [  2.0, 10.0 ], [  4.0, 10.0 ],
                  [  6.0, 10.0 ], [  8.0, 10.0 ], [ 10.0, 10.0 ], [ 10.0,  8.0 ],
                  [ 10.0,  6.0 ], [ 10.0,  4.0 ], [ 10.0,  2.0 ], [ 10.0,  0.0 ],
                  [  8.0,  0.0 ], [  6.0,  0.0 ], [  4.0,  0.0 ], [  2.0,  0.0 ],
                  [  0.0,  0.0 ], [ -2.0,  0.0 ], [ -4.0,  0.0 ], [ -6.0,  0.0 ],
                  [ -8.0,  0.0 ], [ -10.0,  0.0 ], [ -10.0,  2.0 ], [ -10.0,  4.0 ],
                  [ -10.0,  6.0 ], [ -10.0,  8.0 ], [ -10.0, 10.0 ] ]

    print
    print 'Rectangle Points:', len(rectangle)
    complexity = shape_complexity(rectangle)
    print 'Rectangle Complexity:', complexity


    trapezoid = [ [ -10.0, 10.0 ], [ -8.0, 10.0 ], [ -6.0, 10.0 ], [ -4.0, 10.0 ],
                  [ -2.0, 10.0 ], [  0.0, 10.0 ], [  2.0, 10.0 ], [  4.0, 10.0 ],
                  [  6.0, 10.0 ], [  8.0, 10.0 ], [ 10.0, 10.0 ], [  8.0,  8.0 ],
                  [  6.0,  6.0 ], [  4.0,  4.0 ], [  2.0,  2.0 ], [  0.0,  0.0 ],
                  [ -2.0,  0.0 ], [ -4.0,  0.0 ], [ -6.0,  0.0 ], [ -8.0,  0.0 ],
                  [ -10.0, 0.0 ], [ -10.0, 2.0 ], [ -10.0, 4.0 ], [ -10.0, 6.0 ],
                  [ -10.0, 8.0 ], [ -10.0, 10.0 ] ]

    print
    print 'Trapezoid Points:', len(trapezoid)
    complexity = shape_complexity(trapezoid)
    print 'Trapezoid Complexity:', complexity


    circle = [ [ 9.78147600733, 2.07911690817 ],
               [ 9.13545457642, 4.06736643075 ],
               [ 8.09016994374, 5.87785252292 ],
               [ 6.69130606358, 7.43144825477 ],
               [ 5.0, 8.66025403784 ],
               [ 3.09016994374, 9.51056516295 ],
               [ 1.04528463267, 9.94521895368 ],
               [-1.04528463267, 9.94521895368 ],
               [-3.09016994374, 9.51056516295 ],
               [-5.0, 8.66025403784 ],
               [-6.69130606358, 7.43144825477 ],
               [-8.09016994374, 5.87785252292 ],
               [-9.13545457642, 4.06736643075 ],
               [-9.78147600733, 2.07911690817 ],
               [-10.01, 0.0 ],
               [-9.78147600735, -2.07911690817 ],
               [-9.13545457642, -4.06736643075 ],
               [-8.09016994374, -5.87785252292 ],
               [-6.69130606358, -7.43144825477 ],
               [-5.0, -8.66025403784 ],
               [-3.09016994374, -9.51056516295 ],
               [-1.04528463267, -9.94521895368 ],
               [ 1.04528463267, -9.94521895368 ],
               [ 3.09016994374, -9.51056516295 ],
               [ 5.0, -8.66025403784 ],
               [ 6.69130606358, -7.43144825477 ],
               [ 8.09016994374, -5.87785252292 ],
               [ 9.13545457642, -4.06736643075 ],
               [ 9.78147600733, -2.07911690817 ],
               [ 10.01, 0.0 ],
               [ 9.78147600735, 2.079116908177 ] ]
               
    print
    print 'Circle Points:', len(circle)
    complexity = shape_complexity(circle)
    print 'Circle Complexity:', complexity


    # Small set of sample data from the congressional districts file
    island = [ [ -65.4714659849815, 18.0883655505946 ],
               [ -65.4719391423540, 18.0869349608806 ],
               [ -65.4728622797367, 18.0869408023297 ],
               [ -65.4737776913319, 18.0879001190096 ],
               [ -65.4737701539783, 18.0893307087237 ],
               [ -65.4723815850106, 18.0907554569886 ],
               [ -65.4719238792129, 18.0893229829362 ],
               [ -65.4714659849815, 18.0883655505946 ] ]

    print
    print 'Island Points:', len(island)
    complexity = shape_complexity(island)
    print 'Island Complexity:', complexity


if __name__ == '__main__':
    main()  
