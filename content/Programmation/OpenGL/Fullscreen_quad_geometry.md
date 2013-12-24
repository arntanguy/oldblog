Title: Fullscreen quad with geometry shaders 
Date: 2013-12-13 
Tags: programmation, opengl, glsl, shaders, geometry shader
Summary: Explains how to create a fullscreen quad using geometry shaders 
disqus_identifier: geenux-fullscreenquad-shader

One question that we see pop up from time to time on various OpenGL forums
concerns the creation of fullscreen quads. Most of the solutions given are
sending two fullscreen triangles to a vertex shader. While this approach works,
it isn't optimal for graphics card using geometry shaders. 
And guess what? It is much easier to do it using geometry shaders!

Here are the shaders you'll need:

An empty vertex shader

    ::glsl
        #version 330 core
        void main() {}

A geometry shader emitting a fullscreen quad

    ::glsl
        #version 330 core

        /**
         * Emits a fullscreen quad
         * Make sure that the input is an empty VAO emitting a dummy GL_POINT
         */
        layout(points) in;
        layout(triangle_strip, max_vertices = 4) out;

        out vec2 UV;

        void main()
        {
            gl_Position = vec4( 1.0, 1.0, 0.5, 1.0 );
            UV = vec2( 1.0, 0.0 );
            EmitVertex();

            gl_Position = vec4(-1.0, 1.0, 0.5, 1.0 );
            UV = vec2( 0.0, 0.0 );
            EmitVertex();

            gl_Position = vec4( 1.0,-1.0, 0.5, 1.0 );
            UV = vec2( 1.0, 1.0 );
            EmitVertex();

            gl_Position = vec4(-1.0,-1.0, 0.5, 1.0 );
            UV = vec2( 0.0, 1.0 );
            EmitVertex();

            EndPrimitive();
        }

And a dummy fragment shader

    ::glsl
        #version 330 core

        out vec4 out_Color;
        in vec2 UV;

        uniform sampler2D Texture; 

        void main(void)
        {
            out_Color = texture2D(Texture,UV);
        }

Now, to use it, all you need to do is bind all three shaders, and emmit an
empty VAO.

    ::cpp
        /**
         * Issue a dummy VAO call to send one point to the graphics card.
         * It will then be able to generate a fullscreen quad
         **/
        glBindVertexArray( vao );
        glDrawArrays( GL_POINTS, 0, 1 );
        // Don't forget to clear the vertex array, or you might run into some
        // ugly surprises, like segfaults on glDrawArray calls for instance.
        glBindVertexArray(0); 

If this doesn't work, make sure that:

* Your graphics card supports geometry shaders
* The shaders are correctly bound
* The geometry emitted is **a point** (empty VAO shown above)


That's it, you can now create fullscreen quads!
An exemple of post-processsing with an FBO can be found
[here]({filename}/Programmation/OpenGL/FBO_Workflow.md)
