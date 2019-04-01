import cv2
import os
import shutil
import json
import uuid
from clams import Mmif
from clams.vocab import AnnotationTypes

def process_file(temp_file):
    cap = cv2.VideoCapture(temp_file)
    counter = 0
    sample_ratio = 30
    #make a directory to store the images
    file_name = os.path.splitext(os.path.basename(temp_file))[0]
    img_dir = "static/imgs/{}".format(file_name)
    shutil.rmtree(img_dir, ignore_errors=True, onerror=None)

    os.mkdir(img_dir)

    while cap.isOpened():
        ret, f = cap.read()
        if not ret:
            break
        if counter % sample_ratio == 0:
            processed_frame = process_image(f)
            cv2.imwrite(os.path.join(img_dir, str(counter)+".png"), processed_frame)
        counter += 1
    return img_dir

def process_image(f):
    maxsize = (50, 50)
    imRes = cv2.resize(f, maxsize, interpolation=cv2.INTER_CUBIC)
    return imRes

def generate_image_html(image_path):
    ##<option data-img-src='/static/img/1.png' value='4.jpg'>4.jpg</option>
    result = ""
    # for file in os.listdir("static/imgs"):
    #     if file.endswith(".png"):
    #         result += "<option data-img-src='static/imgs/{0}' value='{0}'>{0}</option>".format(file)
    num_files = len(os.listdir(image_path))
    cur_frame = 0
    for i in range(num_files):
        file = str(cur_frame)+".png"
        result += "<option data-img-src='{0}/{1}' value='{2}'>{1}</option>".format(image_path, file, cur_frame)
        cur_frame += 30
    return result

def annotations_to_mmif(request_form_data):
    """
    converts annotations to mmif
    :param request_form_data:
    :return: mmif
    """
    def media_dict(media_path):
        md = {}
        md["type"] = "audio-video"
        md = {}
        md["id"] = 0
        md["type"] = "audio-video"
        md["location"] = media_path
        md["metadata"] = {}
        return md

    annotations =  (request_form_data.getlist("anno"))
    MMIF_dict = {}
    MMIF_dict["context"] = ""
    MMIF_dict["contains"] = {}
    MMIF_dict["metadata"] = {}
    MMIF_dict["media"] = [media_dict(request_form_data.get("video"))]
    MMIF_dict["views"] = []

    MMIF_json = json.dumps(MMIF_dict)
    mmif = Mmif(MMIF_json)
    new_view = mmif.new_view()
    contain = new_view.new_contain(AnnotationTypes.SD)
    contain.producer = str("human_annotator")

    for int_id, frame_number in enumerate(annotations):
        annotation = new_view.new_annotation(int_id)
        annotation.start = str(frame_number)
        annotation.end = str(
            frame_number)  # since we're treating each frame individually for now, start and end are the same
        annotation.attype = AnnotationTypes.SD

    for contain in new_view.contains.keys():
        mmif.contains.update({contain: new_view.id})

    unique_filename = str(uuid.uuid4()) + ".json"
    with open(os.path.join("mmif_json_files",unique_filename), "w") as f:
        f.write(str(mmif))

    return mmif