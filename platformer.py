"""
Platformer
"""
import arcade

SCREEN_WITH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

class MyGame(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WITH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

    def setup(self):
        """
        Setup game. Call for reset
        """
        pass

    def on_draw(self):
        """
        Render the screen
        """

        self.clear()
        # code to draw the screen goes here

def main():
    """
    Main function
    """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()    