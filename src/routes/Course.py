from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
import uuid
from models.entities.Course import Course
from models.CourseModel import CourseModel


# Crea un Namespace temporal para definir el modelo
ns = Namespace("courses", description="Namespace to define models")

# Define el modelo de datos "item_model"
item_model = ns.model("Course", {
    "id": fields.String(readOnly=True, description="Course ID"),
     "name": fields.String(required=False, description="Course Name"), 
     "credits": fields.String(required=False, description="Course credits"), 
     "beginDate": fields.Date(required=False, description="Course Beging Date")
})

# Almacenamiento en memoria de los items (solo para fines de ejemplo)
courses = []


@ns.route("/")
class GetCoursesList(Resource):
    @ns.doc("list_courses")
    @ns.marshal_list_with(item_model)
    def get(self):
        """List all courses"""
        try:
            courses = CourseModel.get_courses()

            return courses

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@ns.route("/<string:id>")
class GetCourse(Resource):
    @ns.doc("get_course")
    @ns.marshal_with(item_model)
    def get(self, id):
        """Retrieve a single course by ID"""
        try:
            course = CourseModel.get_course_by_id(id)
            
            if course is None:
                return {"message": "Course not found"}, 404
            return course

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@ns.route("/add")
class AddCourse(Resource):
    @ns.doc("add_course")
    @ns.expect(item_model, validate=True)
    # @ns.marshal_with(item_model, code=201)
    def post(self):
        """Add a new course"""
        try:
            name = request.json['name']
            credits = int(request.json['credits'])
            beginDate = request.json['beginDate']
            id = uuid.uuid4()       
             #To put Validation here
            new_course = Course(str(id), name, credits, beginDate)
       
            affected_rows = CourseModel.add_course(new_course)   

            if affected_rows != 1:
                return jsonify({'message': "No course inserted"}), 404     

            courses.append(new_course)
            return {"message": f"Course with id {new_course.id} inserted successfully"}, 200  
            
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500    


@ns.route("/delete/<string:id>")
class DeleteCourse(Resource):
    @ns.doc("delete_course")
    def delete(self, id):
        """Delete a course by ID"""
        try:
            affected_rows = CourseModel.delete_course(id)
            if affected_rows != 1:
                return {"message": "Course to delete not found"}, 404
            return {"message": f"Course with id {id} deleted successfully"}, 200    

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@ns.route("/update/<string:id>")
class UpdateCourse(Resource):
    @ns.doc("update_course")
    @ns.expect(item_model, validate=True)
    # @ns.marshal_with(item_model, code=201)
    def put(self, id):
        """Update a course"""
        try:
            # To put Validation here
            name = request.json['name']
            credits = int(request.json['credits'])
            beginDate = request.json['beginDate']                
            courseToUpdate = Course(str(id), name, credits, beginDate)
       
            affected_rows = CourseModel.update_course(courseToUpdate)   

            if affected_rows != 1:
                return jsonify({'message': "No course updated"}), 404     
            return {"message": f"Course with id {id} updated successfully"}, 200
            
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500    