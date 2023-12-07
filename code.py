import glob
import os
import random
import pathlib


Path_Till_Folder="/Autovid"
OP_path="Autovid/output/"



# This function randomaly remane all files in a folder
def Randomly_Name_All_Folder_Files(loc_in_program):
	os.chdir(''+Path_Till_Folder+loc_in_program)
	#print(os.getcwd())	 
	for count, f in enumerate(os.listdir()):
		count_name = random.randint(1,1000000)
		f_name, f_ext = os.path.splitext(f)
		f_name = "az" + str(count_name)
		new_name = f'{f_name}{f_ext}'
		os.rename(f, new_name)


def Concatenate_Avi(vidlength):


	loc=Path_Till_Folder+"/media"
	os.chdir(loc)
	os.system("""for %i in (*.avi) do echo file '%i'>> mylist.txt""")

	os.chdir(loc)
	con_avi="ffmpeg -f concat -safe 0 -i mylist.txt -copytb 1 -c copy " + vidlength + " -y "+ OP_path +"output.avi"
	os.system(con_avi)
	os.system("del /f mylist.txt")
	os.chdir(Path_Till_Folder)



# Add audio to video (this will replace audio file to current video audio file)
def Add_Audio_To_Video():
	old_op_file=''+Path_Till_Folder+'/output/output.avi'
	audio_loc=''+Path_Till_Folder+'/input/audio.mp3'
	command = "ffmpeg -i "+ old_op_file +" -i "+ audio_loc +" -map 0:v -map 1:a -c:v copy -shortest -y "+OP_path+"output2.avi"
	os.system(command)
	

# Add subtitle to video
def Add_Subtitle_To_Video():
	old_op_file=""+Path_Till_Folder+"/output/output2.avi"
	#subtitle_loc="C//://Users//AZ//Desktop//Autovid//subtitle.srt"
	mypath=Path_Till_Folder+"/input"
	os.chdir(mypath)
	#ffmpeg -i input.mp4 -filter_complex "subtitles=subs.srt:force_style='OutlineColour=&H80000000,BorderStyle=4,Outline=1,Shadow=0,MarginV=20,Fontsize=10,PrimaryColour=&H0000ff&'" output.mp4
	command="ffmpeg -i "+ old_op_file +" -vf subtitles=subtitle.srt -max_muxing_queue_size 4096 -c:v libx264 -c:a libmp3lame -b:a 384K -y "+OP_path+"output.avi"  # Normal Text Filter
	#command="""ffmpeg -i """+ old_op_file +""" -filter_complex "subtitles=subtitle.srt:force_style='OutlineColour=&H80000000,BorderStyle=4,Outline=1,Shadow=0,MarginV=20,Fontsize=18,PrimaryColour=&H00120ff&'" -max_muxing_queue_size 9999 -y """+OP_path+"""output3.mp4""" #style filter
	os.system(command)

	#deleting output2.mp4 video

	os.chdir(OP_path)
	os.system("del /f output2.avi")
	os.chdir(Path_Till_Folder)


def Add_Intro():
	os.chdir(OP_path)
	os.system("""for %i in (*.avi) do echo file '%i'>> mylist.txt""")

	con_avi="ffmpeg -f concat -safe 0 -i mylist.txt -c copy -y "+ OP_path +"output.avi"
	os.system(con_avi)
	os.system("del /f mylist.txt")
	os.chdir(Path_Till_Folder)


#This function concate all files together (old function do not working properly stuck video issue)
def Concatenate(vidlength):

	stringa = "ffmpeg -i \"concat:"
	elenco_video = glob.glob(""+Path_Till_Folder+"/media/*.mp4")
	elenco_file_temp = []
	for f in elenco_video:
		file = "temp" + str(elenco_video.index(f) + 1) + ".ts"
		os.system("ffmpeg -i " + f + " -c copy -bsf:v h264_mp4toannexb -f mpegts " + file)
		elenco_file_temp.append(file)
	#print(elenco_file_temp)
	for f in elenco_file_temp:
		stringa += f
		if elenco_file_temp.index(f) != len(elenco_file_temp)-1:
			stringa += "|"
		else:
			stringa += "\" -c copy  -bsf:a aac_adtstoasc " + vidlength + " -y "+ OP_path +"output.mp4 "
	#print(stringa)
	os.system(stringa)

#This function delete temp files
def Delete_Temp_Files(folder_and_file_type):
	filo=Path_Till_Folder+folder_and_file_type
	elenco_video = glob.glob(filo)
	for f in elenco_video:
		file = "temp" + str(elenco_video.index(f) + 1) + ".ts"
		os.system("del /f " + file)
	print("Temp Files Deleted \n")


if __name__ == "__main__":


	Randomly_Name_All_Folder_Files("/media")
	
																		#	Concatenate("-ss 00:00:00 -to 00:00:20") #Make sure to add 10 extra seconds
	
	Concatenate_Avi("-ss 00:00:00 -to 00:02:50")
	
																		#	Delete_Temp_Files("/media/*.ts") # delete temp files in media folder (Not required any more)
	
	Add_Audio_To_Video()

	Add_Subtitle_To_Video()

	#	Add_Intro()

																		#	Delete_Temp_Files("/output/*.ts") # delete temp files in media folder (Not required any more)


	print("Program Complete! \n")
