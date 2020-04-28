


import csv
import urllib.request
import urllib.parse
import re
import time
file = open('billboard_lyrics_1964-2015.csv','r', encoding='utf-8', errors='surrogateescape')
lyricinfo = list(csv.DictReader(file ,delimiter=','))
#This imports the csv and preps it for being read and also preps the youtube URL request stuff
max_list_len = 30

#Important Variables Go Here
def youtube_url(i):
    query_string = urllib.parse.urlencode({"search_query" : lyricinfo[i]['Song'].title()})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    youtube_url_searched = "http://www.youtube.com/watch?v=" + search_results[0]
    print("You can listen to this song by using this url: "+youtube_url_searched)
# This is for searching the url of "i", which is the song position in the list.

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#This is for formatting text. I didn't write this.

def lyric_locate_beta():
    print("This program will help you locate songs that were on the Billboard Hot 100 from 1965-2015, based on a phrase in the lyrics or individual words present in the lyrics,")
    print("and will produce the full title, the artist, the rank of the song, what year it achieved that rank, and a url that links to the song on YouTube.")
    time.sleep(2)
    print("You can search by words or phrases. This program returns a maximum of",max_list_len,"songs.")
    print("If your think your phrase is too common in songs, you should search the words individually instead.")
    time.sleep(1)
    lyric_word_list = []
    lyric_quest = ""
    while lyric_quest != "1" or "2":
        lyric_quest = input("Do you want to search a [1]phrase or [2]words?")
        break
    if lyric_quest == "1":
        lyric_phrase = input("What is the phrase from the lyrics of the song you are searching for?").lower()
        song_pos_phrase = [lyricinfo.index(i) for i in lyricinfo if lyric_phrase in i['Lyrics']]
        print("These songs have '"+lyric_phrase.title()+"' in their lyrics:")
        if lyric_phrase != "" and len(song_pos_phrase) <= max_list_len:
            n = 1
            for i in song_pos_phrase:
                print(str(n)+". "+color.BOLD+lyricinfo[i]['Song'].title()+color.END+" performed by "+lyricinfo[i]['Artist'].title()+", which was ranked #"+lyricinfo[i]['Rank']+" in "+lyricinfo[i]['Year']+ " on the Billboard Hot 100.")
                n += 1
                youtube_url(i)
        if len(song_pos_phrase) == 0:
            print("There are no songs with this phrase in their lyrics")
        if lyric_phrase == "":
            print("You did not enter a phrase, please try again and follow the directions!")
        elif len(song_pos_phrase) > max_list_len:
            print("Your phrase is too common. It appears in "+str(len(song_pos_phrase))+" songs. Please try again with a different phrase.")
#Pt. A works to my knowledge mostly flawlessly. Cant get the while statement to work without the break.
#Problems with Pt B: combines words into phrases instead of searching each word and then matching. Depends on the order of the words. Needs to search lyrics, return lyrics to an internal reference and then search again with each additional word.
    if lyric_quest == "2":
        x = 0
        lyric_word_response = ""
        lyric_word_string = ""
        lyric_word_phrase = ""
        while lyric_word_response != "Y" and lyric_word_list != "":
            lyric_word = ""
            lyric_word = input("What is one word in the lyrics of the song you are looking for?").lower()
            lyric_word_list.append(lyric_word)
            lyric_word_response = input("Is '"+lyric_word+"' the word you want to search? [Y]Yes or [N]No?")
            if lyric_word_response == "N":
                print(lyric_word+" has been removed from your search. If this was a mistake, you may safely enter the word again.")
                lyric_word_list.remove(lyric_word)
        filtered_lyricinfo = [s for s in lyricinfo if lyric_word_list[0] in s['Lyrics']]
        length_words = len(filtered_lyricinfo)
#This correctly fetches the songs with the first word in the list
        while length_words >= max_list_len:
            lyric_word_response = ""
            print("Your chosen word occurs in "+str(length_words)+" songs. Please add more words")
            x += 1
            while lyric_word_response != "Y":
                lyric_word = ""
                lyric_word = input("What is another word in the lyrics of the song you are looking for?").lower()
                lyric_word_list.append(lyric_word)
                lyric_word_response = input("Is '"+lyric_word+"' the word you want to search? [Y]Yes or [N]No?")
                if lyric_word_response == "N":
                    print(lyric_word+" has been removed from your search. If this was a mistake, you may safely enter the word again.")
                    lyric_word_list.remove(lyric_word)
            j = 0
            while j < len(filtered_lyricinfo):
                song_pos_var1 = filtered_lyricinfo[j]
                filtered_lyricinfo = [s for s in filtered_lyricinfo if lyric_word_list[x] in s['Lyrics']]
                j += 1
            length_words = len(filtered_lyricinfo)
        song_pos_words = [lyricinfo.index(i) for i in filtered_lyricinfo if lyric_word_list[x] in i['Lyrics']]
        print("These songs have the words "+str(lyric_word_list)+" in their lyrics:")
        if length_words <= max_list_len and length_words > 0:
            n = 1
            for i in song_pos_words:
                print(str(n)+". "+color.BOLD+lyricinfo[i]['Song'].title()+color.END+" performed by "+lyricinfo[i]['Artist'].title()+", which was ranked #"+lyricinfo[i]['Rank']+" in "+lyricinfo[i]['Year']+ " on the Billboard Hot 100.")
                n += 1
                youtube_url(i)
        if length_words == 0:
            print("There are no songs with the words"+str(lyric_word_list)+"in their lyrics")


if __name__ == '__main__':
    lyric_locate_beta()
