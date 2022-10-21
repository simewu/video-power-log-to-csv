@ECHO OFF

echo "**********************************************************************"
echo "Starting step 1"
python3 -m pip install opencv-python
python3 step1_video_to_frames.py video.mp4 frames --rotate=180
echo "Finished step 1"

echo "**********************************************************************"
echo "Starting step 2"
echo "Be sure to install tesseract from:"
echo "https://github.com/UB-Mannheim/tesseract/wiki"
python3 -m pip install pytesseract
python3 step2_frames_to_readtext.py
echo "Finished step 2"

echo "**********************************************************************"
echo "Starting step 3"
python3 step3_readtext_to_csv.py
echo "Finished step 3"

echo "**********************************************************************"
echo "Starting step 4"
python3 step4_cleanup_output_file.py
echo "Finished step 4"

PAUSE