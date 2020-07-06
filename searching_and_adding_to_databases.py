import os
import sqlite3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
from io import BytesIO

def search_and_create_database():
	print(os.listdir("resources"))
	if "album_arts" not in os.listdir("resources"):
		os.makedirs("resources/album_arts")
	conn = sqlite3.connect(os.path.join("resources",'data.db'))
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS songs (song_name text,song_path text, art_path text,song_len text)''')  	
	for folderName, subfolders, filenames in os.walk('/home'):
		for filename in filenames:
			if filename.endswith(".mp3"):
				c.execute('''SELECT song_name FROM songs WHERE song_name=?''',(filename,))
				exists = c.fetchall()
				
				sp=os.path.join(folderName,filename)
				ap=os.path.join("resources","default_album_art.jpg")
				if not exists :
					track=MP3(os.path.join(folderName,filename))				
					tags = ID3(os.path.join(folderName,filename))
					sl=track.info.length
					if sl<=15:
						continue
					if "APIC" in tags.pprint():
						pict = tags.get("APIC:").data
						im = Image.open(BytesIO(pict))
						im=im.resize((250,250))
						pic_name=filename.replace(".mp3",".jpg")
						im=im.save(os.path.join("resources","album_arts",pic_name))
						ap=os.path.join("resources","album_arts",pic_name)
					c.execute('INSERT INTO songs VALUES (?,?,?,?)',(filename,sp,ap,str(sl)))
					conn.commit()

# search_and_create_database()