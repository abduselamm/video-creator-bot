import telebot # telebot
import pandas as pd
import googletrans
from googletrans import Translator
import gtts
from playsound import playsound
from moviepy.editor import *
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
# States storage
from telebot.storage import StateMemoryStorage
from moviepy.editor import *
import cv2
import os
import moviepy.editor as mpe

# Starting from version 4.4.0+, we support storages.
# StateRedisStorage -> Redis-based storage.
# StatePickleStorage -> Pickle-based storage.
# For redis, you will need to install redis.
# Pass host, db, password, or anything else,
# if you need to change config for redis.
# Pickle requires path. Default path is in folder .state-saves.
# If you were using older version of pytba for pickle, 
# you need to migrate from old pickle to new by using
# StatePickleStorage().convert_old_to_new()



# Now, you can pass storage to bot.
translator = Translator()
state_storage = StateMemoryStorage() # you can init here another storage

language ={'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic', 'hy': 'Armenian', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'hi': 'Hindi', 'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'km': 'Khmer', 'ko': 'Korean', 'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 
'Marathi', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sr': 'Serbian', 'si': 'Sinhala', 'sk': 'Slovak', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'cy': 'Welsh', 'zh-cn': 'Chinese (Mandarin/China)', 'zh-tw': 'Chinese (Mandarin/Taiwan)', 'en-us': 'English (US)', 'en-ca': 'English (Canada)', 'en-uk': 'English (UK)', 'en-gb': 'English (UK)', 'en-au': 'English (Australia)', 'en-gh': 'English (Ghana)', 'en-in': 'English (India)', 'en-ie': 'English (Ireland)', 'en-nz': 'English (New Zealand)', 'en-ng': 'English (Nigeria)', 'en-ph': 'English (Philippines)', 'en-za': 'English (South Africa)', 'en-tz': 'English (Tanzania)', 'fr-ca': 'French (Canada)', 'fr-fr': 'French (France)', 'pt-br': 'Portuguese (Brazil)', 'pt-pt': 'Portuguese (Portugal)', 'es-es': 'Spanish (Spain)', 'es-us': 'Spanish (United States)'}
lang_list=list(language.keys())



bot = telebot.TeleBot("5672449214:AAFsLKNTRBgDShGmpFMSbsxgk0mmsB905VM",
state_storage=state_storage)


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    csv = State() # creating instances of State class is enough from now
    language = State()
    background_image = State()
    background_sound=State()
    delay_time=State()





def inlinebutton():
    markup = InlineKeyboardMarkup()
    markup.width =3
    for j in range(0,len(lang_list),3):
        markup.add(
                    InlineKeyboardButton(language[lang_list[j]],callback_data=lang_list[j]),
                    InlineKeyboardButton(language[lang_list[j+1]],callback_data=lang_list[j+1]),
                    InlineKeyboardButton(language[lang_list[j+2]],callback_data=lang_list[j+2]),
                    )
    return markup 
@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.csv, message.chat.id)

    bot.send_message(message.chat.id, 'please upload a csv file')
 

# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(state=MyStates.csv)
@bot.message_handler(content_types=['document']) # list relevant content types
def addfile(message):
    #print(message)
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.set_state(message.from_user.id, MyStates.language, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['csv'] = file_name
    bot.send_message(message.from_user.id,text="please enter language",reply_markup=inlinebutton())


@bot.callback_query_handler(func=lambda m : True)
def language_query(message):
    bot.send_message(message.from_user.id, "please upload image")
    bot.set_state(message.from_user.id, MyStates.background_image, message.from_user.id)
    with bot.retrieve_data(message.from_user.id, message.from_user.id) as data:
        data['language'] = message.data
@bot.message_handler(state=MyStates.background_image)
@bot.message_handler(content_types= ["photo"])
def uploadImage(message):
    #print("myfoto",message)
    file_name = "img.jpg"
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.set_state(message.from_user.id, MyStates.background_sound, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['background_image'] = file_name
    bot.send_message(message.from_user.id,text="Upload background sound")


@bot.message_handler(state=MyStates.background_sound)
@bot.message_handler(content_types=['audio']) # list relevant content types
def uploadSound(message):
    #print(message)
    file_name = message.audio.file_name
    print("my file name ",file_name)
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.set_state(message.from_user.id, MyStates.delay_time, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['background_sound'] = file_name
    bot.send_message(message.from_user.id,text="enter delay time ")

def add_static_image_to_audio(image_path, audio_path, output_path):
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 1
    video_clip.write_videofile(output_path)






@bot.message_handler(state=MyStates.delay_time)
def backgroundSound(message):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    bot.send_message(message.chat.id, 'we are proceessing please wait ... ')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['delay_time'] = message.text

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        df=pd.read_csv(data["csv"])
        for i,row in df.iterrows():
            row=row[0]
            text_to_translate = translator.translate(row,src= 'auto',dest=data['language']).text
            print(2)
            anotherlang = gtts.gTTS(text_to_translate, lang=data['language'])
            anotherlang.save("anaudio.mp3")
            print("my row :- ",row[0])
            englishlang= gtts.gTTS(row, lang=data['language'])
            englishlang.save("engaudio.mp3")
            add_static_image_to_audio('img.jpg',"anaudio.mp3",'another.mp4')
            add_static_image_to_audio('img.jpg',"engaudio.mp3",'english.mp4')
            # loading video dsa gfg intro video
            anotherclip = VideoFileClip("another.mp4")    
            durationofanotherclip = anotherclip.duration
            another_txt_clip = TextClip(text_to_translate, fontsize = 20, color = 'white')
            another_txt_clip = another_txt_clip.set_pos('center').set_duration(durationofanotherclip)
            anothervideo = CompositeVideoClip([anotherclip, another_txt_clip])
            anothervideo.write_videofile("anothersubtvid.mp4", fps = 24, codec = 'mpeg4')
            engclip = VideoFileClip("english.mp4") 
            durationofengclip = engclip.duration   
            eng_txt_clip = TextClip(row, fontsize = 20, color = 'white')
            eng_txt_clip = eng_txt_clip.set_pos('center').set_duration(durationofengclip)
            engvideo = CompositeVideoClip([engclip, eng_txt_clip])
            engvideo.write_videofile("engsubtvid.mp4", fps = 24, codec = 'mpeg4')
            clip1 = VideoFileClip("engsubtvid.mp4")
            clip2 = VideoFileClip("anothersubtvid.mp4")
            try:
                clip3= VideoFileClip("bothsubtitledvid"+str(i-1)+".mp4")
                bothlang = concatenate_videoclips([clip1, clip2,clip3])
            except:
                bothlang = concatenate_videoclips([clip1, clip2])

            bothlang.write_videofile("bothsubtitledvid"+str(i)+".mp4", fps = 24, codec = 'mpeg4')
            
            if i==len(df)-1:
                clip = mpe.VideoFileClip("bothsubtitledvid"+str(i)+".mp4")
                duration = clip.duration
                audio_background = mpe.AudioFileClip(data['background_sound']).subclip(0,duration)
                final_audio = mpe.CompositeAudioClip([clip.audio, audio_background])
                final_clip = clip.set_audio(final_audio)
                final_clip.write_videofile("myfinal.mp4", fps = 24, codec = 'mpeg4')
                bot.send_video(chat_id=message.chat.id, video=open("myfinal.mp4", 'rb'), supports_streaming=True)
                os.remove("bothsubtitledvid"+str(i-1)+".mp4")
                #os.remove("myfinal.mp4")

                



            else:
                try:
                    os.remove('"bothsubtitledvid"+str(i-1)+".mp4"')
                except:
                    pass
    #bot.send_video(chat_id=message.chat.id, video=open("bothsubtitledvid"+str(i)+".mp4", 'rb'), supports_streaming=True)
    bot.send_message(chat_id=message.chat.id,text="goood done")
        

 









# result





#incorrect number
@bot.message_handler(state=MyStates.background_image, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for MyStates.age
    """
    bot.send_message(message.chat.id, 'Looks like you are submitting a string in the field age. Please enter a number')

# register filters

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)


#converting an audio to video


#.py directed-by-robert-image.jpg "Directed-by-Robert-B.-Weide-theme.mp3" output.mp4
