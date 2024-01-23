import os
import re
import sys
from google.cloud import speech_v1p1beta1 as speech
import io

def main():
	fileName = selectFile(r'.*', False)

	if fileName:
		if fileName.endswith(('.mp4', '.mov', '.avi')):
			audio_file = os.path.splitext(fileName)[0] + '.wav'
		else:
			audio_file = fileName

		try:
			transcription = transcribeAudio(audio_file)
			script = formatScript(transcription)
			print(script)
		except Exception as e:
			print(f'Error during transcription: {e}')
			sys.exit(1)
	else:
		print('No file selected.')
		sys.exit(1)


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

def transcribeAudio(audio_file):
	client = speech.SpeechClient()

	with io.open(audio_file, 'rb') as audio_file:
		content = audio_file.read()

	audio = speech.RecognitionAudio(content=content)
	config = speech.RecognitionConfig(
		encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=16000,
		language_code='en-US',
		enable_speaker_diarization=True,
		diarization_speaker_count=6,  # Set to a reasonably high number
	)

	try:
		response = client.recognize(config=config, audio=audio)
	except Exception as e:
		raise Exception(f'Google Cloud API error: {e}')

	# Analyzing the speaker tags to determine the actual number of speakers
	speaker_tags = set()
	for result in response.results:
		for word_info in result.alternatives[0].words:
			speaker_tags.add(word_info.speaker_tag)

	print(f'Detected {len(speaker_tags)} speakers in the audio.')

	return response


def formatScript(transcription):
	script = ''
	current_speaker = None
	for result in transcription.results:
		for word_info in result.alternatives[0].words:
			if current_speaker != word_info.speaker_tag:
				script += '\nPerson {}: '.format(word_info.speaker_tag)
				current_speaker = word_info.speaker_tag
			script += word_info.word + ' '
	return script

if __name__ == '__main__':
	main()
	print('Done.')