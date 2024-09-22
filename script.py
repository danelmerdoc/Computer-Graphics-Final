import mdl
from display import *
from matrix import *
from draw import *

def pass_0 (commands): 
    nFrames = 1
    frames = False
    vary = False
    basename = False
    name = "image"
    for command in commands:
        c = command["op"]
        if (c == "frames"):
            frames = True
            nFrames = int(command['args'][0])
        if (c == "vary"):
            vary = True
        if (c == "basename"):
            basename = True
            name = command["args"][0]
    
    if frames and not basename: 
        print("Warning! basename not found.")
        
    if vary and not frames: 
        raise Exception("frames not found")
    
    return (name,nFrames)
            
def pass_1(commands, nFrames):
    frames = [ {} for i in range(nFrames)]
    
    for command in commands:
        c = command["op"]
        if (c == "vary"):
            knob = command["knob"]
            (start, end, a, b) = command["args"]
            i = a
            di = (b-a)/(int(end)-int(start))
            for frame in range(int(start), int(end) + 1):
                frames[frame][knob] = i
                i += di
    return frames

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]
    shading = 'flat'

    color = [0, 0, 0]
    
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    
    (name, nFrames) = pass_0(commands)
    frames = pass_1(commands, nFrames)
    
    for frame in range(nFrames):
        tmp = new_matrix()
        ident(tmp)
        stack = [[x[:] for x in tmp]]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []
        sample = ''
        
        for command in commands:
            print(command)
            c = command['op']
            args = command['args']

            knob = 1
            if nFrames > 1 and'knob' in command and command['knob'] != None:
                    knob = frames[frame][command['knob']]
            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == "sample":
                sample = command['sample_type']


            elif c == 'shading':
                shading = command['shade_type']

            elif c == 'mesh':
                if command['constants']:
                    reflect = command['constants'] if command['constants'] != ':' else '.white'
                add_mesh(tmp, command['cs'])
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'

            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                        args[0], args[1], args[2], args[3], step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'

            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                        args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                        args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult(stack[-1], tmp)
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                tmp = make_translate(args[0] * knob, args[1] * knob, args[2] * knob)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                tmp = make_scale(args[0] * knob , args[1] * knob, args[2] * knob)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                theta = args[1] * (math.pi / 180)
                if args[0] == 'x':
                    tmp = make_rotX(theta * knob)
                elif args[0] == 'y':
                    tmp = make_rotY(theta * knob)
                else:
                    tmp = make_rotZ(theta * knob)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]])
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
            
        if (nFrames > 1):
            save_extension(screen, "animation/" + name + str(frame) + ".png")
    if nFrames > 1:
        animate(name)
                
        
