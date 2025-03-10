from app.models.db import db, environment, SCHEMA
from flask.cli import AppGroup
from .users import seed_users, undo_users
from .colors import seed_colors, undo_seed_colors
from .sizes import seed_sizes, undo_seed_sizes
from .listings import undo_listings
from .listing_colors import seed_listing_colors, undo_listing_colors
from .listing_sizes import seed_listing_sizes, undo_listing_sizes
from .images import seed_images, undo_images
from .categories import seed_categories, undo_categories



# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command, which will  truncate all tables prefixed with 
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below

        undo_categories()
        undo_images()
        undo_listing_sizes()
        undo_listing_colors()
        undo_seed_colors()
        undo_seed_sizes()
        undo_listings()
        undo_users()
    seed_users()
    seed_sizes()
    seed_colors()
    seed_listing_colors()
    seed_listing_sizes()
    seed_images()
    seed_categories()

    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():

    undo_categories()
    undo_images()
    undo_listing_sizes()
    undo_listing_colors()
    undo_seed_colors()
    undo_seed_sizes()
    undo_listings()
    undo_users()
    # Add other undo functions here
