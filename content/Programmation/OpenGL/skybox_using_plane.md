Title: Creating a Skybox from a fullscreen quad! 
Date: 2014-01-21 
Tags: programmation, opengl, glsl 
Summary: This post shows you how to create a Skybox by generating a plane in a geometry shader and using an inverse projection trick to make it look like a cube skybox :) 
disqus_identifier: geenux-plane_skybox

Creating a skybox is commonly done by either rendering an infite cube or
sphere. Both methods are working nicely, but require to set up VBOs, transfer
data to the GPU... Granted, that's far from the costlier thing you can do, but
then every little bit counts ;)

In this article, I will show you how to create a skybox by creating a
fullscreen quad in a geometry shader and applying an inverse projection to get
the eye direction as it would be if we were to render a cube. 

Why, will you ask me? Two reasons, it's fun and it's convenient!

First, let me thank "msell" for [the idea](http://gamedev.stackexchange.com/questions/60313/skyboxes-using-glsl-version-330).

![Skybox using a plane]({filename}/images/programmation/opengl/skybox_plane.png)

The result is quite interesting:

- Notice how the center is of perfect resolution? That's because no distortion
  is applied there, so whatever your environment map resolution was will be
  preserved.
- Notice how the sides are "stretched"? That's because the texture is virtally
  projected on a cube, and thus appears stretched towards us. This gives a
  really deep impression of depth, however it comes at the cost of a little bit
  of motion blur. This side effect could be very useful for designing skyboxes
  for racing games!
  For other types of games, by tweaking the matrices inverted, this effect
  could be lessened.


## Geometry shader
The role of this geometry shader is to emit a fullscreen quad, and send the
view vectors corresponding to each of the corners. These view vectors will be
interpolated when being passed to the fragment shader, resulting in view
vectors for every part of the skybox, that can be used, for instance to fetch
texture information from a samplerCube.

    ::glsl
        #version 330 core
        
        uniform mat4 uProjectionMatrix;
        uniform mat4 uWorldToCameraMatrix;
        
        smooth out vec3 eyeDirection;
        
        layout(points) in;
        layout(triangle_strip, max_vertices = 4) out;
        
        void main()
        {
            vec4 corner1 = vec4( 1.0, 1.0, 0., 1. );
            vec4 corner2 = vec4(-1.0, 1.0, 0., 1. );
            vec4 corner3 = vec4( 1.0,-1.0, 0., 1. );
            vec4 corner4 = vec4(-1.0,-1.0, 0., 1. );
            // Inverse matrix is costly, should be precalculated
            // This is effectively a non-issue there as it is only computed four times
            // and would probably be calculated slower on the CPU (unless the view is
            // fixed, then it's obviously faster to compute it once and for all).
            mat4 inverseProjection = inverse(uProjectionMatrix);
            mat3 inverseModelview = transpose(mat3(uWorldToCameraMatrix));
        
            gl_Position = corner1;
            eyeDirection = -inverseModelview * (inverseProjection * corner1).xyz;
            EmitVertex();
        
            gl_Position = corner2;
            eyeDirection = -inverseModelview * (inverseProjection * corner2).xyz;
            EmitVertex();
        
            gl_Position = corner3;
            eyeDirection = -inverseModelview * (inverseProjection * corner3).xyz;
            EmitVertex();
        
            gl_Position = corner4;
            eyeDirection = -inverseModelview * (inverseProjection * corner4).xyz;
            EmitVertex();
        
            EndPrimitive();
        }

## Fragment shader
Nothing fancy here, we only need to use the eyeDirection vector interpolated
from the geometry shader to fetch the texture in a samplerCube.

    ::glsl
        #version 330
        
        uniform samplerCube cubemap;
        
        smooth in vec3 eyeDirection;
        
        out vec4 fragmentColor;
        
        void main() {
            fragmentColor = texture(cubemap, eyeDirection);
        }

## Usage
When rendering it, you need to disable depth testing, so that the fullscreen
quad always appear behind every other object.
Then just generate an empty VAO to activate it:

    ::cpp
        glBindVertexArray( vao_skybox );
        glDrawArrays( GL_POINTS, 0, 1 );
        glBindVertexArray(0);

