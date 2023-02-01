the script should be in the same folder as the images and labels folder . i.e the script should have  the same hierarchy as the images and label folder
.
├── file_train_test_split.py
├── images
├── labels


copy the images you wish to anotate into the  images folder and their corresponding label into the labels folder 

then run the file_train_test_split.py

it would create automatically the train and val folder with their respective images and label folder with the files  placed accordingly.

By default 1 of every 5 files copied into train  is picked and copied into the val path. 
