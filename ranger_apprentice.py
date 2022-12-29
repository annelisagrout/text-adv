


"""
Welcome to this Ranger's Apprentice Minigame!
"""

# Import the library contents
import adventurelib as adv

# Define your rooms



stable = adv.Room(
    """
There is a small stable with three stalls, two of which are empty.
One of the stalls holds a small, scruffy horse,
that you mysteriosly know is named "Acorn".
And also there's the label on the stall.
with a nearly empty water trough and a small pile of hay.
There is a saddle on a rack.

Across the stable yard, to the East, you see a small cabin.
To the North, you see the small path that led you here.
"""
)

cabin = adv.Room(
    """
There is a bed, a fireplace, a dusty table with 4 chairs scattered around,
and a rocking chair by the fire. There is also a small desk with some loose sheets of paper.
A couple of the pieces of paper has an oak leaf insignia. On a peg on the wall,
there is a grey and green mottled cloak hung on a peg by the locked door.
The window, before you crashed through, was thick canvas with libral amounts of oil.

To the West is the stable.
"""
)

forest = adv.Room(
    """
You are in a forest. There is a small path. If you look closely,
you may even see some trees around the forest. The path leads south,
and seems to start exactly where you are standing. It is early morning,
and you seem to be healthy and in reasonable shape...

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

@adv.when("inventory")
@adv.when("inv")
@adv.when("i")
def list_inventory():
    if inventory:
        print("You have the following items:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("You have nothing in your inventory.")


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
            I'll need to avoid suspicion by leaving Acorn here.""")
    
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
        go("east")

        

# Create your items
saddle = adv.Item("nice saddle, but dusty", "saddle")
saddle.use_item = saddle_horse

cloak = adv.Item("a mottled cloak in good condition", "cloak")
cloak.use_item = wear_cloak

papers = adv.Item("a sheaf of papers with an oak leaf insignia.", "papers")
papers.use_item = read_papers
# Create empty Bags for room contents
forest.contents = adv.Bag()
cabin.contents = adv.Bag()
stable.contents = adv.Bag()

# Put the key in the bedroom
stable.contents.add(saddle)
cabin.contents.add(papers)
cabin.contents.add(cloak)


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