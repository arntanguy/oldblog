Title: Loading a Blender scene in Physijs and Three.js
Date: 2013-12-11
Tags: programmation, webgl, blender, js, javascript
Summary: During an event called "Nuit de l'info" where teams from all over France compete on accomplishing a fair number of programming challenges. Some good came out of it, as it led me to write a way to import a full Blender scene in Three.js, including some Physijs parameters.
disqus_identifier: geenux-loading-blender-threejs


# La Nuit de l'Info
It is quite interesting to realize the context in which these tools have been
written. It was all done during an event called "[La Nuit de l'Info](http://www.nuitdelinfo.com/)". It is a
national event held every year in France in which engineers students are competing from sunset to dawn over
a number of challenges. These challenges spawn an impressive number of
technologies, ranging from digging up some very old protocols to using some
mainstream technologies, passing through Django, Javascript, Android, WebGL...
Well you get the idea, that's a lot of possibilites for just a night!

Our team ".pyVerts" won 3 challenges, sadly none of them concerns this article
on WebGL. Nonetheless, what will be presented here might not have been material
for winning challenges, but certainly did a lot more good than most projects out there: it led to some pretty useful code that could possibly be used by anyone!


# Three.js, Physijs and Blender: How to fit them together?

* [three.js](Three.js) is a really good 3D WebGL engine. It contains most of what
you need to create a game: shader's support, materials, texture, camera,
raycasting, and much more.
* [Physijs](http://chandlerprall.github.io/Physijs/) is a physics engine plugin for Three.js. It is based on the quite famous Bullet Physics engine.
* [Blender](www.blender.org) is an opensource modelling tool.

I will present the rest of this article in the same order as the ideas I had
for the night, so that you can grasp the thought process that led me to write
    additional tools for Three.js.



# First step: Loading a blender scene in Three.js

## Install the JSON export plugin for Blender

Hopefully, loading a blender scene in Three.js engine is pretty easy. You just
need to use the JSON exporter for blender along with the JSONLoader from
Three.js. I will show you a version of that with the addition of the integration of Physijs.

Here is how to install my version of the blender export plugin:

** Update: ** Thanks to some user submissions, the plugin and loading code has been improved. See the updates section at the end of this article to get the newest files. The installation method is the same.

* Download [the modified exporter for blender 2.69]({filename}/download/io_mesh_threejs_physijs.tar.gz)
* Untar it in ~/.config/blender/2.69/scripts/addons

Then go to Blender "User Preferences"->"Addons", and look for "three" in the
research bar. Activate it.


## What's new

![Exporter modification]({filename}/images/programmation/blender/blender_threejs.png)

As you can see, in the Mesh panel, there is an additionnal **PHYSICS section**.
To use it, just select (in object mode) the mesh that you're interested in, and
set its properties:

* Shape: the physics representation of the object (box, sphere, convex hull...).
* Mass: self-explanatory, set it to 0 if you want a static object

## Export scene

Select all objects within the scene (including cameras and lights), and click
on the menu "File->Export->Threejs"

* Make sure that "scene" and "camera" are checked!

That's it, you should now have a JSON scene file that you can use with three.js


# Load scene

I wrote a modified version of the JSON Loader reading the physics parameters
from Blender.

First, [download this class](https://raw.github.com/geenux/.jSuisUn.pyVert/master/webgl/libs/PhysicsSceneLoader.js).
Now to load a scene, you can look at [this example loader](https://raw.github.com/geenux/.jSuisUn.pyVert/master/webgl/tests/PhysicsLoader/physics_load_scene.html)

The interesting part is

    ::js
	    var loader = new PhysicsSceneLoader();
	    loader.callbackProgress = callbackProgress;
	    loader.load( "scene.js", callbackFinished );

There is two callback functions.
You can use this one to show a progress bar

    ::js
        var callbackProgress = function( progress, result ) { }

And this one to handle what to do when loading is finished

    ::js
        var loaded = {}
	    var callbackFinished = function( result ) {
            loaded = result
            // Add gravity to the scene
		    loaded.scene.setGravity(new THREE.Vector3( 0, -9.8, 0 ));
            // Start the physics simulation
		    scene.addEventListener(
		    	'update',
		    	function() {
		    		scene.simulate( undefined, 1 );
		    	}
		    );
        }

The variable *loaded* now contains all the scene.
You can use *loaded.scene* to access the scene object. For instace, if you want
to render it

    ::js
        renderer.render(loaded.scene, loaded.camera)

You'll have access to all objects loaded through *loaded.objects*.

Well you get the gist of it!


# How to improve the export script

The export script is far from complete as far as physics is concerned. So here is the gist of how to improve
it.

If you lack properties, you can easily integrate them by following the following steps:

**In export_threejs.py**:

* Modify the *TEMPLATE_OBJECT* variable
* Modify the *object_string* in generate_object

**In __init__.py**:

Define your element at the top of the file Something like

    ::python
        bpy.types.Object.THREE_physicsShape = bpy.props.EnumProperty(
            items = [('BoxMesh', 'BoxMesh', 'Cube-like mesh'),
                    ('PlaneMesh', 'PlaneMesh', 'Plane'),
                    ('SphereMesh', 'SphereMesh', 'Sphere'),
                    ('CylinderMesh', 'CylinderMesh', 'Cylinder'),
                    ('ConeMesh', 'ConeMesh', 'Cone'),
                    ('CapsuleMesh', 'CapsuleMesh', 'Capsule'),
                    ('ConvexMesh', 'ConvexMesh', 'Convex hull of object'),
                    ('ConcaveMesh', 'ConcaveMesh', 'Concave'),
                    ('HeightfieldMesh', 'HeightfieldMesh', 'matches a regular grid of height values given in the z-coordinatesHeightfield')],
            name = "Mesh Type")

Add it to the *OBJECT_PT_physics* class

**In the engine**, add it to **PhysicsLoader.js**:
Look for where the Physijs.Mesh are defined, and do the proper changes, that's it, you're all set!


# Troubleshoot

*My physics bounding volume seems way bigger than the real object*

There my friend, you probably just encountered one of the most common problems with blender. By default, exporting doesn't apply scale to your mesh, quite stupid ain't it.
Hopefully it is very easy to solve: select your model in Blender, and then hit Ctrl-A -> Apply Rotation and Scale.
That's it, you're done ;)

# Updates

Kevin Bikhazi improved upon my plugin. You can find [the modified exporter for blender 2.69 here]({filename}/download/io_mesh_threejs_physijs_update1.tar.gz)

Here is the changelog

* Adds friction and restitution parameters under an object's material tab in Blender. These parameters are very important as they affect how the model interacts with the physics world.
* The Blender add-on has been modified to handle the new material parameters.  Currently the mods only work with standard materials and not with normal mapped materials.  It should be pretty easy to get it to work with normal maps, that might come soon
* PhysicsSceneLoader.js modified to use the new friction and restitution parameters.  
        
To install it, just untar, and copy the files to the proper location as specified in the article.

# Conclusion

It's probably far from the best way of loading physics within three.js: it
was written during a crazy night of coding! Yet, I hope this helps to give you
ideas of how to automatically load geometry and physics within your webgl
application.
