import json
import boto3
from PIL import Image
from io import BytesIO
import zipfile

INPUT_BUCKET_NAME = "mip-day-source"
OUTPUT_BUCKET_NAME = "mip-day-target"
INPUT_FILE = "input1.jpg"
CONFIDENCE_THRESHOLD = 97.0

OUTPUT_FOLDER = "<YOUR_HANDLE_HERE>"


def lambda_handler(event, context):
    
    s3 = boto3.resource('s3')

    # create buckets
    input_bucket = s3.Bucket(INPUT_BUCKET_NAME)
    output_bucket = s3.Bucket(OUTPUT_BUCKET_NAME)

    # load input1.jpg from S3 storage
    picture_stream = input_bucket.Object(INPUT_FILE).get()['Body']
    image = Image.open(picture_stream)

    # save image to RAM
    buffer = BytesIO()
    image.save(buffer, "PNG")
    buffer.seek(0)
        
    # save input2.jpg from RAM to output_bucket
    output_bucket.put_object(Key=OUTPUT_FOLDER + "/" + "input2.png", Body=buffer)

    return {
        "status": 200,
        #"categories": None,
        #"numCategories": 0,
        #"numFaces": 0,
        #"output_location": OUTPUT_BUCKET_NAME + "/" + OUTPUT_FOLDER + ".zip",
    }
    
    
def process_detected_faces(face_detection_response, image):
    """
    Processes the detected faces, by
    (1) cropping them in memory
    (2) and writing them to a zip buffer
    :param face_detection_response: the response of aws rekognition
    :param image: the original image to be cropped
    :return: a tuple containing: the zip buffer of all cropped images, the emotions detected in the images and the number of images
    """
    image_width, image_height = image.size
    emotion_set = set()
    zip_buffer = BytesIO()
    counter = 0

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for faceDetail in face_detection_response['FaceDetails']:
            confidence = faceDetail['Confidence']
            if float(confidence) >= CONFIDENCE_THRESHOLD:
                counter = counter + 1
                emotion = faceDetail['Emotions'][0]['Type']
                emotion_set.add(emotion)

                box = calculate_cropping_box(faceDetail, image_width, image_height)
                cropped_image = image.crop(box)

                cropped_buffer = BytesIO()
                cropped_image.save(cropped_buffer, "PNG")
                cropped_buffer.seek(0)

                zip_file.writestr(emotion + "/cropped_" + str(counter) + ".png", cropped_buffer.read())
    zip_buffer.seek(0)
    return zip_buffer, list(emotion_set), counter


def calculate_cropping_box(face_detail, image_width, image_height):
    """
    Calculation from https://blog.devgenius.io/facial-emotion-detection-using-aws-rekognition-in-python-69b2da668192
    :param face_detail: face_detail returned from aws recognition
    :param image_width: width of input image
    :param image_height: height of input image
    :return: box with values for cropping the recognized face
    """
    box_width = face_detail['BoundingBox']['Width']
    box_height = face_detail['BoundingBox']['Height']
    box_left = face_detail['BoundingBox']['Left']
    box_top = face_detail['BoundingBox']['Top']

    width = image_width * box_width
    height = image_height * box_height
    left = image_width * box_left
    top = image_height * box_top

    left = int(left)
    top = int(top)
    width = int(width) + left
    height = int(height) + top

    box = (left, top, width, height)

    return box