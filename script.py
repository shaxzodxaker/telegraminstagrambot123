import telebot
import instaloader
import os

# Initialize the Telebot with your token
bot_token = '7457158702:AAG87HIwb4QugG8S6WEVkZUPzcWWHVMfxC4'
bot = telebot.TeleBot(bot_token)

# Initialize Instaloader
L = instaloader.Instaloader()

# Login to Instagram (replace with your credentials)
try:
    L.login('shaxzodtest', 'Baradappa1')
except Exception as e:
    print(f"Failed to login to Instagram: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Quyidagi komandalarni foydalaning:\n"
                          "/profile username - Profil ma'lumotlarini olish.\n"
                          "/post_info username - Post ma'lumotlarini olish.\n"
                          "/comments username - Birinchi 5 postdagi izohlarni olish.")

@bot.message_handler(commands=['profile'])
def handle_profile(message):
    try:
        username = message.text.split()[1]
        profile = instaloader.Profile.from_username(L.context, username)

        profile_data = (
            f"Username: {profile.username}\n"
            f"Full Name: {profile.full_name}\n"
            f"Followers: {profile.followers}\n"
            f"Following: {profile.followees}\n"
            f"Posts: {profile.mediacount}\n"
            f"Bio: {profile.biography}\n"
            f"Profile Picture URL: {profile.profile_pic_url}\n"
            f"Is Private: {profile.is_private}\n"
        )

        profile_filename = f'{username}_profile.txt'
        with open(profile_filename, 'w', encoding='utf-8') as file:
            file.write(profile_data)

        with open(profile_filename, 'rb') as file:
            bot.send_document(message.chat.id, file, caption="Profil ma'lumotlari:")

        os.remove(profile_filename)

    except instaloader.exceptions.ProfileNotExistsException:
        bot.reply_to(message, "Bu username bilan profil topilmadi.")
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

@bot.message_handler(commands=['post_info'])
def handle_post_info(message):
    try:
        username = message.text.split()[1]
        profile = instaloader.Profile.from_username(L.context, username)

        posts_data = []
        for post in profile.get_posts():
            if len(posts_data) >= 10:
                break
            post_data = (
                f"\n\nPost URL: {post.url}\n"
                f"Caption: {post.caption}\n"
                f"Likes: {post.likes}\n"
                f"Comments: {post.comments}\n"
                f"Date: {post.date}\n"
            )
            posts_data.append(post_data)

        post_filename = f'{username}_post_info.txt'
        with open(post_filename, 'w', encoding='utf-8') as file:
            file.writelines(posts_data)

        with open(post_filename, 'rb') as file:
            bot.send_document(message.chat.id, file, caption="Post ma'lumotlari:")

        os.remove(post_filename)

    except instaloader.exceptions.ProfileNotExistsException:
        bot.reply_to(message, "Bu username bilan profil topilmadi.")
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

@bot.message_handler(commands=['comments'])
def handle_comments(message):
    try:
        username = message.text.split()[1]
        profile = instaloader.Profile.from_username(L.context, username)
        posts = profile.get_posts()

        for i in range(5):
            try:
                post = next(posts)
                comments = post.get_comments()

                file_name = f'{username}_post_{i + 1}_comments.txt'
                with open(file_name, 'w', encoding='utf-8') as f:
                    for comment in comments:
                        f.write(f"{comment.owner.username}: {comment.text}\n")

                with open(file_name, 'rb') as f:
                    bot.send_document(message.chat.id, f)

                os.remove(file_name)

            except StopIteration:
                bot.send_message(message.chat.id, "No more posts available.")
                break
            except Exception as e:
                bot.send_message(message.chat.id, f"Error fetching comments for post {i + 1}: {e}")
                break

        bot.send_message(message.chat.id, "Finished fetching comments.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
