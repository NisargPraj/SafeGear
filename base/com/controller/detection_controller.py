import os
import urllib
import uuid
from datetime import datetime
import json

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import app

from base.com.vo.detection_vo import DetectionVO
from base.com.dao.detection_dao import DetectionDAO
# from base.com.service.safety_detection import detection
# from base.com.service.revised_safety_detection import detection
from base.com.service.safety_tracker import detection


@app.route('/detect', methods=['POST'])
def detect():
    media = request.files.get('media')
    user_id = request.cookies.get('user_id')
    print("type of userid=======>", type(user_id))

    print("user_id at detect-------->",user_id)

    if media:
        name = secure_filename(media.filename)
        filename = name.split('.')
        filename = f"{filename[0]}_{uuid.uuid4()}.{filename[1]}"
        input_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        media.save(input_video_path)

        detectionVO = DetectionVO()
        detectionDAO = DetectionDAO()

        detectionVO.detection_datetime = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

        output_video_path, count = detection(input_video_path)

        detectionVO.created_by = user_id
        detectionVO.modified_by = user_id
        detectionVO.file_name = name
        detectionVO.input_file_path = input_video_path
        detectionVO.output_file_path = output_video_path
        detectionVO.is_deleted = False
        detectionVO.created_on = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
        detectionVO.modified_on = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
        detectionVO.detection_stats = json.dumps(count)

        detectionDAO.save(detectionVO)

        return render_template("detection/detection_output.html", video=filename, video_name=name)

    return render_template("core/error.html")


@app.route("/view_video", methods=["GET"])
def view_video():
    video = request.args.get('video')
    video_name = request.args.get('video_name')

    return render_template('detection/detection_output.html', video=video, video_name=video_name)


@app.route("/view_detection_table")
def view_detection_table():
    detectionDAO = DetectionDAO()

    detection_table = detectionDAO.view()

    return render_template("detection/view_detections.html", data=detection_table)


@app.route("/detection_delete", methods=["GET"])
def detection_delete():
    detection_id = request.args.get("det_id")
    user_id = request.cookies.get('user_id')

    print("user_id in delete------>", user_id)

    detectionDAO = DetectionDAO()

    detectionDAO.soft_delete(detection_id, user_id)

    return redirect(url_for('view_detection_table'))

