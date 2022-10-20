echo "Be sure to install tesseract from:"
echo "https://github.com/UB-Mannheim/tesseract/wiki"
python3 -m pip install pytesseract

python3 step2_frames_to_readtext.py
echo "DONE"
PAUSE