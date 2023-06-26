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

class MyGame(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        self.player_list = None
        self.wall_list = None

    def setup(self):
        """
        Setup game. Call for reset
        """

        # Create walls (wil not move -> optimize)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Create ground
        for x in range(21, SCREEN_WIDTH, TILE_WIDTH):
            wall = arcade.Sprite("images/tile_0001.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = wall.height/2
            self.wall_list.append(wall)

        # More stuff on ground
        coordinate_list = [[TILE_WIDTH*9.5, TILE_WIDTH*1.5]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/tile_0071.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Setup player sprite
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("images/tile_0019.png", CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen
        """

        self.clear()
        self.player_list.draw()
        self.wall_list.draw()

def main():
    """
    Main function
    """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()    