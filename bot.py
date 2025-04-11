from flask import Flask
import os
import threading
import discord
import random
import json
from discord.ext import commands

# === Flask App for Uptime Ping ===
app = Flask(__name__)


@app.route('/')
def home():
    return "I'm alive"


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


# Start Flask in background
threading.Thread(target=run_flask).start()

# === Load Token & Setup Bot ===
TOKEN = os.environ.get("DISCORD_TOKEN")
print(f"🔐 Token loaded? {'Yes' if TOKEN else 'No'}")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.dm_messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Book Swap Data ===
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


# === Bot Events & Commands ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def bookswap(ctx):
    user_id_str = str(ctx.author.id)
    if user_id_str in book_swap_partners:
        partner_id = book_swap_partners[user_id_str]
        partner_name = user_real_names.get(partner_id, f"<@{partner_id}>")
        try:
            await ctx.author.send(
                f"📚 Your book swap partner is **{partner_name}**! I'm sure you'll pick the perfect book for them! 🎁"
            )
            await ctx.message.add_reaction("👍")
        except discord.Forbidden:
            await ctx.send(
                "❌ I can't DM you! Please enable DMs and try again.",
                delete_after=5)
    else:
        await ctx.send("❌ You're not in the book swap list!", delete_after=5)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        sender_id = str(message.author.id)
        if sender_id in book_swap_partners:
            giftee_id = book_swap_partners[sender_id]
            giftee = await bot.fetch_user(int(giftee_id))
            if giftee:
                try:
                    await giftee.send(
                        f"📩 Message from your gifter: {message.content}")
                    await message.author.send("✅ Your message has been sent!")
                except discord.Forbidden:
                    await message.author.send(
                        "❌ Your giftee has DMs disabled. Try another method.")
            else:
                await message.author.send(
                    "❌ The giftee could not be found. Please check the ID.")
        else:
            await message.author.send(
                "❌ You are not in the book swap list or your giftee is unavailable."
            )
    await bot.process_commands(message)


# === Witch Name Feature ===
SAVE_FILE = "witch_names.json"

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        witch_names = {int(k): v for k, v in json.load(f).items()}
else:
    witch_names = {}

first_names = [
    "Eira", "Seraphina", "Lilith", "Morgana", "Rowena", "Nyx", "Thalassa",
    "Ophelia", "Celeste", "Isolde", "Morwen", "Vespera", "Althea", "Bryony",
    "Sylva", "Rhiannon", "Faye", "Elowen", "Juniper", "Ondine", "Lunaria",
    "Tempest", "Aradia", "Selene", "Belladonna", "Corvina", "Fenella",
    "Gwyneira", "Hecate", "Ione", "Manon"
]

dark_words = [
    "Shadow", "Ash", "Moon", "Night", "Blood", "Thorn", "Dark", "Storm",
    "Dusk", "Frost", "Grave", "Obsidian", "Raven", "Mist", "Echo", "Hollow",
    "Wraith", "Drift", "Phantom", "Chill", "Shade", "Ember", "Glare", "Crypt",
    "Fog", "Iron", "Whisper", "Black", "Shiver"
]

witchy_words = [
    "brew", "veil", "whisper", "flame", "charm", "hex", "gleam", "curse",
    "shroud", "spark", "chant", "glow", "bite", "dust", "glee", "flicker",
    "ember", "glimmer", "kiss", "flare", "howl", "tide", "blade", "spell",
    "song", "sigh", "bloom", "aura", "beak"
]


def generate_witch_name():
    return f"{random.choice(first_names)} {random.choice(dark_words)}{random.choice(witchy_words)}"


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
        await ctx.send(
            "You don't have a witch name yet! Try `!witchname` to get one.")


@bot.command()
async def rerollwitchname(ctx):
    user_id = ctx.author.id
    new_name = generate_witch_name()
    witch_names[user_id] = new_name
    save_witch_names()
    await ctx.send(f"🔁 Your new witch name is **{new_name}**")


@bot.command()
async def coven(ctx):
    if not witch_names:
        await ctx.send("🧹 No witches have claimed their names yet!")
        return

    result_lines = ["🔮 **Coven Members** 🔮"]
    for user_id, witch_name in witch_names.items():
        member = ctx.guild.get_member(user_id)
        display_name = member.display_name if member else f"User ID {user_id}"
        result_lines.append(f"**{display_name}** — *{witch_name}*")

    result = "\n".join(result_lines)
    if len(result) > 2000:
        for chunk in [result[i:i + 1990] for i in range(0, len(result), 1990)]:
            await ctx.send(chunk)
    else:
        await ctx.send(result)


# === Final Bot Startup ===
if __name__ == "__main__":
    if TOKEN:
        print("🚀 Starting Discord bot...")
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN not found in environment variables!")
