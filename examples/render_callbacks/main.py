'''
Created on 03/03/2012

@author: adam
'''

import math

from pyglet.gl import *
import pyglet

# over-ride the default pyglet idle loop
import renderer.idle
import renderer.window
from renderer.viewport import Viewport
from renderer.projection_view_matrix import ProjectionViewMatrix
from scene.scene_node import SceneNode
from scene.render_callback_node import RenderCallbackNode
from scene.camera_node import CameraNode
import maths.quaternion

import grid


class Application( object ):
    
    def __init__( self ):
        super( Application, self ).__init__()
        
        # setup our opengl requirements
        config = pyglet.gl.Config(
            depth_size = 16,
            double_buffer = True
            )

        # create our window
        self.window = pyglet.window.Window(
            fullscreen = False,
            width = 1024,
            height = 768,
            config = config
            )

        # create a viewport that spans
        # the entire screen
        self.viewport = Viewport(
            [ 0.0, 0.0, 1.0, 1.0 ]
            )

        # setup our scene
        self.setup_scene()
        
        # setup our update loop the app
        # we'll render at 60 fps
        frequency = 60.0
        self.update_delta = 1.0 / frequency
        # use a pyglet callback for our render loop
        pyglet.clock.schedule_interval(
            self.step,
            self.update_delta
            )

        print "Rendering at %iHz" % int(frequency)

    def setup_scene( self ):
        # create a scene
        self.scene_node = SceneNode( '/root' )

        # create a grid to render
        self.grid_node = RenderCallbackNode(
            '/grid',
            grid.initialise_grid,
            grid.render_grid
            )
        self.scene_node.add_child( self.grid_node )

        # rotate the mesh so it is tilting forward
        self.grid_node.pitch( math.pi / 4.0 )

        # move the grid backward so we can see it
        self.grid_node.translate(
            [ 0.0, 0.0, -80.0 ]
            )

        # create a camera and a view matrix
        self.view_matrix = ProjectionViewMatrix(
            fov = 60.0,
            near_clip = 1.0,
            far_clip = 200.0
            )
        self.camera = CameraNode(
            '/camera',
            self.view_matrix
            )
        self.scene_node.add_child( self.camera )

        # set the viewports camera
        self.viewport.set_camera( self.scene_node, self.camera )
    
    def run( self ):
        pyglet.app.run()
    
    def step( self, dt ):
        # rotate the mesh about it's own vertical axis
        self.grid_node.yaw( dt )

        # render the scene
        viewports = [ self.viewport ]
        renderer.window.render( self.window, viewports )

        # display the frame buffer
        self.window.flip()
    

def main():
    # create app
    app = Application()
    app.run()
    app.window.close()


if __name__ == "__main__":
    main()

