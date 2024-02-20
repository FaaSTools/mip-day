# Teil 2

## Schritt 1: Funktion tunen

Standardmäßig haben Lambdas nur sehr wenig Speicher und Laufzeit zur Verfügung.

Gleichzeitig sind nicht alle Abhängigkeiten installiert, die wir für die folgende Übung brauchen.

### Layer hinzufügen

Layers sind packaged Libraries die eine Funktion durch weitere Softwarekomponenten erweitern.

Scrollen Sie zu Layers und fügen Sie einen neuen Layer hinzu. 

Wählen Sie **ARN angeben** und füllen Sie das Feld aus. 

**Achtung! Wählen Sie die richtige ARN aus:**

Gruppe von 11:45 - 12:45
```
arn:aws:lambda:eu-west-3:770693421928:layer:Klayers-p311-Pillow:3
```

Gruppe von 14:30 - 15:30
```
arn:aws:lambda:ca-central-1:770693421928:layer:Klayers-p311-Pillow:3
```

### Mehr RAM, mehr POWER und mehr Zeit

Scrollen Sie hoch und wechseln Sie auf den Tab **Konfiguration**. 
Wählen Sie **Allgemeine Konfiguration**, dann **Bearbeiten**.

Vergeben Sie als Arbeitsspeicher **1024** MB. 

Und erhöhen Sie das Timeout auf **1 Min. 3 Sek.**

**Speichern** Sie die Änderungen.

## Schritt 2: Funktion mit externem Speicher erweitern

Lambdas verlieren nach Ihrem Aufruf Ihren Speicher, bei der nächsten Ausführung ist der Urzustand wiederhergestellt. 
Deshalb müssen wir um Dateien zu speichern Cloud Speicher, wie S3 verwenden.

Ersetzen Sie den Funktionscode mit dem folgenden Snippet:

```python
import json
import boto3
from PIL import Image
from io import BytesIO
import zipfile

INPUT_BUCKET_NAME = "mip-day-source"
OUTPUT_BUCKET_NAME = "mip-day-target"
INPUT_FILE = "input1.jpg"
CONFIDENCE_THRESHOLD = 97.0

OUTPUT_FOLDER = "<YOUR PSEUDONYM>"


def lambda_handler(event, context):
    
    s3 = boto3.resource('s3')

    # create buckets
    input_bucket = s3.Bucket(INPUT_BUCKET_NAME)
    
    # TODO 
    #output_bucket = ...

    # load input1.jpg from S3 storage
    # TODO replace filename
    picture_stream = input_bucket.Object(<filename>).get()['Body']
    image = Image.open(picture_stream)

    # save image to RAM
    buffer = BytesIO()
    image.save(buffer, "PNG")
    buffer.seek(0)
        
    # save input2.jpg from RAM to output_bucket
    output_bucket.put_object(Key=OUTPUT_FOLDER + "/" + "input_copied.png", Body=buffer)

    return {
        "status": 200,
        #"categories": None,
        #"numCategories": 0,
        #"numFaces": 0,
        #"output_location": OUTPUT_BUCKET_NAME + "/" + OUTPUT_FOLDER + ".zip",
    }
```

## Deployen und Ausführen

Öffnen Sie 
[S3 MIP Day Target](https://s3.console.aws.amazon.com/s3/buckets/mip-day-target?region=eu-central-1&bucketType=general&tab=objects)

Navigieren Sie zu Ihrem Ordner, und prüfen Sie ob er die Datei *input_copied.png* enthält.

## Schritt 3: Face Recognition einbauen

Im folgenden sind zwei weitere Funktionen, die Sie bitte **kopieren** und unter die Funktion *lambda_handle* **einfügen**.

Falls Sie im zweiten Schritt Schwierigkeiten hatten, können Sie von [clean_point_second_part.py](clean_point_second_part.py) **ALLES** kopieren und Ihren Code überschreiben. **Vergessen Sie nicht erneut Ihr Pseudonym am Anfang der Datei auszubessern**

```python
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

    # here we open a zipfile
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # for each found face
        for faceDetail in face_detection_response['FaceDetails']:
            confidence = faceDetail['Confidence']
            # if AWS is very sure that this is a face
            if float(confidence) >= CONFIDENCE_THRESHOLD:
                # increase the faces counter
                counter = counter + 1

                # get the emotion of the face and add it to a set
                emotion = faceDetail['Emotions'][0]['Type']
                emotion_set.add(emotion)

                # calculate where the face is
                box = calculate_cropping_box(faceDetail, image_width, image_height)
                # crop the image
                cropped_image = image.crop(box)

                # save the cropped image to RAM
                cropped_buffer = BytesIO()
                cropped_image.save(cropped_buffer, "PNG")
                cropped_buffer.seek(0)

                # write the cropped image to zipfile
                zip_file.writestr(emotion + "/cropped_" + str(counter) + ".png", cropped_buffer.read())
    # reset the buffer
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
    # in the following lines we get the borders of one detected face
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
```

Die Funktionen die Sie kopiert haben, verarbeiten das Ergebnis von AWS Gesichtserkennung. Die Vortragenden studieren mit Ihnen kurz den Code.

Nun müssen wir lediglich unsere *lambda_handler* Funktion anpassen um die gewünschte Funktionalität zu erreichen.

### Recognition Client ergänzen

```python 
# get the recognition client (similar to boto3.resource('s3'))
recognition_client = boto3.client('rekognition', region_name='eu-central-1')
```

### Save Image to RAM ist nicht mehr notwendig

Entfernen Sie die folgenden Zeilen: 

```python
# save image to RAM
buffer = BytesIO()
image.save(buffer, "PNG")
buffer.seek(0)
```

### Rufen Sie Face-Detection auf

```python
    # insert after image = Image.open(picture_stream)


    # this calls AWS service to detect faces
    response = recognition_client.detect_faces(Image={'S3Object': {'Bucket': INPUT_BUCKET_NAME, 'Name': INPUT_FILE}},
                                               Attributes=['ALL'])

    # this line crops the image and creates a zip
    zip_buffer, emotions, number_of_images = process_detected_faces(response, image)
```

### Speichern Sie das ZIP

```python
# replace the previous save of the png file, we copied
output_bucket.put_object(Key=OUTPUT_FOLDER + ".zip", Body=zip_buffer)
```

### Entfernen Sie die Kommentarmarker vom Return 

```python
    return {
        "status": 200,
        "categories": emotions,
        "numCategories": len(emotions),
        "numFaces": number_of_images,
        "output_location": OUTPUT_BUCKET_NAME + "/" + OUTPUT_FOLDER + ".zip",
    }
```

### Deployen und Testen

Erwartete Ausgabe

```
Response
{
  "status": 200,
  "categories": [
    "CALM",
    "HAPPY"
  ],
  "numCategories": 2,
  "numFaces": 7,
  "output_location": "mip-day-target/<YOUR_HANDLE_HERE>.zip"
}
```

Prüfen Sie ob sich im S3 Ordner eine Zipdatei mit ihrem Pseudonym befindet und laden Sie diese herunter um das Ergebnis zu prüfen.