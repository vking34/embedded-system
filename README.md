### Requirement

* python3
* pip3

### Design Document
[link here]()

### Server - Client

You can run server - client in ```server``` folder:

* Install packages:

```
$ pip3 install -r requirements
```

* Modify the ```host``` variable in ```server.py``` and ```templates/index.html``` based on server's network ip address (use ```ifconfig``` to determine)

* Run server-client:

```
$ python server.py
```


### Robot

You can run robot in ```robot``` folder:

* Install packages:

```
$ pip3 install -r requirements
```

* Modify the ```host``` variable in ```robot.py```  based on server's network ip address (use ```ifconfig``` to determine)

* Run robot: There are two option to run robot, fake robot (use for your computer) or real robot (use for lego ev3). By this way, we can create many virtual robots as we want:
```
// Run fake robot, please change the robot_id (for example: robot01)
$ python robot.py robot_id fake

// Run real robot, please change the robot_id (for example: robot02)
$ python robot.py robot_id real
```

*Notify*: The robot_id is unique

### Todo

* Update robot's direction, x position, y position after each manual controlling
* Auto controlling robot
* Camera - Server - Client