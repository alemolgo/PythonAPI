from database.db import get_db_data
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.sql import select, insert, update, delete
from utils.Logger import Logger
import traceback

# Obtiene los datos para armar la conección
dbData = get_db_data()

# Configuración de la base de datos
DATABASE_URL = f"mysql+pymysql://{dbData.user}:{dbData.password}@localhost/{dbData.database}"
engine = create_engine(DATABASE_URL, echo=False)

# Crea un objeto MetaData
metadata = MetaData()

# Definición de la tabla "course"
course_table = Table(
    "Course", metadata,
    # id = Column(Integer, primary_key=True, autoincrement=True)
    Column("id", String(36), primary_key=True),
    Column("name", String(30), nullable=False),
    Column("credits", Integer, nullable=False),
    Column("beginDate", DateTime, nullable=False)
)

# metadata.create_all(engine)  # Crear la tabla en la base de datos (si no existe)

class CourseDao():
    @classmethod
    def get_all_courses(self):
        try:
            with engine.connect() as conn:
                stmt = select(course_table)
                result = conn.execute(stmt)                
                resultset = [dict(row._mapping) for row in result] # Usamos row._mapping para convertir la fila en un diccionario
               
                Logger.add_to_log("info", "information delivery successfully")
                return resultset
        except Exception as ex:
            Logger.add_to_log("error", f"[CourseDao.get_all_courses]: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            raise Exception(f"Error executing [CourseDao.get_all_courses] query on DB: {str(ex)}")
        finally:
            conn.close

    @classmethod
    def get_course_by_id(self, id):
        try:
            with engine.connect() as conn:
                stmt = select(course_table).where(course_table.c.id == id)
                result = conn.execute(stmt).fetchone()
                return dict(result._mapping) if result else None

        except Exception as ex:
            Logger.add_to_log("error", f"[CourseDao.get_all_courses]: {str(ex)}")
            raise Exception("Error executing [CourseDao.get_course_by_id] query on DB")
        finally:
            conn.close

    @classmethod
    def create_course(self, course):
        try:
            with engine.connect() as conn:                 
               with conn.begin():  # Iniciar una transacción
                    stmt = insert(course_table).values(id=course.id, name=course.name, credits=course.credits, beginDate=course.beginDate)
                    result = conn.execute(stmt)
                    # inserted_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
                    return result.rowcount

        except Exception as ex:
            Logger.add_to_log("error", f"[CourseDao.get_all_courses]: {str(ex)}")
            raise Exception(f"Error executing [CourseDao.create_course] query on DB: {str(ex)}")
        finally:
            conn.close

    @classmethod
    def update_course(self, course):
        try:
            with engine.connect() as conn:                 
               with conn.begin():  # Iniciar una transacción
                
                stmt = update(course_table).where(course_table.c.id == course.id).values(
                    name=course.name,
                    credits=course.credits,
                    beginDate=course.beginDate)
                
                result = conn.execute(stmt)
                return result.rowcount  # Retorna el número de filas afectadas
                
        except Exception as ex:
            Logger.add_to_log("error", f"[CourseDao.get_all_courses]: {str(ex)}")
            raise Exception(f"Error executing [CourseDao.update_course] query on DB: {str(ex)}")
        finally:
            conn.close

    @classmethod
    def delete_course(self, id):
        try:
            with engine.connect() as conn:                 
               with conn.begin():  # Iniciar una transacción
                
                stmt = delete(course_table).where(course_table.c.id == id)
                result = conn.execute(stmt)
                return result.rowcount  # Retorna el número de filas afectadas
                
        except Exception as ex:
            Logger.add_to_log("error", f"[CourseDao.get_all_courses]: {str(ex)}")
            raise Exception(f"Error executing [CourseDao.delete_course] query on DB: {str(ex)}")
        finally:
            conn.close       

