Raymarching: Easy 3D and Perfect Spheres
Post
8/11/23

If you've done any 3D modeling before you may have heard that "You can't make a perfect sphere" because every model is a mesh made up of verticies and triangles, and not curves. But what if there is another way of defining and rendering objects? Well there is: Raymarching and signed distance functions! (It's more interesting than it sounds)

Raymarching uses a very simple and clever method to render 3D scenes using mathimatical definitions of objects instead of meshes. It is very easy to implement and can be used to render things like perfect spheres, fractals, and infinetly repeating spaces.

## How it works

<table>
<tr>
    <th>Defintions</th>
<tr>
<tr>
    <td>Ray - a line going forever through space that intersects objects as it goes. It stores info about where it hit objects and what objects it hit. For raymarching this ray can stop after its first hit.</td>
</tr>
<tr>
    <td><img src="{{ url_for('static', filename='raymarching/ray_definition.png') }}", alt="Image demenstrating a ray"></td>
</tr>
</table>


Like most 3D renders, raymarching works by casting rays at a scene and determining where and what they hit. The main difference is how it finds where the rays hit.

Here is how it casts rays:

1. Start at the ray origin.

2. Get the distance to the scene and info about the closest object
3. If the distance is 0, then the ray has hit something! Return the total distance traveled and the closest object
4. Move along the ray by the distance to the scene
5. Repeat from step 2 stopping if a maximum amount of steps is reached

_

- implementation (shader overview?)
- SDFs
- union, intersection, difference
- colors
- transforms
