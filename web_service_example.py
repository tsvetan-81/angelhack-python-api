
# Now you can import your module
#from face_recognition import face_recognition
# Or just
import face_recognition
from flask import Flask, jsonify, request, redirect, Response
import json
from flask_cors import CORS

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

test_image = face_recognition.load_image_file("test.jpg")
test_face_encoding = face_recognition.face_encodings(test_image)[0]
known_face_encodings = [
    test_face_encoding
]

known_face_names = [
    "FirstName FamilyName"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    print("test")
    print(request.method)
    if request.method == 'POST':
        print("POST method")
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        print("POST method")
        print(request.files)
        if 'file' not in request.files:
            print("before redirect")
            return redirect(request.url)

        file = request.files['file']
        print(file)

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    print(file_stream)
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    known_face_encoding = known_face_encodings[0]

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    print(img)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    print(unknown_face_encodings)

    face_found = False
    name = ""
    print("engoding length")
    print(len(unknown_face_encodings))
    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            name = known_face_names[0]

    # Return the result as json

    result = {
        "face_found_in_image": face_found,
        "personname": name
    }
    json_data = json.dumps(result)
    #response = app.response_class(
        #response=json.dumps(result),
        #mimetype='application/json'
    # )
    #js = json.dumps(data)

    resp = Response(json_data, status=200, mimetype='application/javascript')
    print(resp)
    return resp
    
    #return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
