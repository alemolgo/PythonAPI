from models.entities.Course import Course
from database.db import get_connection
from database.CourseDao import CourseDao
from flask import jsonify


class CourseModel():
    @classmethod
    def get_courses(self):
        try:
            resultset = CourseDao.get_all_courses()
            courses = []

            for row in resultset:
                course = Course(row["id"], row["name"],
                                row["credits"], row["beginDate"])
                courses.append(course.to_JSON())

            return courses

        except Exception as ex:
            raise Exception(f"Error on [CourseModel.get_courses]: {str(ex)}")

    @classmethod
    def get_course_by_id(self, id):
        try:
            row = CourseDao.get_course_by_id(id)
            course = None

            if row != None:
                course = Course(row["id"], row["name"],
                                row["credits"], row["beginDate"])
                course = course.to_JSON()
            return course

        except Exception as ex:
            raise Exception(
                f"Error on [CourseModel.get_course_by_id]: {str(ex)}")

    @classmethod
    def add_course(self, course):
        try:
            affected_rows = CourseDao.create_course(course)

            return affected_rows
        except Exception as ex:
            raise Exception(f"Error adding a course: {str(ex)}")        

    @classmethod
    def update_course(self, course):
        try:
            affected_rows = CourseDao.update_course(course)

            return affected_rows
        except Exception as ex:
            raise Exception(f"Error updating a course: {str(ex)}")

    @classmethod
    def delete_course(self, id):
        try:
            affected_rows = CourseDao.delete_course(id)

            return affected_rows
        except Exception as ex:
            raise Exception(f"Error deleting course: {str(course), str(ex)}")
        
    @classmethod
    def old_get_courses(self):
        try:
            connection = get_connection()
            courses = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, credits, beginDate FROM Course ORDER BY name ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    course = Course(row[0], row[1], row[2], row[3])
                    courses.append(course.to_JSON())
                return courses
        except Exception as ex:
            raise Exception(f"Error getting courses: {str(ex)}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def old_get_course_by_id(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, credits, beginDate FROM Course WHERE id = %s", (id,))
                row = cursor.fetchone()

                course = None
                if row != None:
                    course = Course(row[0], row[1], row[2], row[3])
                    course = course.to_JSON()

                return course
        except Exception as ex:
            raise Exception(f"Error getting a course: {str(ex)}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def old_add_course(self, course):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO Course (id, name, credits, beginDate)
                                VALUES (%s, %s, %s, %s)""", (course.id, course.name, course.credits, course.beginDate))
                affected_rows = cursor.rowcount
                connection.commit()

                return affected_rows
        except Exception as ex:
            raise Exception(f"Error adding a course: {str(ex)}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def old_update_course(self, course):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE Course SET name = %s, credits = %s, beginDate = %s 
                                WHERE id = %s""", (course.name, course.credits, course.beginDate, course.id))
                affected_rows = cursor.rowcount
                connection.commit()

                return affected_rows
        except Exception as ex:
            raise Exception(f"Error updating a courses: {str(ex)}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def old_delete_course(self, id):
        try:
            connection = get_connection()
            print(id)

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Course WHERE id = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            return affected_rows

        except Exception as ex:
            raise Exception(f"Error deleting course: {str(course), str(ex)}")
        finally:
            cursor.close()
            connection.close()
