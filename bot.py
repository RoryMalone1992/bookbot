from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

import discord
import random
import json
import os
from discord.ext import commandsS

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True  # ✅ Required to get display names
intents.messages = True
intents.dm_messages = True  # Allows the bot to receive DMs
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Book swap partner assignments
book_swap_partners = {
    "333312489750265860": "1348067676899246132",
    "1348067676899246132": "406963070615814174",
    "406963070615814174": "1328510002301898824",
    "1328510002301898824": "611670055679164447",
    "611670055679164447": "1215101865117745248",
    "1215101865117745248": "1303579590416928820",
    "1303579590416928820": "692495533318733884",
    "692495533318733884": "333312489750265860",
    "118143857895407619": "222510172705259521",
    "222510172705259521": "118143857895407619"
}

# IDs to real names mapping
user_real_names = {
    "333312489750265860": "Jen",
    "1348067676899246132": "Natalie",
    "406963070615814174": "Bec",
    "1328510002301898824": "Savannah",
    "611670055679164447": "Rebecca",
    "1215101865117745248": "Danielle",
    "1303579590416928820": "Audra",
    "692495533318733884": "Kait",
    "222510172705259521": "Rory",
    "118143857895407619": "Vince"
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def bookswap(ctx):
    """Sends the user a DM with their book swap partner."""
    user_id = ctx.author.id  # Get the actual user ID
    print(f"User ID (from command): {user_id}")  # Log the user ID for debugging

    # Convert the user ID to a string to match the dictionary keys
    user_id_str = str(user_id)
    print(f"Checking if {user_id_str} is in book_swap_partners")  # Log the check

    # Debugging: Print all the keys in the book_swap_partners
    print(f"Book swap partners keys: {list(book_swap_partners.keys())}")  # Log the keys in the dictionary

    if user_id_str in book_swap_partners:
        partner_id = book_swap_partners[user_id_str]  # Get the partner's ID
        partner_name = user_real_names.get(partner_id, f"<@{partner_id}>")  # Get real name if available

        try:
            await ctx.author.send(f"📚 Your book swap partner is **{partner_name}**! I'm sure you'll pick the perfect book for them! 🎁")
            await ctx.message.add_reaction("👍")  # React with a thumbs up in the channel
        except discord.Forbidden:
            await ctx.send("❌ I can't DM you! Please enable DMs and try again.", delete_after=5)
    else:
        print(f"{user_id_str} was not found in book_swap_partners.")  # Log if user is not in the list
        await ctx.send("❌ You're not in the book swap list!", delete_after=5)

@bot.event
async def on_message(message):
    """Forwards messages from gifters to their assigned giftees."""
    if message.author == bot.user:
        return  # Ignore bot messages

    if isinstance(message.channel, discord.DMChannel):  # If message is a DM
        sender_id = str(message.author.id)  # Convert the ID to a string for comparison

        print(f"Sender ID: {sender_id}")  # Debug log to check the sender ID being used

        if sender_id in book_swap_partners:
            giftee_id = book_swap_partners[sender_id]
            print(f"Giftee ID: {giftee_id}")  # Debug log to show the giftee ID

            # Try to send the message to the giftee directly
            giftee = await bot.fetch_user(int(giftee_id))  # Use fetch_user instead of get_user
            print(f"Searching for giftee: {giftee} (ID: {giftee_id})")  # Debug log to check giftee lookup

            if giftee:
                try:
                    await giftee.send(f"📩 Message from your gifter: {message.content}")
                    await message.author.send("✅ Your message has been sent!")
                    print(f"Message sent to giftee: {giftee.name}")  # Debug log when the message is successfully sent
                except discord.Forbidden:
                    await message.author.send("❌ Your giftee has DMs disabled. Try another method.")
                    print(f"Failed to send message to {giftee.name} due to DMs being disabled.")
            else:
                await message.author.send("❌ The giftee could not be found. Please check the ID.")
                print(f"Giftee not found for ID: {giftee_id}")

        else:
            await message.author.send("❌ You are not in the book swap list or your giftee is unavailable.")
            print(f"Sender ID {sender_id} is not in the book swap list.")

    await bot.process_commands(message)  # Ensure commands still work

# File path for saved witch names
SAVE_FILE = "witch_names.json"

# Load saved names if file exists
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        witch_names = json.load(f)
        # Convert string keys back to integers (user IDs)
        witch_names = {int(k): v for k, v in witch_names.items()}
else:
    witch_names = {}

# Name lists
first_names = [
    "Eira", "Seraphina", "Lilith", "Morgana", "Rowena", "Nyx", "Thalassa", "Ophelia", "Celeste", "Isolde",
    "Morwen", "Vespera", "Althea", "Bryony", "Sylva", "Rhiannon", "Faye", "Elowen", "Juniper", "Ondine",
    "Lunaria", "Tempest", "Aradia", "Selene", "Belladonna", "Corvina", "Fenella", "Gwyneira", "Hecate", "Ione", "Manon"
]

dark_words = [
    "Shadow", "Ash", "Moon", "Night", "Blood", "Thorn", "Dark", "Storm", "Dusk", "Frost",
    "Grave", "Obsidian", "Raven", "Mist", "Echo", "Hollow", "Wraith", "Dusk", "Drift", "Phantom",
    "Chill", "Shade", "Ember", "Glare", "Crypt", "Fog", "Iron", "Whisper", "Black", "Shiver"
]

witchy_words = [
    "brew", "veil", "whisper", "flame", "charm", "hex", "gleam", "curse", "shroud", "spark",
    "chant", "glow", "bite", "dust", "glee", "flicker", "ember", "glimmer", "gleam", "kiss",
    "flare", "howl", "tide", "blade", "spell", "song", "gleam", "sigh", "bloom", "aura", "beak"
]

def generate_witch_name():
    first = random.choice(first_names)
    last = random.choice(dark_words) + random.choice(witchy_words)
    return f"{first} {last}"

def save_witch_names():
    with open(SAVE_FILE, "w") as f:
        json.dump(witch_names, f)

@bot.command()
async def witchname(ctx):
    user_id = ctx.author.id
    if user_id not in witch_names:
        witch_names[user_id] = generate_witch_name()
        save_witch_names()
    await ctx.send(f"✨ Your witch name is **{witch_names[user_id]}** ✨")

@bot.command()
async def mywitchname(ctx):
    user_id = ctx.author.id
    if user_id in witch_names:
        await ctx.send(f"🖤 Your witch name is **{witch_names[user_id]}**")
    else:
        await ctx.send("You don't have a witch name yet! Try `!witchname` to get one.")

@bot.command()
async def rerollwitchname(ctx):
    user_id = ctx.author.id
    new_name = generate_witch_name()
    witch_names[user_id] = new_name
    save_witch_names()
    await ctx.send(f"🔁 Your new witch name is **{new_name}**")

@bot.command()
async def coven(ctx):
    """Lists all users with their server display name and witch name."""
    if not witch_names:
        await ctx.send("🧹 No witches have claimed their names yet!")
        return

    result_lines = ["🔮 **Coven Members** 🔮"]

    for user_id, witch_name in witch_names.items():
        member = ctx.guild.get_member(user_id)
        display_name = member.display_name if member else f"User ID {user_id}"
        result_lines.append(f"**{display_name}** — *{witch_name}*")

    # Discord message limit is 2000 characters; batch if needed
    result = "\n".join(result_lines)
    if len(result) > 2000:
        for chunk in [result[i:i+1990] for i in range(0, len(result), 1990)]:
            await ctx.send(chunk)
    else:
        await ctx.send(result)

# Keep Alive
keep_alive()

# Run the bot
bot.run(TOKEN)
