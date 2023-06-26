"""
Platformer
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 2
TILE_SCALING = 2

TILE_WIDTH = 42

GRAVITY = 1

PLAYER_MOVEMENT_SPEED = 5
PlAYER_JUMP_SPEED = 20

class MyGame(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        # Scene object
        self.scene = None

        # Variable for player sprite
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Camera that can be used for scrolling the screen
        self.camera = None

    def setup(self):
        """
        Setup game. Call for reset
        """

        # Initialize scene
        self.scene = arcade.Scene()

        # Create sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls")

        # Create ground
        for x in range(21, SCREEN_WIDTH, 42):

            wall = arcade.Sprite("images/tile_0001.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = wall.height/2
            self.scene.add_sprite("Walls", wall)

        # More stuff on ground

        coordinate_list = [[TILE_WIDTH*9.5, TILE_WIDTH*1.5]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/tile_0071.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Setup player sprite
        self.player_sprite = arcade.Sprite("images/tile_0019.png", CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.scene.add_sprite("Player", self.player_sprite)

        # Create physics egnine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

        # Set up camera
        self.camera =  arcade.Camera(self.width, self.height)

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        """
        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        """
        if screen_center_y < 0:
            screen_center_y = 0
        
        player_centered = screen_center_x, screen_center_y
        
        self.camera.move_to(player_centered)

    def on_draw(self):
        """
        Render the screen
        """

        self.clear()
        self.scene.draw()

        self.camera.use()

    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PlAYER_JUMP_SPEED
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