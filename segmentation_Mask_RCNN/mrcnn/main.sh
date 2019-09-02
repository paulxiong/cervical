rm -rf cells/rois/*
rm -rf origin_imgs/*JPG_abc.png
rm -rf ./cells/crop/*
python my_inference.py
python tocsv.py
python tocells.py