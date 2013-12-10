Title: Using CGEngine's FBOs 
Date: 2013-12-09 
Tags: programmation, opengl, FBO, glsl 
Summary: Using FBO's can sometimes be quite tricky. I've written a class making it easier to use. It can still however, when not used properly be a pain to use. The goal of this document is to show the overall steps required to using my FBO system. 

Create a FBO:

    ::cpp
        cg::FBO fbo = cg::FBO(windowSize.x, windowSize.y, cg::FBO::COLOR);

Link its internal texture to rendering shader (the one used to render on a
visible fullscreen quad for instance).

    ::cpp
        cg::Shader shader;
        shader.loadVertexShaderFromFile("../src/fullscreen_quad.vert");
        shader.loadGeometryShaderFromFile("../src/fullscreen_quad.geom");
        shader.loadFragmentShaderFromFile("../src/fullscreen_quad.frag");
        // Activate shader
        shader();
        // Link texture
        shader.setTexture("Texture", fbo.getColorTextureId());

Do the linking texture step only *once* before the rendering. There is no point in linking it every time! Anyway that wouldn't work properly if you were to do that.

Now you can activate the FBO in the render loop and render on it:

    ::cpp
        // Activate render to FBO
        fbo.renderToFBO();
        // Clear the FBO (equivalent to glClear(...))
        fbo.clear();

        /**
         *  drawing...
         *  We fill the array and then activate the Vertex Attrib 0
         **/
        shader();
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, vertices);
        glEnableVertexAttribArray(0);
        // Draw triangles
        glDrawArrays(GL_TRIANGLES, 0, 3);
        // Disable Vertex array when not needed anymore
        glDisableVertexAttribArray(0);


The rendering part on the FBO is finished. After this step, you should have a triangle drawn on the FBO's texture.
All that's left to do is display the texture to check whether everything is fine.
This can be done using a fullscreen quad. The code below uses a geometric
shader to generate the quad, and a fragment shader to texture it with the
previously generated texture.
Note that we don't need to bind the FBO's texture to the shader since this has
been done ***before*** the rendering loop.


        cg::FBO::renderToScreen();
        shader();

        /**
         * Issue a dummy VAO call to send one point to the graphics card.
         * It will then be able to generate a fullscreen quad
         * Since we've bound the FBO's render texture to the uniform Texture of
         * the shader, we only need a sampler2D Texture; in the fragment shader
         * to make it work!
         **/
        glBindVertexArray( vao );
        glDrawArrays( GL_POINTS, 0, 1 );
        // Don't forget to clear the vertex array, or you might run into some
        ugly surprises, like segfaults on glDrawArray calls for instance.
        glBindVertexArray(0);


