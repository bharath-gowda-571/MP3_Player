import pyglet
import os
from searching_and_adding_to_databases import search_and_create_database
import sqlite3
import shutil

window=pyglet.window.Window(500,500)

icon1=pyglet.image.load(os.path.join("resources","icons","mp3_16x16.png"))
icon2=pyglet.image.load(os.path.join("resources","icons","mp3_32x32.png"))

window.set_caption("MP3 Player")
window.set_icon(icon1,icon2)


background=pyglet.image.load(os.path.join("resources","background.jpg"))

pause=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","pause.png")),x=208,y=37)

play=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","play.png")),x=208,y=37)

next_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","next.png")),x=310,y=50)

back_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","back.png")),x=130,y=50)

forward_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","forward.png")),x=400,y=50)

rewind_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","rewind.png")),x=40,y=50)

plus_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","plus.png")),x=425,y=290)

minus_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","minus.png")),x=425,y=250)

refresh_button=pyglet.sprite.Sprite(pyglet.image.load(os.path.join("resources","refresh.png")),x=45,y=115)

pause_or_play=[pause,play]
pause_or_play_count=0
if "data.db" not in os.listdir("resources"):
	search_and_create_database()
conn=sqlite3.connect(os.path.join("resources","data.db"))
c=conn.cursor()
c.execute("""SELECT * FROM songs""")
songs=c.fetchall()


def reload_songs():
	global player,conn,songs,songs_loaded,song_time,label,number_of_songs,current_art
	conn.close()
	shutil.rmtree(os.path.join("resources","album_arts"))
	os.remove(os.path.join("resources","data.db"))
	player.pause()
	player=pyglet.media.Player()
	search_and_create_database()
	conn=sqlite3.connect(os.path.join("resources","data.db"))
	c=conn.cursor()
	c.execute("""SELECT * FROM songs""")
	songs=c.fetchall()
	songs_loaded=[pyglet.media.load(i,streaming=False) for i in list(zip(*songs))[1]]
	player.queue(songs_loaded)
	song_index=0
	current_art=pyglet.image.load(songs[0][2])

	number_of_songs=len(songs)
	label = pyglet.text.Label(songs[0][0].replace(".mp3",""),
							  font_name="Times New Roman",
	                          font_size=20,
	                          x=250, y=175,
	                          anchor_x='center', anchor_y='center',color=(0,0,0,255))
	song_time=str(int(float(songs[0][3]))//60)+":"+str(int(float(songs[0][3]))%60).rjust(2,"0")

	player.play()

song_index=0

player=pyglet.media.Player()

try:
	songs_loaded=[pyglet.media.load(i,streaming=False) for i in list(zip(*songs))[1]]
	player.queue(songs_loaded)
	current_art=pyglet.image.load(songs[0][2])

	number_of_songs=len(songs)

	label = pyglet.text.Label(songs[0][0].replace(".mp3",""),
						  font_name="Times New Roman",
                          font_size=20,
                          x=250, y=175,
                          anchor_x='center', anchor_y='center',color=(0,0,0,255))
	song_time=str(int(float(songs[0][3]))//60)+":"+str(int(float(songs[0][3]))%60).rjust(2,"0")

	player.play()

except :
	reload_songs()



@window.event
def on_draw():
	window.clear()
	background.blit(0,0)
	pause_or_play[pause_or_play_count%2].draw()
	next_button.draw()
	back_button.draw()
	forward_button.draw()
	rewind_button.draw()
	current_art.blit(125,225)
	label.draw()
	refresh_button.draw()
	current_time=str(int(player.time)//60)+":"+str(int(player.time)%60).rjust(2,"0")
	time_label=pyglet.text.Label(current_time+"/"+song_time,
									font_name="Times New Roman",
                          			font_size=15,
                          			x=420, y=140,
                          			anchor_x='center', anchor_y='center',color=(0,0,0,255))
	time_label.draw()
	plus_button.draw()
	minus_button.draw()
	volume_label=pyglet.text.Label(str(int(player.volume*10)).rjust(2,"0")+"/10",
									font_name="Times New Roman",
                          			font_size=13,
                          			x=440, y=340,
                          			anchor_x='center', anchor_y='center',color=(0,0,0,255))
	volume_label.draw()

@window.event
def on_key_press(symbol,modifiers):
	global pause_or_play_count
	if symbol==pyglet.window.key.SPACE:
		pause_or_play_count+=1
		if pause_or_play_count%2:
			player.pause()
		else:
			player.play()
		on_draw()
	if symbol==pyglet.window.key.UP:
		if player.volume+0.1<=1:
			player.volume+=0.1

	if symbol==pyglet.window.key.DOWN:
		if player.volume-0.1>=0:
			player.volume-=0.1

	if symbol==pyglet.window.key.LEFT:
		player.seek(player.time-10)

	if symbol==pyglet.window.key.RIGHT:
		player.seek(player.time+10)

@player.event
def on_eos():
	global song_index,current_art,label,song_time,number_of_songs
	song_index+=1
	current_art=pyglet.image.load(songs[song_index%number_of_songs][2])
	label = pyglet.text.Label(songs[song_index%number_of_songs][0].replace(".mp3",""),
						  font_name="Times New Roman",
                          font_size=20,
                          x=250, y=175,
                          anchor_x='center', anchor_y='center',color=(0,0,0,255))
	song_time=str(int(float(songs[song_index%number_of_songs][3]))//60)+":"+str(int(float(songs[song_index%number_of_songs][3]))%60).rjust(2,"0")


@player.event
def on_player_eos():
	player.queue(songs_loaded)
	player.play()

@window.event
def on_mouse_press(x, y, button, modifiers):
	global pause_or_play_count,player,song_index,current_art,song_time,label,number_of_songs
	if 130<x<180 and 50<y<100:
		player.pause()
		player.delete()
		player=pyglet.media.Player()
		if song_index-1>=0:
			song_index-=1
		player.queue(songs_loaded[song_index%number_of_songs:])
		player.play()
		current_art=pyglet.image.load(songs[song_index%number_of_songs][2])
		label = pyglet.text.Label(songs[song_index%number_of_songs][0].replace(".mp3",""),
							  font_name="Times New Roman",
	                          font_size=20,
	       	                  x=250, y=175,
	                          anchor_x='center', anchor_y='center',color=(0,0,0,255))
		song_time=str(int(float(songs[song_index%number_of_songs][3]))//60)+":"+str(int(float(songs[song_index%number_of_songs][3]))%60).rjust(2,"0")

	if 207<x<283 and 37<y<112:
		pause_or_play_count+=1
		if pause_or_play_count%2:
			player.pause()
		else:
			player.play()
		on_draw()

	if 310<x<360 and 50<y<100:
		player.next_source()
		on_eos()
	
	if 400<x<450 and 50<y<100:
		player.seek(player.time+10)
	
	if 40<x<90 and 50<y<100:
		player.seek(player.time-10)

	if 425<x<450 and 290<y<315:#plus
		if player.volume+0.1<=1:
			player.volume+=0.1

	if 425<x<450 and 250<y<275:# minus
		if player.volume-0.1>=0:
			player.volume-=0.1
		
	if 45<x<85 and 115<y<155:
		reload_songs()

pyglet.app.run()