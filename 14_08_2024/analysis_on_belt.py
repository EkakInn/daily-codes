import cv2
import hashlib


video_path = '/home/ubuntu/Try_code/camera_ip_101/videos/camera_ip_101_2 - Made with Clipchamp.mp4'

cap =cv2.VideoCapture(video_path)
previous_hash_value = 0
while True :
    ret,frame = cap.read()
    # Step 1: Read the image
    # image = cv2.imread('/home/ubuntu/Try_code/camera_ip_101/frames/camera_belt_101.jpg')


    # Step 2: Convert the image to bytes
    # Optional: Resize or preprocess the image if needed
    if not ret :
        break

    frame = frame[366:1339,1243:2480]

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image_bytes = image.tobytes()

    # Step 3: Create a hash object using SHA-256
    hash_object = hashlib.sha256(image_bytes)

    # Step 4: Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()
    hash_decimal = hash_hex * 16

    if previous_hash_value == hash_decimal:
        print("hash_decimal :",hash_decimal)
        print("previous_hash_value : ", previous_hash_value)
    
    previous_hash_value = hash_hex
    # print(f"SHA-256 Hash of the image: {hash_hex}")
    

# belt_image_hash_value = 025c0351991bb72fad160dea552a161b051e611c1225ce18963a54cc212de31a

# a1ebba67d58287add77671118b1511f76c0325ccfcc4e9317da4435aff89523e
