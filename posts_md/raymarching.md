Ray Marching: Easy 3D and Perfect Spheres
Post
8/11/23
If you've done any 3D modeling before you may have heard that "You can't make a perfect sphere" because every 3d object is just a bunch of triangles. But what if there is another way of rendering a 3d scene? Well there is: Ray marching.

In ray marching. instead of a bunch of triangles all you need to define a scene is a function that takes a point in space and returns the distance to the scene from that point. Although this may seem very limiting, it allows you to do really neat things like fractals, twists & bends, and infinitely repeating objects at almost no extra computational cost.

Note: This article uses lots of Shadertoy embeds, you can view the source code for any of these by hovering over them and clicking on the name. 

Throughout this series, we will be working up to making animations like this one:

  <iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/ctXfzB?gui=true&t=10&paused=false&muted=true" allowfullscreen></iframe>

But before I talk about how they work, we have to take a step back:
# How lighting works in the real world (simplified)

In the real world, lights emit an unimaginable amount of photons (A 50 watt light bulb emits about 3,730,000,000,000,000 every 60th of a second) which will each "pick up" colors they hit along the way. We can only see because some of these photons just happen to randomly hit our eye.

![[reallighting.png]]

Using a computer, we obviously can't simulate 3,730,000,000,000,000 photons each going on their own paths for every frame. So how else should we simulate real lighting?
# How 3D renders work

Instead of casting rays (shooting photons) from a light you can just start at the eye and work backwards towards the scene. It can achieve almost the same effect in the end with only having to cast as many rays as the amount of pixels on the screen. 

![[raymarchingfakelighting.png]]

For a 1080p screen this would be about 2 million rays which seems like a lot, but it is only .000000000535% of the 3,730,000,000,000,000 rays you would have to calculate for a single lightbulb to get truly real lighting.

This method of casting rays to render a scene can be used in many different ways such as:
- Ray casting - Simply cast a few rays (usually only along a single axis) and see how far they go. This is how games like Wolfenstein 3d were made. 
- Ray tracing - Cast rays at the scene, bounce them around if there's a mirror, split them if there's a blur, and bend them if there's a refraction. Rays work by checking for intersections with each analytically defined object.
- Ray marching - Very similar to ray tracing, but it casts rays by "marching" towards a scene defined by a single signed distance function (I'll explain these soon).

![[rayexamples.png]]

It is worth noting that although these methods of 3D rendering give nice graphics, the main way of 3D rendering is called rasterization which works by checking what pixels different triangles take up on a screen. 
# How does a ray marcher work?

From now on I will assume some basic knowledge of GLSL (a programing language used for shaders), which I will be using to render our animation, but you can probably sort of understand it if you don't know it.

To start we will make this super simple animation, which just casts a ray for each pixel and determines a shade of gray based on how far it goes. We'll create a simple scene with sphere moving over a plane.

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/ctjcWm?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>

To do this, we will need a ray casting function which just returns the distance a ray traveled before hitting the scene, and a function that returns the distance to the scene (we'll call this getDistanceToScene)

Before we get to how the getDistanceToScene function works, lets make the rayMarch function.

A ray marcher works by starting at a point, getting the distance to the scene, moving ("marching") along the ray by that distance, then repeating the cycle until the distance to the scene is 0 (or something like .01 to avoid it sampling forever when it gets close to an edge but doesn't hit it).

![[raymarch - Copy.png]]

It can be implemented using:

```glsl
#define MAX_MARCH_STEPS 200
#define MAX_MARCH_DIST 500.
#define MARCH_NEAR_DIST .01

float rayMarch(vec3 rayOrigin, vec3 rayDirection)
{
    float distanceFromOrigin = 0.;

    for (int i=0; i < MAX_MARCH_STEPS && distanceFromOrigin < MAX_MARCH_DIST; i++)
    {
	    // calculate the next point to sample from
	    vec3 point = rayOrigin + rayDirection * distanceFromOrigin;

        float d = getDistanceToScene(point);
        distanceFromOrigin += d;
        
        // hit something 
        if (d <= MARCH_NEAR_DIST)
            return distanceFromOrigin;
    }

	// if it didn't hit anything
    return MAX_MARCH_DIST;
}
```

We can render our scene using:

```
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // normalize pixel cordinates
    vec2 uv=(fragCoord.xy-.5*iResolution.xy)/iResolution.y;

    vec3 camera = vec3(0, 2, 0);
    vec3 rayDirection = normalize(vec3(uv.x,uv.y,1));
    
    float d = rayMarch(camera, rayDirection);
    
    fragColor = vec4(vec3(d/MAX_MARCH_DIST),1.0);
}
```

So all we need to do now is make our function that returns the distance to the scene.
# SDFs (signed distance functions)

Signed distance functions do just about what the name says they do. They are functions that return the distance to something, being positive if its outside, 0 if it's on the surface, and negative if it's inside. This is explained better by this visual made by Inigo Quilez:

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/3ltSW2?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

This represents the signed distance function for a 2D circle with blue showing negative values, and orange showing positive values.

To start, lets just make the SDF for the ground.

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/dlXBWj?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

This is probably the most simple SDF to make as it is just the distance of the sampling point's y value from the y value of the plane. This can simply be represented as `abs(p.y - y)` where p is the sample point and y is the location of the plane.

```
float planeSDF(vec3 p, float y)
{
    return abs(p.y - y);
}
```

We can now build the start of our getDistanceToScene function:

```
float getDistanceToScene(vec3 p)
{
    float ground = planeSDF(p, -1.);
        
    return ground;
}
```

To make an SDF for a sphere, all we would need is to get the distance from the center of the sphere to the sample point, and subtract the radius. This sounds a bit weird at first, but it makes sense if you think about it.

```
float sphereSDF(vec3 p, float radius, vec3 position)
{
    return length(p-position) - radius;
    // same as distance(p,position), but using this instead becomes important later
}

float getDistanceToScene(vec3 p)
{
    float sphere = sphereSDF(p, 2., vec3(-3,1,8));
        
    return sphere;
}
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/dlXfWj?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

That's cool, but how do we combine the sphere and the plane?
# Combine SDFs

If you have the result of two distance functions, how do you tell which is closer? You just take the smaller value! Remember, all our raymarcher needs (for now) is the closest distance to the scene. It doesn't care about how far the other parts are. 

![[unionsdf.png]]

We can implement this with the very short unionSDF function:

```
float unionSDF(float a, float b)
{
    return min(a,b);
}
```

Here is the completed code for our getDistanceToScene function with our fancy new unionSDF:

```
float sphereSDF(vec3 p, float radius, vec3 position)
{
    return length(p-position) - radius;
}

float planeSDF(vec3 p, float y)
{
    return abs(p.y - y);
}

float unionSDF(float a, float b)
{
    return min(a,b);
}

float getDistanceToScene(vec3 p)
{
    float ground = planeSDF(p, -1.);
    float sphere = sphereSDF(p, 2., vec3(-3,1,8));
    
    float scene = unionSDF(ground, sphere);
    
    return scene;
}
```

We can also add a little animation to our sphere by making it revolve in a circle:

```
    float sphere = sphereSDF(p, 2., vec3(
		1. * sin(iTime), 
	    1, 
	    11. + 3. * cos(iTime)
	));
```

And that's it! Now you have everything you need to make a raymarcher. In the rest of the articles, we will just be adding to this, with lighting, colors, and fractals, but all of those are just additions, and you already have a working ray marcher.

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/ctjcWm?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>

Here is a great list of many SDFs and functions that can be used with them: https://iquilezles.org/articles/distfunctions/
# Colors

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/cllfDs?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

Now, we will add color to our renderer, which is a lot easier to do than it sounds because of how the rest of the raymarcher was set up. We can create a struct for objects and add more values, such as color:

```
struct closestObject {
    float d; // the distance to the object
    vec3 col;
};
```

And change our definition of objects by adding a color:

```
closestObject ground = closestObject(
    planeSDF(p, -1.), 
    vec3(0,1,1) // cyan
);
```

Now that we're working with objects and not just distances, we'll have to update our functions. We can change our getDistanceToScene function to getClosestObject, and our unionSDF function to unionObject:

```
closestObject unionObject(closestObject a, closestObject b)
{
    if (a.d < b.d) // min
        return a;
    return b;
}

closestObject getClosestObject(vec3 p)
{
    closestObject ground = closestObject(
	    planeSDF(p, -1.), 
	    vec3(0,1,1) // cyan
	);
    closestObject sphere = closestObject(
	    sphereSDF(p, 2., vec3(-3.,1,9.)),
	    vec3(1,0,0) // red
	);

    closestObject scene = unionObject(ground, sphere);
    
    return scene;
}
```

All we need to change in our main function is a few lines that calculate where the ray hit and one that gets the points color. We can also multiply our color by the distance we had earlier for a fog effect:

```
	...
    float d = rayMarch(camera, rayDirection);
    vec3 hitP = camera+rayDirection*d;
    
    vec3 col = getClosestObject(hitP).col;
    
    fragColor = vec4(col*vec3(1.-d/MAX_MARCH_DIST),1.0); // fog
    ...
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/cllfDs?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>
# Lighting

Lighting is the most important part of any 3D renderer. For now we will just implement some basic lighting without any shadows.

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/dt2Bzz?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>
## Lighting in the real world

Lighting from a global light source works similarly to how temperature changes by latitude on the earth. The sharper of an angle a surface is to the sun, the less radiation rays will be hitting the ground, making it colder.

![[realworldlighting.png]]

When thinking about lighting, the only difference is that the light is emitting photons which will change brightness (amount of photons that end up bouncing to your eye) instead of radiation changing temperature.
## Fake lighting

Instead of casting a bunch of rays from a light simulating photons, we can use a little trick to quickly and easily calculate how bright any point should be. 

All that's really changing in our example of the earth and the sun is the angle that the radiation ray hits the surface. If that angle is 90 or greater, then there are no rays hitting the surface, but if it's any less there will at least be some.

Here's where the trick comes in: this value can just be calculated with the dot product of the normalized light ray and the normal of the surface. That's it!
## Implementation

Before we go on, lets increase how far we can see to better demonstrate the light hitting the ground.

```
#define MAX_MARCH_STEPS 200
#define MAX_MARCH_DIST 250.
#define MARCH_NEAR_DIST .01
```

We can easily write our getLighting function using the method described earlier:

```
vec3 getLighting(vec3 p)
{
    vec3 col = getClosestObject(p).col;

    vec3 lightRay = normalize(vec3(1,1,-.5)); // try playing around with this vector
    
    float lighting = clamp(dot(lightRay, getNormal(p)), 0., 1.);   
    return col*lighting;
}
```

Easy right? Nope! I still haven't gone over how to get the normal of a surface or made getNormal.
## Normals

The way of getting normals in our SDF defined scene is a bit confusing, but it is really nice because:
- It works with any point in space, just like our getLighting function.
- It works for any scene and doesn't need any complicated math like it would with ray tracing.

It works by getting the distance to the scene from some offset points, subtracting the distance to the scene from the original point from each, and putting these values together into a vector.

![[raymarchingnormals.png]]

This can be implemented using:

```
vec3 getNormal(vec3 p)
{
    vec2 e = vec2(.01,0); // just used to make translation vectors like vec3(.01,0,0)
     
    vec3 n1 = vec3(
        getClosestObject(p+e.xyy).d,
        getClosestObject(p+e.yxy).d,
        getClosestObject(p+e.yyx).d
    );
         
    return normalize(n1-getClosestObject(p).d);
}
```

But we can get some more precision by also sampling points in the opposite direction:

```
// extra precision
vec3 getNormal(vec3 p)
{
    vec2 e = vec2(.01,0);
     
    vec3 n1 = vec3(
        getClosestObject(p+e.xyy).d,
        getClosestObject(p+e.yxy).d,
        getClosestObject(p+e.yyx).d
    );
    vec3 n2=vec3(
        getClosestObject(p-e.xyy).d,
        getClosestObject(p-e.yxy).d,
        getClosestObject(p-e.yyx).d
    );
         
    return normalize(n1-n2);
}
```

And now our getLighting function should work!
## Putting it all together

In our main function we have to replace our old method of just getting the color directly from the scene with our new getLighting function.

```
    vec3 col = getClosestObject(hitP).col; // OLD
	vec3 col = getLighting(hitP);          // NEW
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/DtBfzW?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

If we want to use a point light instead of the global lighting, all we need to change is how we calculate our light ray:

```
    vec3 lightPos = vec3(0, 3, 5. + sin(iTime) * 5.);
    vec3 lightRay = normalize(lightPos-p);
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/dt2Bzz?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>

One of the nice things about building something from scratch is that you have complete control over everything. For example if I wanted to give the scene some cartoony lighting all I'd need to do is use a ceil function with the lighting value:

```
	lighting = ceil(lighting*5.)/5.;
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/DtSfzW?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>

Now that our scene looks partly presentable, we can start talking about the cool parts of raymarching. 😎
# Transformations

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/mt2fzW?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>
Left - translation, center - scale, right - rotation

Transformation work a bit different than you may think. Instead of moving the object, you move the point being sampled in your SDF.

This idea of moving space is already demonstrated in our sphereSDF function:

```
float sphereSDF(vec3 p, float radius, vec3 position)
{
    return length(p-position) - radius;
}
```

If we take away the `-position` and move it to when we call the function, our SDF can assume the center should be at the origin (0, 0, 0), which makes things much easier for our SDF. 

```
float sphereSDF(vec3 p, float radius, vec3 position)
{
    return length(p) - radius;
}

sphere = sphereSDF(p - position, 2.) // moved the translation
```

Our SDFs can be rewritten to work around the origin, making them simpler and avoiding repetitive code:

```
// simpler SDFs 
float sphereSDF(vec3 p, float radius)
{
    return length(p) - radius;
}

float planeSDF(vec3 p)
{
    return abs(p.y);
}
```

And we can define translations for our objects in the getClosestObject function:

```
closestObject getClosestObject(vec3 p)
{
    closestObject ground = closestObject(
        planeSDF(p - vec3(0,-1,0)), // move to (0, -1, 0)
        vec3(0,1,1)); // color

	closestObject sphere = closestObject(
        sphereSDF(
	        p - vec3(sin(iTime)*7., 1, 15),  // slide between (-7, 1, 15) and (7, 1, 15)
	        2.),      // radius
        vec3(1,0,0)); // color

    closestObject scene = unionObject(ground, sphere);

    return scene;
}
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/Dt2BR3?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>

Although this does the exact same thing as having our positions in the arguments, it's better because now we don't have to put those in every SDF. This also allows us to make other transformations that work on any object. 

To scale something we can use:

```
sphere = mySDF(p / scale, 2.) * scale
```

We can also do rotation, but it is a lot harder and I'm not going to go into how it works. I'll be using the standard function which can be found on Wikipedia https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions

Here's our rotation function that takes a vec3 of pitch, roll, and yaw as Euler angles (degrees):

```
vec3 rotate(vec3 p, vec3 rot)
{
    rot = mod(rot, 360.)/(180./3.1415); // degrees to radians
    
    float ca = cos(rot.x); float sa = sin(rot.x);
    float cb = cos(rot.y); float sb = sin(rot.y);
    float cy = cos(rot.z); float sy = sin(rot.z);
    
    return p*mat3(
        cb*cy         , cb*sy         , -sb,
        sa*sb*cy-ca*sy, sa*sb*sy+ca*cy, sa*cb,
        ca*sb*cy+sa*sy, ca*sb*sy-sa*cy, ca*cb
    );
}
```
## Other functions?

So now we know what happens when we use basic functions like subtraction/division, but what happens when you use more complicated functions? Lets try modulo-ing our point:

```
closestObject getClosestObject(vec3 p)
{       
    closestObject spheres = closestObject(
        sphereSDF(
	        mod(p, vec3(4)) - vec3(2),
	        1.),
        vec3(1,0,0)
    );

    return sphere;
}
```

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/mlSBzV?gui=true&t=10&paused=false&muted=false" allowfullscreen></iframe>

Wow! All we added is one extra cheap operation into our function and now there's an infinite amount of spheres! What happened? 

It's simple really: When we took the modulo of the point and 4, it made the point repeat every 4 units over and over. I also had to subtract 2 to make sure the result of the modulo includes negatives. 

![[moduloshader.png]]
Made from https://www.shadertoy.com/view/dtSBRc

add note about non symetric boxes with link to iq article

Next sections:
- more lighting:
	- soft shadows
	- ambient occlusion
- smooth union, bend, twist, etc.
- fractals
- maybe a little note about my bending light thingy
# Resources

- https://www.youtube.com/watch?v=BNZtUB7yhX4 A great introduction to ray marching.
- https://www.youtube.com/@InigoQuilez/videos More of Inigo Quilez's cool stuff.
