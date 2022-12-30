

#TODO: make apples you can feed to the horse.
print(
"""
Welcome to this Ranger's Apprentice Minigame!
""")

# Import the library contents
import adventurelib as adv

# Define your rooms



stable = adv.Room(
    """
There is a small stable with three stalls, two of which are empty.
One of the stalls holds a small, scruffy horse,
that you mysteriosly know is named "Acorn".
And also there's the label on the stall.
There is a water trough and a small pile of hay.

"""
)

cabin = adv.Room(
    """
There is a bed, a fireplace, a dusty table with four chairs scattered around,
and a rocking chair by the fire. There is also a small desk with some loose sheets of paper.
A couple of the pieces of paper has an oak leaf insignia. On a peg on the wall,
there is a grey and green mottled cloak hung on a peg by the locked door.
The window, before you crashed through, was thick canvas with libral amounts of oil.
"""
)

forest = adv.Room(
    """
You are in a forest. There is a small path. If you look closely,
you may even see some trees around the forest. The path leads south, along a stream, 
and seems to start exactly where you are standing. You seem to be healthy and in reasonable shape...

To the south you see a glimpse of a building through the trees.
"""
)

# Define the connections between the rooms
forest.south = stable
stable.east = cabin

# Define a constraint to move from the bedroom to the living room
# If the door between the living room and front porch door is locked,
# you can't exit
stable.locked = {"east": True}

# None of the other rooms have any locked doors
forest.locked = dict()
cabin.locked = dict()

# Set the starting room as the current room
current_room = forest

# Define functions to use items
horse_saddled = False
water_full = False
bucket_full = False
slip_stable = False
slip_forest = False
slip_cabin = False

@adv.when('slip')
def slip():
    global slip_forest
    global slip_cabin
    global slip_stable
    global current_room
    
    if current_room == forest and slip_forest == True:
        print("You slipped on that nice patch of mud you made.")
    elif current_room == cabin and slip_cabin == True:
        print("You slipped on that nice puddle of water you made.")
    elif current_room == stable and slip_stable == True:
        print("You slipped on that nice patch of mud you made.")
    
    else:
        print("I'm sorry, you're going to have to spill something to slip on")

@adv.when("use bucket")
def bucket_error():
    print("I'm sorry, you're going to have to be more specific.")

@adv.when("inventory")
@adv.when("i")
def list_inventory():
    if inventory:
        print("You have the following items:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("You have nothing in your inventory.")
        
@adv.when('dump bucket')
@adv.when('empty bucket')
@adv.when('spill bucket')
def dump_bucket():
    global inventory
    obj = inventory.find('bucket')
    # Do you have this thing?
    if not obj:
        print("You don't have a bucket to spill.")
    else:
        global bucket_full
        global slip_forest
        global slip_stable
        global slip_cabin
        if bucket_full:
            print("""You dump the bucket on the ground,
creating a nice patch of mud perfect for slipping on.""")
            bucket_full = False
            if current_room == forest:
                slip_forest = True
            elif current_room == stable:
                slip_stable == True
            elif current_room == cabin:
                slip_cabin == True
        else:
            print("""Umm, you need a bucket with water in it...""")
        
@adv.when("fill bucket")
def fill_bucket():
    global inventory
    obj = inventory.find('bucket')
    # Do you have this thing?
    if not obj:
        print("You don't have a bucket, silly person.")
    else:
        global bucket_full
        if not bucket_full and current_room == forest:
            print("""You fill the bucket up from the small woodland stream.""")
            bucket_full = True
        else:
            if bucket_full:
                print("""Well, you're very through.
The bucket is already full...
How do you propose to fill it again?""")
            elif current_room != forest:
                print("And what do you plan on filling the bucket with?!")
            
            
@adv.when("wash horse")
def wash_horse():
    global inventory
    obj = inventory.find('bucket')
    # Do you have this thing?
    if not obj:
        print("You don't have a bucket. Do you need me to tell you again?")
    else:
        global bucket_full
        global horse_saddled
        if bucket_full and not horse_saddled:
            print("""You wash the horse. Now, all clean, it rolls in the dust of the stableyard.
You return it to its stall.""")
            bucket_full = False
        else:
            print("""Umm, make sure the horse is unsaddled, and your bucket is full.""")

            
@adv.when("fill trough")
@adv.when("water horse")
def fill_trough():
    global inventory
    obj = inventory.find('bucket')
    # Do you have this thing?
    if not obj:
        print("You don't have a bucket. What part of that do you not understand?")
    else:
        global bucket_full
        global water_full
        if bucket_full and not water_full and not horse_saddled:
            print("""You fill the trough and put the horse in the stall. It whickers in gratitude.""")
            bucket_full = False
            water_full = True
        else:
            print("""Umm, make sure the horse is unsaddled,
the bucket is full,
and the trough is empty.""")


@adv.when("unsaddle horse")
@adv.when("take off saddle")
def unsaddle_horse(): 
    global horse_saddled
    global inventory
    if horse_saddled:
        horse_saddled = False
        stable.contents.add(saddle)
        print("You put the saddle back on the rack and the horse back in the stall.")
    else:
        print("Did you really just try to undsaddle an unsaddled horse?")



@adv.when("saddle horse")
@adv.when("use saddle")
def saddle_horse():
    global inventory
    # Make sure you have the thing first
    obj = inventory.find('saddle')
    # Do you have this thing?
    if not obj:
        print("You don't have a saddle.")
    else:
        print("""You lead the horse into the stableyard and lift the saddle (and pad) on.
        It stands quietly as if waiting for something.""")
        inventory.take('saddle')

    global horse_saddled
    horse_saddled = True
        
@adv.when("wear cloak")
@adv.when("use cloak")
def wear_cloak():
    global inventory
    # Make sure you have the thing first
    obj = inventory.find('cloak')

    # Do you have this thing?
    if not obj:
        print("You don't have a cloak.")
    else:
        print("The cloak feels warm and comfortable. You wonder what the splotches are for. Meal stains?")
        
@adv.when("read papers")
@adv.when("use papers")
def read_papers():
        global inventory
        # Make sure you have the thing first
        obj = inventory.find('papers')

        # Do you have this thing?
        if not obj:
            print("The papers aren't close enough to read. Pick them up.")
        else:
            print("""They seem to be reports on a band of kidnappers in the area.
            At the top, near the oakleaf insignia is a small, neatly written name: "Ranger Berrigan"
            There is also a date... three days ago.
            A map holds an 'x' right on the closest village.
            A note says: "They will strike here next. Must be there.
            I'll need to avoid suspicion by leaving Acorn here." """)
            
            
@adv.when("feed horse")
@adv.when("use apples")
def feed_horse():
        global inventory
        # Make sure you have the thing first
        obj = inventory.find('some apples')
        

        # Do you have this thing?
        if not obj:
            print("And WHAT EXACTLY do you plan on feeding the horse? It already has hay...")
        else:
            print("The horse gobbles up the apples and seems to act more friendly.")
            forest.contents.add(apples)
            
@adv.when("eat apples")
def eat_error():
    print("Don't you think you'd rather save those for the horse?")
    
@adv.when("ride horse")
@adv.when("get on horse")
@adv.when("mount horse")
def ride_horse():
    if current_room == stable and horse_saddled == True:
        horse_buck(stable)
    else:
        print("The horse is not saddled. Unfortunatly, riding bareback is not very comfortable.")
        
        
def horse_buck(current_room):
        print("""You mount the horse. It stands still for a moment, then the horse bucks like crazy.
You fall off and fly through the window of the cabin. Stunned, you lay there for a moment.
You get up and have the presence of mind to unlock the door from the inside.
        
""")

        current_room.locked["east"] = False
        go('east')
        

 

# Create your items
saddle = adv.Item("a nice, dusty, saddle", "a saddle")
saddle.use_item = saddle_horse

cloak = adv.Item("a mottled cloak in good condition", "a cloak")
cloak.use_item = wear_cloak

papers = adv.Item("a sheaf of papers with an oak leaf insignia.", "some papers")
papers.use_item = read_papers

bucket = adv.Item("a small wooden bucket", "a bucket")
bucket.use_item = fill_bucket
bucket.use_item = fill_trough
bucket.use_item = wash_horse

apples = adv.Item("a bag of ripe red apples", "some apples", "apples", "bag")
apples.use_item = feed_horse

# Create empty Bags for room contents
forest.contents = adv.Bag()
cabin.contents = adv.Bag()
stable.contents = adv.Bag()

# Put the key in the bedroom
stable.contents.add(saddle)
cabin.contents.add(papers)
cabin.contents.add(cloak)
stable.contents.add(bucket)
forest.contents.add(apples)


# Set up your current empty inventory
inventory = adv.Bag()

# Define your movement commands
@adv.when("go DIRECTION")
@adv.when("north", direction="north")
@adv.when("south", direction="south")
@adv.when("east", direction="east")
@adv.when("west", direction="west")
@adv.when("n", direction="north")
@adv.when("s", direction="south")
@adv.when("e", direction="east")
@adv.when("w", direction="west")
def go(direction: str):
    """Processes your moving direction

    Arguments:
        direction {str} -- which direction does the player want to move
    """

    # What is your current room?
    global current_room

    # Is there an exit in that direction?
    next_room = current_room.exit(direction)
    if next_room:
        # Is the door locked?
        if direction in current_room.locked and current_room.locked[direction]:
            print(f"You can't go {direction} --- the cabin door is locked.")
        else:
            current_room = next_room
            print(f"You go {direction}.")
            
            slip()
            look()
            

    # No exit that way
    else:
        print(f"You can't go {direction}.")
        

        

# How do you look at the room?
@adv.when("look")
def look():
    """Looks at the current room"""

    # Describe the room
    adv.say(current_room)

    # List the contents
    for item in current_room.contents:
        print(f"There is {item} here.")

    # List the exits
    print(f"The following exits are present: {current_room.exits()}")

# How do you look at items?
@adv.when("look at ITEM")
@adv.when("inspect ITEM")
def look_at(item: str):

    # Check if the item is in your inventory or not
    obj = inventory.find(item)
    if not obj:
        print(f"You don't have {item}.")
    else:
        print(f"It's an {obj}.")

# How do you pick up items?
@adv.when("take ITEM")
@adv.when("get ITEM")
@adv.when("pickup ITEM")
def get(item: str):
    """Get the item if it exists

    Arguments:
        item {str} -- The name of the item to get
    """
    global current_room

    obj = current_room.contents.take(item)
    if not obj:
        print(f"There is no {item} here.")
    else:
        print(f"You now have {item}.")
        inventory.add(obj)

# How do you use an item?
@adv.when("unlock door", item="key")
@adv.when("use ITEM")
def use(item: str):
    """Use an item, consumes it if used

    Arguments:
        item {str} -- Which item to use
    """

    # First, do you have the item?
    obj = inventory.take(item)
    if not obj:
        print(f"You don't have {item}")

    # Try to use the item
    else:
        obj.use_item(current_room)

if __name__ == "__main__":
    # Look at the starting room
    look()

    adv.start()