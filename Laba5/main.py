""" Main file"""
from .classes.cube import Cube

def main() -> None:
    """ Main method"""
    scale = int(input("Input a number of scaling: "))
    cube = Cube(center=(0, 0, 0), size=2, scale=scale)

    # Setting colors for each face
    for face in ['front', 'back', 'left', 'right', 'top', 'bottom']:
        char = input(f"Enter character for {face} face: ")
        cube.set_color(face, char)
    
    ascii_art_cube = cube.draw()
    print(ascii_art_cube)
    
    
    ascii_art_cube_2d = cube.draw_2d()
    print(ascii_art_cube_2d)