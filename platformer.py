"""
Platformer
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CAMERA_OFFSET = 50
CAMERA_SCROLL_SPEED = 0.01

CHARACTER_SCALING = 2
TILE_SCALING = 2

TILE_WIDTH = 42

GRAVITY = 0.5

PLAYER_MOVEMENT_SPEED = 5
PlAYER_JUMP_SPEED_BAD = 14
PlAYER_JUMP_SPEED_GOOD = 9
PLAYER_GRAPHIC =  {
    "god_idle": arcade.load_texture("images/tile_0019.png"),
    "god_jump_right": arcade.load_texture("images/tile_0026.png"),
    "god_jump_left": arcade.load_texture("images/tile_0026.png", flipped_horizontally=1),
    "god_fall_right": arcade.load_texture("images/tile_0023.png"),
    "god_fall_left": arcade.load_texture("images/tile_0023.png", flipped_horizontally=1),
    "god_land_right": arcade.load_texture("images/tile_0022.png"),
    "god_land_left": arcade.load_texture("images/tile_0022.png", flipped_horizontally=1),
    "ond_idle": arcade.load_texture("images/tile_0109.png"),
    "ond_jump_right": arcade.load_texture("images/tile_0116.png"),
    "ond_jump_left": arcade.load_texture("images/tile_0116.png", flipped_horizontally=1),
    "ond_fall_right": arcade.load_texture("images/tile_0113.png"),
    "ond_fall_left": arcade.load_texture("images/tile_0113.png", flipped_horizontally=1),
    "ond_land_right": arcade.load_texture("images/tile_0112.png"),
    "ond_land_left": arcade.load_texture("images/tile_0112.png", flipped_horizontally=1),
}

RIGHT_FACING = "right"
LEFT_FACING = "left"

# Layer names
LAYER_NAME_PLATFORMS = "Walls"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_DONT_TOUCH = "Don't touch"
LAYER_NAME_SAVE_POINTS = "Savepoints"
LAYER_NAME_START_POINT = "Startpoint"

class Player(arcade.Sprite):
    """
    Class for the player
    """

    def __init__(self):
        super().__init__()

        # Direction
        self.character_face_direction = RIGHT_FACING

        # Track jumping
        self.is_jumping = False
                          
    def update_animation(self, mode, delta_time: float = 1 / 60):

        # Facing left or right?
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = PLAYER_GRAPHIC[f"{mode}_jump_{self.character_face_direction}"]
            self.is_jumping = True
            return
        if self.change_y < 0:
            self.texture = PLAYER_GRAPHIC[f"{mode}_fall_{self.character_face_direction}"]
            self.is_jumping = True
            return
        
        if self.change_y == 0 and self.is_jumping == True:
            self.texture = PLAYER_GRAPHIC[f"{mode}_land_{self.character_face_direction}"]
            self.is_jumping = False
            return
        
        # Player walk/idle
        if self.change_x:
            self.texture = PLAYER_GRAPHIC[f"{mode}_idle"]
            return

class MyGame(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        # Variable for map
        self.tile_map = None

        # Scene object
        self.scene = None

        # Variable for level
        self.level = 1

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

        # List for emitters
        self.emitter_list = []

    def setup(self):
        """
        Setup game. Call for reset
        """

        # Variables for keyboard control
        self.right_pressed = False
        self.left_pressed = False

        layer_options={
            "Walls": {"use_spatial_hashing" : True}
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(f"map0{self.level}.tmx", TILE_SCALING, layer_options)

        # Initialize scene with tile_map, this will automatically add all
        # layers from the map as SpriteLists to the scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        # Keep track of collected coins
        self.collected_coins = 0

        # Square for seperating screen
        self.dark_side = arcade.Sprite(
            center_y=SCREEN_HEIGHT/2,
            texture=arcade.make_soft_square_texture(SCREEN_HEIGHT, arcade.color.BLACK, 255, 255)
        )
        self.dark_side.alpha = 128
        self.dark_side.left = SCREEN_WIDTH/2

        # Setup player sprite
        #self.player_sprite = arcade.Sprite("images/tile_0019.png", CHARACTER_SCALING)
        self.player_sprite = Player()
        self.player_sprite.texture = PLAYER_GRAPHIC["god_idle"]
        self.player_mode = "god"
        self.player_sprite.scale = TILE_SCALING
        self.spawn_point = self.scene[LAYER_NAME_START_POINT][0]
        self.player_sprite.position = self.spawn_point.position
        self.scene.add_sprite("Player", self.player_sprite)

        # Set up cameras
        self.camera =  arcade.Camera(self.width, self.height)
        player_tile = self.screen_to_tile(self.player_sprite.center_x, self.player_sprite.center_y)
        self.camera_go_to_tile(player_tile[0], player_tile[1])
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Create physics egnine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

        # No save points has been touched
        for sp in self.scene[LAYER_NAME_SAVE_POINTS]:
            sp.taken = False

        # Timer
        self.timer = 0

    def center_camera_to_player(self, camera_scroll_speed=CAMERA_SCROLL_SPEED):
        """
        Moves camera to player
        """
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        player_cam_dist = abs(self.player_sprite.center_x - (self.camera.position[0] + (self.camera.viewport_width/2)))
        if player_cam_dist > CAMERA_OFFSET:

            self.camera.move_to((screen_center_x, screen_center_y), camera_scroll_speed)
        else: self.camera.move_to((self.camera.position[0], screen_center_y), camera_scroll_speed)
                 
    def player_change_mode(self):
        """
        If needed changes player_good and runs get_player_change_mode_emitter()
        """

        cam_x, _ = self.camera.position

        # minus PLAYER_START_X to set player and camera to the same "start point"
        if ((self.player_sprite.center_x - self.camera.viewport_width/2) - cam_x) > 0:
            if self.player_mode == "god":
                self.player_mode = "ond"
                self.emitter_list.append(self.get_player_change_mode_emitter())
        elif self.player_mode == "ond":
            self.player_mode = "god"
            self.emitter_list.append(self.get_player_change_mode_emitter())

    def get_collected_coin_emitter(self, pos_x, pos_y):
        new_emitter = arcade.make_burst_emitter(
        center_xy=[pos_x, pos_y],
        filenames_and_textures=["images/tile_0078.png"],
        particle_count=10,
        particle_speed=2,
        particle_lifetime_min=0.5,
        particle_lifetime_max=1,
        particle_scale=2
        )
        return new_emitter

    def get_player_change_mode_emitter(self):
        new_emitter = arcade.make_burst_emitter(
            center_xy=self.player_sprite.position,
            filenames_and_textures=["images/tile_0596.png"],
            particle_count=50,
            particle_speed=0.7,
            particle_lifetime_min=0.1,
            particle_lifetime_max=1,
            particle_scale=2
        )

        return new_emitter
    
    def get_new_spawn_point_emitter(self, pos):
        new_emitter = arcade.make_burst_emitter(
            center_xy=pos,
            filenames_and_textures=["images/tile_0896.png"],
            particle_count=10,
            particle_speed=1,
            particle_lifetime_min=0.5,
            particle_lifetime_max=2,
            particle_scale=2
        )

        return new_emitter

    def on_draw(self):
        """
        Render the screen
        """

        self.clear()

        self.camera.use()
        
        self.scene.draw()

        for e in self.emitter_list:
            e.draw()
        
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
        self.dark_side.draw()      

    def camera_go_to_tile(self, tile_x, tile_y):
        tw = self.tile_map.tile_width*TILE_SCALING
        th = self.tile_map.tile_height*TILE_SCALING
        x = tw*tile_x - self.camera.viewport_width/2 - tw/2 
        y = th*tile_y - self.camera.viewport_height/2 - th/2

        self.camera.move_to((x, y))

    def tile_to_screen(self, tile_x, tile_y):
        """
        Takes a tile coordinate and returns a screen coordinate
        """
        tw = self.tile_map.tile_width * TILE_SCALING
        th = self.tile_map.tile_height * TILE_SCALING
        screen_x = tw*tile_x - self.camera.viewport_width/2 - tw/2
        screen_y = th*tile_y - self.camera.viewport_height/2 - th/2

        return screen_x, screen_y

    def screen_to_tile(self, screen_x, screen_y):
        """
        Takes a screen coordinate and returns a tile coordinate
        """
        tile_x = screen_x/(self.tile_map.tile_width*TILE_SCALING)
        tile_y = screen_y/(self.tile_map.tile_height*TILE_SCALING)

        return round(tile_x), round(tile_y)

    def on_update(self, delta_time):
        """
        Movement and game logic
        """
        # Count time
        self.timer += delta_time
        
        # Move the player with the physics engine
        self.physics_engine.update()
        
        # Position the camera
        self.center_camera_to_player()

        # Do we hit any coins?
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_COINS])

        # Loop through coins we hit and remove it
        for coin in coin_hit_list:
            # Remove coin
            self.emitter_list.append(self.get_collected_coin_emitter(coin.center_x, coin.center_y))
            coin.remove_from_sprite_lists()
            self.collected_coins += 1

        # Did player fall off map?
        if self.player_sprite.center_y < -SCREEN_HEIGHT:
            self.player_sprite.position = self.spawn_point.position
            self.center_camera_to_player(0.1)

        # Did player touch something they shouldn't?
        if arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]):
            self.player_sprite.position = self.spawn_point.position

        # Did player touch spawn point?
        for sp in arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_SAVE_POINTS]):
            self.spawn_point = sp
            if sp.taken == False:
                sp.taken =True
                self.emitter_list.append(self.get_new_spawn_point_emitter(sp.position))

            # Is level over?
            number_of_taken_flags = 0
            for sp in self.scene[LAYER_NAME_SAVE_POINTS]:
                if sp.taken == True:
                    number_of_taken_flags += 1

            if number_of_taken_flags == len(self.scene[LAYER_NAME_SAVE_POINTS]):
                score = (self.collected_coins/self.timer) * 100
                print(self.timer)
                print(self.collected_coins)
                print(f"level {self.level} score: {round(score)}")
                self.level += 1
                self.setup()

        
        # Should player change their mode?
        self.player_change_mode()
        if self.player_mode == "god":
            self.player_sprite.texture = PLAYER_GRAPHIC["god_idle"]
        else:
            self.player_sprite.texture = PLAYER_GRAPHIC["ond_idle"]

        # Update player animation
        self.player_sprite.update_animation(self.player_mode)

        # Update emitters
        for e in self.emitter_list:
            e.update()
                

    def keyboard_control(self):
            # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0


    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                if self.player_mode == "god":
                    self.player_sprite.change_y = PlAYER_JUMP_SPEED_GOOD
                else: self.player_sprite.change_y = PlAYER_JUMP_SPEED_BAD
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.keyboard_control()

    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is released
        """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.keyboard_control()

def main():
    """
    Main function
    """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()    