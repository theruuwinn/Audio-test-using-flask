from flask import Blueprint, request, jsonify
from application.audio import audiofiletype
from application.databases import db

import logging
from rich.logging import RichHandler

import datetime

blueprint = Blueprint("view", __name__, url_prefix="/")

# Logging module
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[RichHandler()]
)

logger = logging.getLogger("rich")



@blueprint.route("/")
def home():
    return "server is runnin"


@blueprint.route("/api/v1/create", methods=["POST"])
def create_api():
    if request.method == "POST":

        data = request.json
        type = data.get("audioFileType", None)

        if type is None:
            return "The request is invalid: 400 bad request", 400
        audio_type = audiofiletype.get(type)
        metadata = data.get("audioFileMetadata")

        # check duration time and upload time
        if metadata["duration_time"] <= 0:
            metadata["duration_time"] = 0
        metadata["uploaded_time"] = datetime.datetime.utcnow()
        if type == "podcast":
            participent = metadata.get("participents", None)
            if (
                participent is None
                or len(participent) > 10
                or any(i for i in participent if len(i) > 100)
            ):
                return "The request is invalid: 400 bad request", 400
        try:
            audio_obj = audio_type(**metadata)
            db.session.add(audio_obj)
            db.session.commit()
            db.session.close()
            return "200 ok", 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400


@blueprint.route("/api/v1/update/<audioFileType>/<audioFileID>", methods=["PUT"])
def update_api(audioFileType, audioFileID):
    if request.method == "PUT":
        request_data = request.json
        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_file_obj = audiofiletype.get(audioFileType)
        metadata = request_data.get("audioFileMetadata")
        metadata["uploaded_time"] = datetime.datetime.utcnow()
        try:
            audio_obj = audio_file_obj.query.filter_by(id=int(audioFileID))
            if not metadata:
                return "The request is invalid: 400 bad request", 400

            audio_obj.update(dict(metadata))
            db.session.commit()
            db.session.close()
            return "200 ok", 200
        except Exception as e:
            logger.exception(e)
            return {
                "msg": "Internal Error"
            }, 500
            
    return "The request is invalid: 400 bad request", 400


@blueprint.route("/api/v1/delete/<audioFileType>/<audioFileID>", methods=["DELETE"])
def delete_api(audioFileType, audioFileID):
    if request.method == "DELETE":

        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_file_obj = audiofiletype.get(audioFileType)
        try:
            audio_obj = audio_file_obj.query.filter_by(id=int(audioFileID))
            if not audio_obj.one():
                return "The request is invalid: 400 bad request", 400
            audio_obj.delete()
            db.session.commit()
            db.session.close()
            return "200 ok", 200
        except Exception as e:
            logger.exception(e)
            return {
                "msg": "Internal Error"
            }, 500
    return "The request is invalid: 400 bad request", 400


@blueprint.route(
    "/api/v1/get/<audioFileType>", methods=["GET"], defaults={"audioFileID": None}
)
@blueprint.route("/api/v1/get/<audioFileType>/<audioFileID>", methods=["GET"])
def get_api(audioFileType, audioFileID):
    if request.method == "GET":
        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_obj = audiofiletype.get(audioFileType)
        data = None
        try:
            if audioFileID is not None:
                data = audio_obj.query.filter_by(id=int(audioFileID)).one()
                data = [data.as_dict()]
            else:
                data = audio_obj.query.all()
                data = [i.as_dict() for i in data]
            return jsonify({"data": data}), 200
        except Exception as e:
            logger.exception(e)
            return {
                "msg": "Internal Error"
            }, 500
    return "The request is invalid: 400 bad request", 400
