import telebot
import os
import random
import time 

API_TOKEN =  "7886745619:AAHqSMos7BAoVtiVa9k-CMbz_AFG0SrEorE" # Replace with your bot token
bot = telebot.TeleBot(API_TOKEN)
# Store player data 
players = {}
leaderboard = {}
# Load leaderboard from file
def load_leaderboard():
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as file:
            for line in file:
                name, score = line.strip().split(': ')
                leaderboard[name] = int(score)

# Save leaderboard to file
def save_leaderboard():
    with open('leaderboard.txt', 'w') as file:
        for player, score in leaderboard.items():
            file.write(f"{player}: {score}\n")

# Call load_leaderboard at the start of your bot
load_leaderboard()
save_leaderboard()


# Aliens dictionary with their abilities and power
aliens = {
    'Four Arms': {'ability': '💪 Strong Punch', 'power': 10},
    'XLR8': {'ability': '🏃‍♂️ Speed Attack', 'power': 8},
    'Heatblast': {'ability': '🔥 Fire Blast', 'power': 9},
    'Diamondhead': {'ability': '💎 Crystal Shield', 'power': 7},
    'Wildmutt': {'ability': '🐾 Claw Strike', 'power': 6},
    'Ghostfreak': {'ability': '👻 Phase Attack', 'power': 5},
    'Ripjaws': {'ability': '🦈 Water Bite', 'power': 8},
    'Stinkfly': {'ability': '🦟 Fly Sting', 'power': 6},
    'Grey Matter': {'ability': '🧠 Strategy Attack', 'power': 5},
    'Upgrade': {'ability': '⚙️ Tech Control', 'power': 9}
}
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Ben 10 Game! "
                          "Choose your alien to start a battle or type /help for instructions.")

@bot.message_handler(commands=['choose_alien'])
def choose_alien(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = {'alien': None, 'score': 0}
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    for alien in aliens.keys():
        markup.add(telebot.types.KeyboardButton(alien))
    
    bot.send_message(message.chat.id, "Choose your alien:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in aliens)
def set_alien(message):
    user_id = message.from_user.id
    players[user_id]['alien'] = message.text
    bot.reply_to(message, f"You've chosen {message.text} with the ability {aliens[message.text]['ability']}! Type /battle to start fighting!")

# Battle animation function
def battle_animation(chat_id, alien, enemy, user_power, enemy_power):
    # Battle animation sequence using emoji
    animation_sequence = [
        f"{alien} faces off against {enemy}... ⚔️",
        "🔁 Preparing for the fight...",
        "🌀 **Battle begins!**",
        f"{alien} charges forward 🏃‍♂️!",
        "👊 Punches are exchanged...",
        f"{enemy} strikes back 💥!",
        "⚡ Sparks fly as the battle heats up...",
        f"{alien} uses {aliens[alien]['ability']}!"
    ]

    for step in animation_sequence:
        bot.send_message(chat_id, step)
        time.sleep(1)  # Delay to simulate animation

    # Battle outcome
    if user_power > enemy_power:
        bot.send_message(chat_id, f"🚨 {alien} defeated {enemy}! +10 points!")
        return "win"
    else:
        bot.send_message(chat_id, f"😵 {alien} was defeated by {enemy}! Better luck next time.")
        return "lose"


@bot.message_handler(commands=['battle'])
def start_battle(message):
    user_id = message.from_user.id
    if players.get(user_id) is None or players[user_id]['alien'] is None:
        bot.reply_to(message, "You need to choose an alien first using /choose_alien!")
        return
    
    alien = players[user_id]['alien']
    enemy = random.choice(list(aliens.keys()))  # Random enemy alien
    enemy_power = random.randint(5, 10)  # Random enemy power
    player_power = aliens[alien]['power']

    # Simulate battle animation
    result = battle_animation(message.chat.id, alien, enemy, player_power, enemy_power)

    # Update player score if they win
    if result == "win":
        players[user_id]['score'] += 10
        leaderboard[message.from_user.first_name] = players[user_id]['score']



@bot.message_handler(commands=['leaderboard'])
def show_leaderboard(message):
    if not leaderboard:
        bot.reply_to(message, "Leaderboard is empty! Start battling to get on the board.")
        return
    
    # Sort the leaderboard by score in descending order
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)

    leaderboard_text = "🏆 Leaderboard 🏆\n"
    for index, (player, score) in enumerate(sorted_leaderboard):
        if index == 0:
            medal = "🥇"
        elif index == 1:
            medal = "🥈"
        elif index == 2:
            medal = "🥉"
            leaderboard_text += f"{medal} {player}: {score} points\n"
        else:
            leaderboard_text += f"{player}: {score} points\n"
    
    bot.send_message(message.chat.id, leaderboard_text)



@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = "👋 Welcome to the Ben 10 game! Here are the commands you can use:\n" \
                "/choose_alien - Choose your alien\n" \
                "/battle - Start a battle\n" \
                "/leaderboard - View the leaderboard\n" \
                "Choose an alien and battle against random enemies to earn points!"
    bot.send_message(message.chat.id, help_text)


# Polling to run the bot
bot.polling()
