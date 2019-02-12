# Door finder robot

Door finder robot turns and scans the room for door images and if it has well trained neural network trained for that room,
it will move towards the door.

## Record training data
1. Record 640*480 resolution videos from the room.
2. Run labelling_tool.py to generate sub frames from it for each video one by one after changing the name of the video in it.
```bash
python labelling_tool.py 
```
3. Organize these images into respective door and notdoor folders.
4. Run sort_dataset.py to remove spaces in filenames and have nice organized dataset. 
```bash
python sort_dataset.py
```

## Training
Train the neural network using the given dataset and generate an output model for the door_scanner.py script.
```bash
python train_network.py -d images -m name_of_output_model.model
```

## Testing
Finally from the model from the above script we can start the script and let the robot roam. 
```bash
sudo python door_scanner.py -m name_of_output_model.model
```
NOTE: I ran it in sudo mode to make sure the Pi gives it access to its ports for serial interface communication with the Roomba. 

## License
Can be used for educational purposes only with permission. 

## Credits
[Prof. Dr.-Ing. Gerald Schuller](https://www.tu-ilmenau.de/mt-ams/personen/schuller-gerald/)
[Adrian Rosebrock](https://www.pyimagesearch.com/)
