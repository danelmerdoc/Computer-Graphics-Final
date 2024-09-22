from subprocess import Popen, PIPE
from os import remove, execlp
import os
from PIL import Image
import glob

#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [0, 0, 0] #[255, 255, 255]

def animate( name ):
    frames = []
    imgs = sorted(glob.glob('animation/*.png'), key= os.path.getmtime)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
    frames[0].save( name + '.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=50, loop=0)

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

def new_zbuffer( width = XRES, height = YRES ):
    zb = []
    for y in range( height ):
        row = [ float('-inf') for x in range(width) ]
        zb.append( row )
    return zb

def plot( screen, zbuffer, color, x, y, z ):
    newy = YRES - 1 - y
    z = int((z * 1000)) / 1000.0
    if ( x >= 0 and x < XRES and newy >= 0 and newy < YRES and zbuffer[newy][x] <= z):
        screen[newy][x] = color[:]
        zbuffer[newy][x] = z

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]

def clear_zbuffer( zb ):
    for y in range( len(zb) ):
        for x in range( len(zb[y]) ):
            zb[y][x] = float('-inf')

def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            f.write( bytes(pixel) )
    f.close()

def save_ppm_ascii( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):

    img = Image.new('RGB', (len(screen[0]), len(screen)))

    mdl = open('animate.mdl').read().split('\n') 
    sample = 'yes'
    for line in mdl:
        if 'sample' in line:
            sample = line.split()[1]
    
    pixels = []
    for row in screen:
        for pixel in row:
            pixels.append( tuple(pixel) )
        
    if sample == 'no':
        img.putdata(pixels)

    if sample == 'yes':
        smoothed = []
        for i in range(len(pixels)):
            if i % len(screen[0]) == 0 or i % len(screen[0]) == len(screen[0]) - 1 or i < len(screen[0]) or i > len(pixels) - len(screen[0]):
                smoothed.append(pixels[i])
            else:
                weight = 1
                r =  pixels[i][0]
                g =  pixels[i][1]
                b =  pixels[i][2]

                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if abs(j) == 1 and abs(k) == 1:
                            weight = 1 
                        elif (abs(j) == 1 and abs(k) == 0) or (abs(j) == 0 and abs(k) == 1):
                            weight = 4  
                        else:
                            weight = 9
                        r += weight * pixels[i + j * len(screen[0]) + k][0]
                        g += weight * pixels[i + j * len(screen[0]) + k][1]
                        b += weight * pixels[i + j * len(screen[0]) + k][2]
                smoothed.append((r // 29, g // 29, b // 29))
            
        img.putdata(smoothed)
    img.save(fname, 'PNG')

def display( screen):
    img = Image.new('RGB', (len(screen[0]), len(screen)))

    mdl = open('face.mdl').read().split('\n') 
    sample = 'no'
    for line in mdl:
        if 'sample' in line:
            sample = line.split()[1]
    
    pixels = []
    for row in screen:
        for pixel in row:
            pixels.append( tuple(pixel) )
        
    if sample == 'no':
        img.putdata(pixels)

    if sample == 'yes':
        smoothed = []
        for i in range(len(pixels)):
            if i % len(screen[0]) == 0 or i % len(screen[0]) == len(screen[0]) - 1 or i < len(screen[0]) or i > len(pixels) - len(screen[0]):
                smoothed.append(pixels[i])
            else:
                weight = 1
                r =  pixels[i][0]
                g =  pixels[i][1]
                b =  pixels[i][2]
                
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if abs(j) == 1 and abs(k) == 1:
                            weight = 1 
                        elif (abs(j) == 1 and abs(k) == 0) or (abs(j) == 0 and abs(k) == 1):
                            weight = 4  
                        else:
                            weight = 9
                       
                        r += weight * pixels[i + j * len(screen[0]) + k][0]
                        g += weight * pixels[i + j * len(screen[0]) + k][1]
                        b += weight * pixels[i + j * len(screen[0]) + k][2]
                smoothed.append((r // 29, g // 29, b // 29))
            
        img.putdata(smoothed)
    img.show()

