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

PLAYER_MOVEMENT_SPEED = 5

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
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

    def on_draw(self):
        """
        Render the screen
        """

        self.clear()
        self.scene.draw()

    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        # Move the player with the physics engine
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """

        if key == arcade.key.LEFT or key == arcade.key.A:
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