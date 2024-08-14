import cv2
import hashlib
# import imagehash


video_path = '/home/ubuntu/Try_code/camera_ip_101/videos/camera_ip_101_2 - Made with Clipchamp.mp4'

cap =cv2.VideoCapture(video_path)

Frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
Frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps)


previous_hash_value= 0

frame_Number=0
while True :
    ret,frame = cap.read()
    frame_Number+=1
    # Step 1: Read the image
    # image = cv2.imread('/home/ubuntu/Try_code/camera_ip_101/frames/camera_belt_101.jpg')


    # Step 2: Convert the image to bytes
    # Optional: Resize or preprocess the image if needed
    if not ret :
        break
     
    if frame_Number % (int(frame_interval/2))==0:
        frame = frame[366:1339,1243:2480]

        # hash1 = imagehash.average_hash(frame)
        
        # if hash1 == hash2:
        #     print("Belt off")

        # hash2=hash1


        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        image_bytes = image.tobytes()

        # Step 3: Create a hash object using SHA-256
        hash_object = hashlib.sha256(image_bytes)

        # Step 4: Get the hexadecimal representation of the hash
        hash_hex = hash_object.hexdigest()
        decimal_value = int(hash_hex, 16)

        if decimal_value == previous_hash_value:
            print("Belt off")

        
        previous_hash_value = decimal_value




cap.release()
