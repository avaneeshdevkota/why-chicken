import random
add_library("sound")
add_library("minim")

# Fixing the resolution of the game window.
X_RES = 600
Y_RES = 600
    
class Game:
    def __init__(self):
        self.state = "Title"                                                   # Determines the state of the game and changes dynamically according to what player does.
        self.score = 0                                                         # Initialize the score.
        
        # Setting the attributes as empty strings to be later accessed by other objects and processing methods (look at the draw function).
        self.road = ""
        self.track = ""
        self.train = ""
        self.car1 = ""
        self.car2 = ""
        self.car3 = ""
        self.chicken = ""
        self.cautious = ""
        self.cryo = ""
        
        # Initializing the highscore as empty string before reading and writing the highscore into it.
        self.highscore = ""
        self.reached_highscore = False                                          # Checks if the player has surpassed the highest score.
    
    def high_score(self):
        # Opening the file in 'append' mode to avoid FileNotFound error.
        file = open("highscore.txt", 'a')
        file.close()
        
        # Opening the file in 'read' mode to read the highscore.
        file = open("highscore.txt", 'r')
        highscore = file.readline()
        self.highscore = highscore                                              # Assigns the current highscore, if any, into the attribute.
        file.close()
        
        if highscore.strip() == "":                                             # Checks if any previous highscore exists and if no any highscore is found, symbolized by the empty string, writes the current score as the highscore
            file = open("highscore.txt", 'w')
            file.write(str(game.score))
            self.highscore = self.score
            file.close()
        elif int(highscore.strip()) < self.score:                               # if previous highscore exists, checks if the highscore is surpassed and writes the updated highscore to the file.
            if self.reached_highscore == False:
                SoundFile(this, "./sounds/highscore_sound.wav").play()
                self.reached_highscore = True
            file = open("highscore.txt", 'w')
            file.write(str(self.score))
            self.highscore = self.score
            file.close()
        
    def increase_score(self):
        self.score += 1
    
    def collision_with_vehicle(self):
        for car in car_manager.cars:                                            # Iterates through all the cars.
            # Detects collision with any of the Cars.
            if chicken.y_pos == car.y and (chicken.x_pos <= car.x + car.car_length and chicken.x_pos + chicken.width_ >= car.x):
                # Checks if the Cautions Chicken power-up is active.
                if power_up.is_cautious:
                    # Returns the chicken to the first safe grassy lane.
                    chicken.y_pos = Y_RES - road.h + (road.h - chicken.height_)//2 
                    # Deactivates the Cautious Chicken power-up
                    power_up.is_cautious = False
                else:
                    # Changes the game state from "Playing" to "Over".
                    game.state = "Over"
                    SoundFile(this, "./sounds/chicken_death.mp3").play()
                    
                
            # Detects collision with the Train.
            if chicken.y_pos == train.y + (train.train_height - chicken.height_)//2 and chicken.x_pos <= train.x + train.train_length and chicken.x_pos + chicken.width_ >= train.x:
                # Changes the game state from "Playing" to "Over".
                game.state = "Over"
                SoundFile(this, "./sounds/chicken_death.mp3").play()
        
    def new_scene(self):                                                         # Implements all the changes that occur when the Chicken crosses the final lane in a scene.
        
        # Returns the chicken to the first safe grassy lane.
        chicken.y_pos = Y_RES - road.h + (road.h - chicken.height_)//2 
        # Randomly sets the train track into one of the eight vehicle lanes.
        train.track = random.randint(1, 7)
        train.set_track(train.track)
        # Sets the train's x position to the extreme right of the screen. The train is basically outside the display/ Resolution of the game window.
        train.reset_train()
        
        # Deletes all the previous cars.
        car_manager.cars = []

        self.increase_car_speed()
        
        # If Cryo Chicken was active in the previous scene, the speed of the cars is returned to the actual value (before the power-up was picked up).
        if power_up.is_cryo:
            car_manager.dx = car_manager.current_dx + 0.5
            # Deactivates the power-up.
            power_up.is_cryo = False
        
        # Decides if a power-up should be dropped, if yes, which power-up and where to drop it.
        power_up.decide_drop()
        power_up.is_picked_up = False
        
        # Deactivates Cautious Chicken power-up.
        power_up.is_cautious = False
        
        # Ensures the train sound is played in the new scene.
        train.play_sound = True
        
    def increase_car_speed(self):
        car_manager.dx += 0.5
        
    def title_screen(self):
        image(loadImage("./images/title_screen.png"), 0,0, X_RES, Y_RES)
        
    def pause_screen(self):
        fill(120,120,120)
        rect(0, Y_RES // 2 - road.h, X_RES, road.h * 2)
        image(loadImage("./images/pause.png"), 0, Y_RES // 2 - road.h)
        noFill()
        
    def end_screen(self):
        self.high_score()                                            # Reads the highscore to display and updates the highscore.
        image(loadImage("./images/end_screen.png"), 0, 0, X_RES, Y_RES)
        textSize(60)
        fill(255)
        # Displays the Score and Highscore.
        text(str(self.score), 460, 500)
        text(str(self.highscore), 460, 570)
        textSize(25)
    
class Road:
    def __init__(self):
        # Set Road Width and Height
        self.w = X_RES
        # Divided by 10 to get 10 lanes.
        self.h = Y_RES // 10
        
        self.img_path = "./images/road.png"
        
    def display(self):
        # Displays all the roads.
        for i in range(self.h, Y_RES - road.h, self.h):
            image(game.road, 0, i, X_RES, road.h)

class Chicken:
    def __init__(self):
        # Set Chicken height, width, and its position.
        self.height_ = 40
        self.width_ = 40
        self.x_pos = X_RES // 2 - self.width_ // 2
        self.y_pos = Y_RES - road.h + (road.h - self.height_)//2
        
        self.img_path = "./images/chicken.png"
        
    def display(self):                                            # Displays the Chicken
        if power_up.is_cautious == True:
            # Makes the Chicken Red
            chicken.img_path = "./images/cautious_chicken.png"
            image(loadImage(chicken.img_path), chicken.x_pos, chicken.y_pos, chicken.width_, chicken.height_)
        elif power_up.is_cryo == True:
            # Makes the Chicken Blue
            chicken.img_path = "./images/cryo_chicken.png"
            image(loadImage(chicken.img_path), chicken.x_pos, chicken.y_pos, chicken.width_, chicken.height_)
        else:
            # Normal Chicken
            chicken.img_path = "./images/chicken.png"
            image(game.chicken, self.x_pos, self.y_pos, self.width_, self.height_)
        
    def move_up(self):
        self.y_pos -= road.h
        
        # If chicken exits from the top of the screen, it means that it has gone to the next scene, so new_scene is called.
        if self.y_pos < 0:
            game.new_scene()
    
    def move_left(self):
        # Restrict the horizontal movement so that it does not move out of the screen.
        if self.x_pos > road.h:
            self.x_pos -= road.h
            
    def move_right(self):
        # Restrict the horizontal movement so that it does not move out of the screen.
        if self.x_pos + self.width_ < X_RES - road.h:
            self.x_pos += road.h
            
class CarManager:
    def __init__(self):
        # List of car objects that are spawned.
        self.cars = []
        # Instantiating a Car object.
        self.car = Car()
        # Initial speed of the cars.
        self.dx = 2
        # Storing current_dx for when Cryo is deactivated
        self.current_dx = self.dx
        
        self.car1_path = "./images/car1.png"
        self.car2_path = "./images/car2.png"
        self.car3_path = "./images/car3.png"
    
    def spawn_car(self):
        # If the cars list is empty, it instantiates a new car and adds it to the list.
        if len(self.cars) == 0:
            self.cars.append(self.car)
        else:
            # Instantiates a new car object and compares its distance from the previous one to determine if the car is added to the list or not.
            car = Car()
            
            # Checks if the previously generated is sufficiently far enough and in a different lane to spawn another car, and for the chicken to have space to move.
            if self.car.x + self.car.car_length * random.randint(1, 3) <= car.x  and self.car.y != car.y:
                self.cars.append(car)
                
                # Re-assigns the current car to be the previous car for another car.
                self.car = car
        
        self.display()
    
    def display(self):
        # Displays different cars according to their lengths.
        for car in self.cars:
            if car.car_length == 50:
                image(game.car1, car.x, car.y, car.car_length, car.car_height)
            elif car.car_length == 60:
                image(game.car2, car.x, car.y, car.car_length, car.car_height)
            else:
                image(game.car3, car.x, car.y, car.car_length, car.car_height)
                
            self.move_car(car)
    
    def move_car(self, car):
        car.x -= self.dx
        
            
class Car:
    def __init__(self):
        # Randomly determines the car length and sets the height and position of the cars.
        self.car_length = random.choice([50, 60, 70])
        self.car_height = 40
        self.x = X_RES
        
        # If the train track is in the top-most vehicle lane, the cars are spawned on other vehicle lanes, by changing the y-value of the cars.
        if train.track == 1:
            self.y = random.randint(2, 8)*road.h + (road.h - self.car_height)//2
        # If the train track is in the bottom-most vehicle lane, the cars are spawned on other vehicle lanes, by changing the y-value of the cars.
        elif train.track == 8:
            self.y = random.randint(1, 7)*road.h + (road.h - self.car_height)//2
        # If the train track is in one of the middle vehicle lane, the cars are spawned on any other vehicle lanes, by changing the y-value of the cars.
        else:
            self.y = random.choice([random.randint(1, train.track - 1), random.randint(train.track+1, 8)])*road.h + (road.h - self.car_height)//2
        
class Train:
    def __init__(self):
        # Sets the train length, height and position.
        self.train_length = 3 * X_RES
        self.train_height = 50
        self.x = X_RES
        # Randomizing where to spawn the train track and the train accordingly.
        self.track = random.randint(1, 7)
        self.y = self.track * road.h + (road.h - self.train_height)//2
        
        # Sets Speed of the train
        self.dx = 40
        
        self.train_img_path = "./images/train.png"
        self.track_img_path = "./images/track.png"
        
        # Ensuring train sound is played only once every train.
        self.play_sound = True
        
    def set_track(self, track):
        '''A setter method to change the track position and the train in every new scene'''
        self.track = track
        self.y = self.track * road.h + (road.h - self.train_height)//2
    
    def display(self):
        fill(0)
        rect(0, self.y-(road.h - self.train_height)//2, X_RES, road.h)
        noFill()
        image(game.track, 0, self.y-(road.h - self.train_height)//2, X_RES, road.h)
        
        # Plays the train sound effect when the chicken is right below the train track
        if self.play_sound == True and chicken.y_pos <= (self.track + 1)*road.h + (road.h - self.train_height):
            self.play_train_sound()
            self.play_sound = False
        
        # Moves the train when the chicken is right below the train track
        if chicken.y_pos <= (self.track + 1)*road.h + (road.h - self.train_height):
            image(game.train, self.x, self.y, self.train_length, self.train_height)
            self.move_train()
    
    def reset_train(self):
        # Returns the train to the extreme right, if it has moved outside the screen.
        if self.x + self.train_length < 0:
            self.x = X_RES
    
    def move_train(self):
        self.x -= self.dx
    
    def play_train_sound(self):
        SoundFile(this, "./sounds/train.wav").play()

class PowerUp:
    def __init__(self):
        # Since the power-ups are squares, area represents the length and height.
        self.area = chicken.width_
        
        # Initializing the position of the power-ups
        self.x = ""
        self.y = ""
        
        # Initializing the choice of power-up
        self.rand_power = ""
        
        # Deactivating the powers when initialized.
        self.is_cautious = False
        self.is_cryo = False
        
        # Setting the drop rate of power-up in terms of percentage
        self.drop_rate = 10
        # Checking if the chicken picked any of the power-up.
        self.is_picked_up = False
        
        # Initializing an attribute that will come to play later in the decide_drop method.
        self.rand_drop = ""
        
        self.decide_drop()
        
        self.cryo_img_path = "./images/cryo.png"
        self.cautious_img_path = "./images/cautious.png"
    
    def decide_drop(self):
        # Randomizes the position of the power-up
        self.x = (X_RES // 2) - (self.area//2) + (random.randint(-4,4) * road.h)
        self.y = (Y_RES - road.h + (road.h - chicken.height_)//2 ) - (random.randint(0,8) * road.h)
        
        # Randomly generates a number between 1 to 100.
        self.rand_drop = random.randint(1, 100)
        # If randomly generated number is between 1 and the drop rate, choose which power-up is to be spawned, else nothing is spawned. This gives a 10% chance of spawning the power-up.
        if 1 <= self.rand_drop <= self.drop_rate:
            self.rand_power = random.choice(["Cautious", "Cryo"])
        else:
            self.rand_power = ""
    
    def display(self):
        self.picked_up()
        
        # Displays the power-up when the power-up is yet not picked up or rand_power is not empty.
        if not self.is_picked_up:
            if self.rand_power == "Cryo":
                image(game.cryo, self.x, self.y, self.area, self.area)
            elif self.rand_power == "Cautious":
                image(game.cautious, self.x, self.y, self.area, self.area)
            
    def picked_up(self):
        # Checks if the chicken has picked the power-up, meaning both of them are in the same position.
        if chicken.y_pos == self.y and chicken.x_pos == self.x:
            
            SoundFile(this, "./sounds/powerup_pickup.wav").play()
            
            # To determine if the power-up is activated.
            self.is_picked_up = True
            
            # Activates Cautious Chicken
            if self.rand_power == "Cautious":
                self.is_cautious = True
            
            # Activates Cryo Chicken
            if self.rand_power == "Cryo":
                self.is_cryo = True
                
                # Stores the current speed of the car to revert back to it after the power-up expires.
                car_manager.current_dx = car_manager.dx
                # Sets the speed to 2.
                car_manager.dx = 2
                    
            # Hides the power-up after it has been picked.
            self.x = -100
            self.y = -100
            
game = Game()
road = Road()
train = Train()
chicken = Chicken()
car_manager = CarManager()
power_up = PowerUp()

minim = Minim(this)
    
def setup():
    frameRate(120)
    
    game.road = loadImage(road.img_path)
    game.track = loadImage(train.track_img_path)
    game.train = loadImage(train.train_img_path)
    game.car1 = loadImage(car_manager.car1_path)
    game.car2 = loadImage(car_manager.car2_path)
    game.car3 = loadImage(car_manager.car3_path)
    game.chicken = loadImage(chicken.img_path)
    game.cryo = loadImage(power_up.cryo_img_path)
    game.cautious = loadImage(power_up.cautious_img_path)
                            
    size(X_RES, Y_RES)
    background(255)
    
    font = createFont("NinjaGardenLaser-m9e9.otf", 25)
    textFont(font)
    
    global player
    player = minim.loadFile("./sounds/background.wav")
    player.loop()

def draw():
    # Displaying Title screen
    if game.state == "Title":
        game.title_screen()
    
    # Displaying Playing screen and all the elements in the game.
    elif game.state == "Playing":
        background(0,255,0)
        strokeWeight(0)
        # rect(0, 0, X_RES, road.h)
        # rect(0, Y_RES - road.h, X_RES, road.h)
        road.display()
        car_manager.spawn_car()
        game.collision_with_vehicle()
        
        train.display()
        chicken.display()
        
        if power_up.rand_power == "Cautious" or power_up.rand_power == "Cryo":
            power_up.display()
        
        # Displays the Score and Highscore.
        fill(0)
        text("Score: "+str(game.score), 450, 30)
        game.high_score()
        
        file = open("highscore.txt", 'r')
        highscore = file.readline()
        file.close()
        
        text("Highscore: " + str(highscore), 10, 30)
        noFill()
    
    # Pausing the game
    elif game.state == "Pause":
        game.pause_screen()
    
    # End Screen
    elif game.state == "Over":
        game.end_screen()

def keyPressed():
    # Deals with all the Keyboard events
    if game.state == "Playing":
        if keyCode == UP or key == 'w':
            SoundFile(this, "./sounds/chicken_jump.mp3").play()
            if game.state != "Over":
                game.increase_score()
                chicken.move_up()
        if keyCode == LEFT or key == 'a':
            SoundFile(this, "./sounds/chicken_jump.mp3").play()
            chicken.move_left()
        if keyCode == RIGHT or key == 'd':
            SoundFile(this, "./sounds/chicken_jump.mp3").play()
            chicken.move_right()
        
    if key == 'p' and game.state == "Playing":
        game.state = "Pause"
        player.pause()
        
    elif key == 'p' and game.state == "Pause":
        game.state = "Playing"
        player.play()
        
    if key == ENTER and game.state == "Title":
        game.state = "Playing"
                
    elif key == ENTER and game.state == "Over":
        game.state = "Playing"
        game.new_scene()
        game.score = 0
        car_manager.dx = 2
        game.reached_highscore = False
    
def mousePressed():
    # Deals with all the mouse events.
    if game.state == "Title":
        game.state = "Playing"
            
    elif game.state == "Over":
        game.state = "Playing"
        game.new_scene()
        game.score = 0
        car_manager.dx = 2
        game.reached_highscore = False
