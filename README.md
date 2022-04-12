# TrainTracts

#### _Import .TCK Files to Blender with Ease!_

![](https://www.4dbrix.com/products/train/rail-yard/rail-yard-left-4-tracks.png)

## About the plugin:
TrainTracts is a Blender plugin that allows you to import neuroimaging .TCK (tractography) files directly into Blender for 3D rendering. Installing the plugin is easy and allows for prettier neuroscience visualizations!

https://user-images.githubusercontent.com/22922192/163030494-4f7bee84-7e50-4e69-9f92-a0212b3a61c9.mp4

## Installation:

1. Download the **TrainTracts.zip** file and **DO NOT** unzip/extract it!
2. Go to **Edit > Preferences > Add-ons** and click on **Install...** in the upper right corner.
3. Navigate to the location of **TrainTracts.zip** and select it, then click **Install Add-on**.
4. Search for the TrainTracts plugin and check the box next to **Import Export: TrainTracts** to activate the plugin.
5. You're ready to use TrainTracts! You can find the .tck import option in **File > Import > Tractography (.tck)**!

https://user-images.githubusercontent.com/22922192/163031983-785964bc-fdd5-40ba-b786-8fb9dac077fd.mp4

## Importing a .TCK File to Blender:

1. Have a .TCK file at the ready!
2. Navigate to **File > Import > Tractography (.tck)** in Blender, and click the **Tractography (.tck)** option.
3. Navigate to your .TCK file of choice and select it.
4. If the file is too big for your computer (generally >100,000 tracts for a laptop) you can set the **Decimate Factor** option on the right sidebar to an integer. If you set **Decimate Factor** to equal **2** then half of the tracts will be imported. An easy way to think about it is: **Number of tracts imported = Number of tracts / Decimate Factor**
5. Click the **Tractography (.tck)** option in the bottom right to import!
6. You're all set! 

**Bonus tip:** select the tracts and right click, then select **Set Origin > Origin to Geometry**. This will move the origin of the tracts to the object's "center of mass". Simply put, this means that if you rotate, scale, or transform the tracts in some other way, they will be transformed nicely around their center and not some point off in space.

https://user-images.githubusercontent.com/22922192/163030076-b3c3e28d-00c5-4c06-b401-7994650c59b6.mp4

## Adding Volume to Tracts (Mesh to Curve to Mesh):

1. Select the tracts object and then in the menu, navigate to and select **Object > Convert > Curve**.
2. Next, go to the **Curve Options** in the right toolbar and expand the **Geometry Tab**.
3. Under **Bevel** set the **Depth** option to some value greater than 0. The bigger this depth value, the thicker your tracts will be.
4. After selecting a nice bevel depth value that you like, select the object again (which is now a curve) and navigate to **Object > Convert > Mesh**. This transforms the curve back into a mesh that can be textured however you want!
5. You're all set, so go crazy with visualizations!

https://user-images.githubusercontent.com/22922192/163030172-5a004be5-e077-4571-94db-b24fe6cba8a6.mp4

## Enjoy!

Thank you for both your interest in this plugin, and for your interest in neuroscience! We need more people like you!

![tractsgif](https://user-images.githubusercontent.com/22922192/163020980-f37acd09-0988-4903-aa5c-428b7bca1ad4.gif)
