import cv2
cap = cv2.VideoCapture('Can_You_See_It.mp4')
while cap.isOpened():
    for i in range(1438): # range of black pixels when i exported all the frams using ffmpeg
        ret, frame = cap.read() #Opening CV File for read as Shown at CV2 Toturials
        if ret: 
            pixel = str(frame[0, 0]) # default to string script found
            is_white = pixel == '[250 253 251]' #when i saw white is not really white i just went to photoshop and pointed on that colour that was the result, lol.
            if pixel == '[95 98 96]': #Photoshop colour detection for GREY
                continue
            else:
                print(int(is_white), end="") #end="" and the line only in the end of the loop. the print underneath is like printing a ("\n")

        else:
            #BASICALLY IF ITS A WHITE PIXEL PRINT 1 IF ITS NOT PRINT 0 - EASY!
            cap.release() #the method for closing the video with opencv2 or else it will be opened and script will keep running, although flag is fully printed.
            break
    print("")
