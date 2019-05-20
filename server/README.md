### Server & Client
+ Requirements:
    + Virtual Environment (optional, recommended)
    + python3 (Python3.6 - recommended)
    + pip3
    + Camera:
        + Laptop: Webcam
        + Android: __IP Webcam__ app (recommended)
        + iOs: __IP Webcam__ app
        
+ Installation:
    ```
    $ pip3 install -r requirements.txt
    ```
    
+ Run:
    + if using Laptop Webcam, in function _generate_frame()_ of _app.py_, comment all lines in _external camera app_ part
    + if using external camera, comment all lines in _webcam_ part. Camera app must be __in the same private network__ with Server. __camera_ip__ must appear on the screen when open app:
        + Android: Open App -> Roll Down to the bottom -> Click "Start Server"
        + iOS: Open App -> Click "Camera" (ignore the port on screen, 8080 still)
    + execute:
        ```
        $ python app.py
        ```
    
+ Usage:
    + Access to http://localhost (according to configuration in app.py)
    + Enter robot id
    + Choose either __Auto Mode__ or __Manual Mode__
        + Auto Mode:
            + Enter RobotID
            + Enter Starting Point - the initial point of robot
            + Enter Head Point - the point right in front of robot. In other word, the init direction of robot is starting point -> head point.
                + For example: Starting Point (0, 1) and Head Point (0, 2)
            + Enter Target Point - the destination point that robot go to and pick an object.
            + Click "Submit"
        + Manual Mode:
            + Type Robot ID
            + Enter Starting Point and Heading Point
            + Click "Submit"
            + Control robot using action buttons