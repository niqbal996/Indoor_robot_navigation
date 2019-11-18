# Indoor robot navigation
The robot scans the room for door archways and locks onto that to exit the room autonomously. The robot functions using object detection approach with a basic LeNet model on 480p SD resolution images.  

A short demo of trained model tracking and moving toward door. The images of the door were provided as training data to the model. 
[![Watch the video](https://i.imgur.com/wNWqVa1.png)](https://www.youtube.com/watch?v=ekJgOvNMv5E)

## Installation and hardware
* If you are using the Roomba vacuum cleaner as a robot, then you need to make a [serial interface](https://makezine.com/2008/02/29/how-to-make-a-roomba-seri/) for communicating with Raspberry PI. 
* Install tensorflow and python3 on Raspberry Pi. 

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

## TODO
* Use 

## License
Can be used for educational purposes only with permission. 

## Acknowledgements
* A small project done under the supervision of [Prof. Dr.-Ing. Gerald Schuller](https://www.tu-ilmenau.de/mt-ams/personen/schuller-gerald/)
* The image detection model from [Adrian Rosebrock](https://www.pyimagesearch.com/) was extended for a video stream and combined with a raspberry Pi Roomba robot. 
