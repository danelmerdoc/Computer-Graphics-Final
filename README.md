# Daniel Murdoch & Tianlang Qin

## Features Implemented
- Animation
- Mesh
    - Mesh was originally intended to support both .obj and .stl files but it doesn't -- it only supports .obj files. But hey, we only needed to do .obj files anyway. To call it, you need to call it by FILENAMEobj.
- Super Sampling
    - It's a pretty basic implementation of super-sampling. To call it in the mdl file it's just sample (yes/no). The center pixel is given a weight of 2 and the surrounding pixels are given a weight of 1. The rgb values are added up and averaged. I know Aidan did this as well. I tacked it on because I thought it was cool. 
 
We included an obj file of Dwayne 'the rock' Johnson merged with yoda. Doing animation with it is pretty slow. On my (Daniel's) computer, it took 50 seconds without the sampling and 85 with the sampling.# Computer-Graphics-Final
