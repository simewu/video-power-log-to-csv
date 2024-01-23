import os
import re
import sys
from moviepy.editor import VideoFileClip

def main():
	fileName = selectFile(r'.*', False)

	# Check if the file is a video
	if fileName and fileName.endswith(('.mp4', '.mov', '.avi')):
		audio_file = os.path.splitext(fileName)[0] + '.wav'  # Using .wav for better compatibility
		try:
			extractAudio(fileName, audio_file)
		except Exception as e:
			print(f'Error processing file {fileName}: {e}')
			sys.exit(1)
	else:
		audio_file = fileName

# Given a regular expression, list the files that match it, and ask for user input
def selectFile(regex, subdirs = False):
	files = []
	if subdirs:
		for (dirpath, dirnames, filenames) in os.walk('.'):
			for file in filenames:
				path = os.path.join(dirpath, file)
				if path[:2] == '.\\': path = path[2:]
				if bool(re.match(regex, path)):
					files.append(path)
	else:
		for file in os.listdir(os.curdir):
			if os.path.isfile(file) and bool(re.match(regex, file)):
				files.append(file)
	
	print()
	if len(files) == 0:
		print(f'No files were found that match '{regex}'')
		print()
		return ''

	print('List of files:')
	for i, file in enumerate(files):
		print(f'  File {i + 1}  -  {file}')
	print()

	selection = None
	while selection is None:
		try:
			i = int(input(f'Please select a file (1 to {len(files)}): '))
		except KeyboardInterrupt:
			sys.exit()
		except:
			pass
		if i > 0 and i <= len(files):
			selection = files[i - 1]
	print()
	return selection

def extractAudio(video_file, audio_file):
	# video = VideoFileClip(video_file)
	# video.audio.write_audiofile(audio_file)
	try:
		video = VideoFileClip(video_file)
		video.audio.write_audiofile(audio_file, codec='pcm_s16le') # Codec for .wav format
	except Exception as e:
		raise Exception(f'Failed to extract audio: {e}')

if __name __ == '__main__':
	main()
	print('Done.')