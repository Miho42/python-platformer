"""
Platformer
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CAMERA_OFFSET = 100
CAMERA_SCROLL_SPEED = 0.01

CHARACTER_SCALING = 2
TILE_SCALING = 2

TILE_WIDTH = 42

GRAVITY = 1

PLAYER_MOVEMENT_SPEED = 5
PlAYER_JUMP_SPEED_BAD = 20
PlAYER_JUMP_SPEED_GOOD = 10
PLAYER_START_X = SCREEN_WIDTH/2
PLAYER_START_Y = SCREEN_HEIGHT/2 + 100
PLAYER_GRAPHIC =  {
    "god": arcade.load_texture("images/tile_0019.png"),
    "ond": arcade.load_texture("images/tile_0109.png")
}

# Layer names
LAYER_NAME_PLATFORMS = "Walls"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_DONT_TOUCH = "Don't touch"

class MyGame(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        # Variable for map
        self.tile_map = None

        # Scene object
        self.scene = None

        # Variable for player sprite
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Camera that can be used for scrolling the screen
        self.camera = None

        # Camera for GUI elements
        self.gui_camera = None

        # Variable counting number of collected coins
        self.collected_coins = 0

    def setup(self):
        """
        Setup game. Call for reset
        """

        # Set up cameras
        self.camera =  arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        layer_options={
            "Walls": {"use_spatial_hashing" : True}
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap("map01.tmx", TILE_SCALING, layer_options)

        # Initialize scene with tile_map, this will automatically add all
        # layers from the map as SpriteLists to the scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of collected coins
        self.collected_coins = 0

        # Setup player sprite
        self.player_sprite = arcade.Sprite("images/tile_0019.png", CHARACTER_SCALING)
        self.player_good = True
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Create physics egnine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def center_camera_to_player(self, camera_scroll_speed=CAMERA_SCROLL_SPEED):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        player_centered = screen_center_x, screen_center_y
        
        self.camera.move_to(player_centered, camera_scroll_speed)

    def player_change_mode(self):
        cam_x, _ = self.camera.position

        # minus PLAYER_START_X to set player and camera to the same "start point"
        if ((self.player_sprite.center_x - PLAYER_START_X) - cam_x) > 0:
            self.player_good = False
        else:
            self.player_good = True

        if self.player_good == True:
            self.player_sprite.texture = PLAYER_GRAPHIC["god"]
        else:
            self.player_sprite.texture = PLAYER_GRAPHIC["ond"]

    def on_draw(self):
        """
        Render the screen
        """

        self.clear()

        self.camera.use()
        
        self.scene.draw()
        
        # Activate gui camera before drawing gui elements
        self.gui_camera.use()
        
        # Draw score on screen, scrolling with viewport
        score_text = f"Collected coins: {self.collected_coins}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        # Draw line to seperate the two sides
        arcade.draw_line(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT,
            SCREEN_WIDTH/2,
            0,
            arcade.color.BLACK,
            5,
        )
        

    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

        # Do we hit any coins?
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_COINS])

        # Loop through coins we hit and remove it
        for coin in coin_hit_list:
            # Remove coin
            coin.remove_from_sprite_lists()
            self.collected_coins += 1

        # Did player fall off map?
        if self.player_sprite.center_y < -SCREEN_HEIGHT:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.center_camera_to_player(0.1)

        # Did player touch something they shouldn't?
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]):
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
        
        # Should player change their mode?
        self.player_change_mode()
            
    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                if self.player_good == True:
                    self.player_sprite.change_y = PlAYER_JUMP_SPEED_GOOD
                else: self.player_sprite.change_y = PlAYER_JUMP_SPEED_BAD
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        
    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is released
        """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    """
    Main function
    """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()    