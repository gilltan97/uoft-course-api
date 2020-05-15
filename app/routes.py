import json 
import re

from bson import json_util
from flask import Blueprint, request

from app.parsers.query_parser import FilterQuery
from app.filters import Filters
from app.database.mongo import db 
from app.errors import CourseNotFoundError, FilterNotAppliedError

mongodb = db

api = Blueprint('api', __name__)

@api.route('/api/v1/courses/', methods=['GET'])
@api.route('/api/v1/courses/<course_code>/', methods=['GET'])
def get_all_courses(course_code=None):
	courses = mongodb.Courses

	filters = {}
	if (course_code):
		filters["course code"] = course_code

	output = []
	for course in courses.find(filters):
		output.append(course)

	if (course_code and not output):
		raise CourseNotFoundError(course_code)

	return json.dumps({ 
		'status': 200,
		'courses': output 
	}, indent=4, default=json_util.default), 200


@api.route('/api/v1/courses/filter', methods=['GET'])
def get_filtered_courses():
	courses = mongodb.Courses

	if ("q" in request.args):
		output = Filters(request.args["q"]).apply(courses)

		return json.dumps({
			'status': 200, 
			'courses': output
		}, indent=4, default=json_util.default), 200

	else:
		raise FilterNotAppliedError()
