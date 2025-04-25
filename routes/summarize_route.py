from flask import Blueprint, request, jsonify
import traceback  # For capturing the full stack trace
from services.summarizer import get_summary

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/summarize', methods=['POST'])
def summarize_video():
    data = request.get_json()
    video_link = data.get("videoLink")

    if not video_link:
        return jsonify({"error": "No video link provided"}), 400

    try:
        summary = get_summary(video_link)
        return jsonify({"summary": summary})
    except Exception as e:
        # Capture full stack trace and print it in the console
        error_message = str(e)
        stack_trace = traceback.format_exc()  # Capture the full stack trace
        print(f"Error: {error_message}\nStack Trace: {stack_trace}")  # Print it to console

        # Return the error and stack trace in the response for easier debugging
        return jsonify({"error": error_message, "stackTrace": stack_trace}), 500
