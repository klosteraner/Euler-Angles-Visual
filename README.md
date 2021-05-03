# Euler angle visualization

The app aims at visualizing Euler angles, or more correctly speaking Tait-Bryan angles.
While I found the general principle of Euler / Tait-Bryan angles can be understood 
from theory, I found it hard to visualize the concrete definitions.

This app helped me getting a better intuition about the world axes & camera axes definitions
as well as how the rotation order influences the final rotation.

Currently Yaw-Pitch-Roll and OPK (Pix4D) can be visualized.

## What for ?

I am often confronted with rotations via numbers, euler angle parametrizations.
The principles of euler angles are straight-forward and are explained on e.g.
[wikipedia](https://en.wikipedia.org/wiki/Euler_angles).

Still after a few years working with them I struggle to build an intuition from numbers 
and convention definition only. This interface allows to **input angles** in the desired
convention and get quick feedback & intuition how they **relate to a visual camera pose**.

Moreover the interface gives slider to get a feeling **how little differences in the angles
would affect the camera pose**. E.g. one can easily discover how and why Omega and Kappa act 
on the same axis if Phi=90°.

Other features I have in mind and may implement in the future:
- Make switch between different systems available in UI
- Split view to compare different combinations

## Coordinate systems

In this project we deal with 3 coordinate systems: The mayavi scene system, the world system
& camera system.

The app ties the world system to the mayavi scene system up to variations on axis names and sign
as multiple world systems may be possible (even though YPR and Pix4D OPK use the same).

The camera system varies w.r.t. to the the other two systems and is indicated as camera outline 
representing camera center and image plane.

## Mayavi

A secondary aim of this project was to become familiar with mayavi and prepare a blue print 
that can be used for future projects. Indeed the project helped getting familiar with the
different levels of mayavi. While the GUI and scripting interface helped me to see where to go,
this project actually shows how to create an interactive 3D scene with mayavi.

Retrospectively looking, Mayavi is a great tool that complements other available 
3D visualization tools such as unity or blender. 
While these tools allow to create nearly every visualization imaginable, game play 
and much more, this power comes at the cost of knowing or learning about complex interfaces.
Mayavi on the other side lets you concentrate on the data you want to visualize first, 
and then only on demand allows you to dig deeper into visual aspects.

With this project I feel like scratching these boarders: The angle GUI to manipulate the 
3D scene was implemented super easy & intuitively using mayavi's underlying traits. 
On this particular aspect mmayavi showed its full strength.

The camera, world & coordinate system meshes as objects that are not representing the data, 
but are rather used as tools to visualize them were implemented using mayavis mesh api.
While the mesh api allowed easy implementation, this implementation was a layer 
that needed to be added on top of mayavi and before the actual application. This was a 
very acceptable overhead to customize mayavi to my needs.

For this project customization stopped at the wish to including image data. While I am aware 
that it would be possible via VTK, it requires an understanding of a different and more complex api.
For this project I stopped at that point and skipped this part.

Another interesting feature would be to embed the program on a webpage. The Mayavi documentation
does not talk about this. I assume a realization of this feature would require another dependency
and some substantial integration work. I will also leave this to a future me.

TODOs:
- clear instructions for install / execution (currently it works on my machine)
- Indicate camera coordinate system
