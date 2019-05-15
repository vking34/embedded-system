### Robot
+ Requirements:
    + python3 (Python3.6 - recommended)
    + pip3
    
+ Installation:
    ```
    $ pip3 install -r requirements.txt
    ```

+ Run:
    + Modify the ```host``` variable in ```robot.py```  based on server's network ip address (use ```ifconfig``` to determine)
    * Run robot: There are two option to run robot, fake robot (use for your computer) or real robot (use for lego ev3). By this way, we can create many virtual robots as we want:
        ```
        // Run fake robot, please change the robot_id (for example: robot01)
        $ python robot.py robot_id fake
        
        // Run real robot, please change the robot_id (for example: robot02)
        $ python robot.py robot_id real
        ```

    + Notify: The robot_id is unique