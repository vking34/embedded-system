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
    + if using external camera, comment all lines in _webcam_ part
    + execute:
        ```
        $ python app.py
        ```
    
+ Usage:
    + Access to http://localhost (according to configuration in app.py)
    + Enter robot id
    + Choose either __Auto Mode__ or __Manual Mode__
        + Auto Mode:
            + Enter Starting Point - the initial point of robot
            + Enter Head Point - the point right in front of robot. In other word, the init direction of robot is starting point -> head point.
                + For example: Starting Point (0, 1) and Head Point (0, 2)
            + Enter Target Point - the destination point that robot go to and pick an object.
        + Manual Mode:
            + Command robot to do actions according to action list.