from models import db, User, Student, Course, Class, Attendance, Grade
from datetime import datetime
from utils import error_response


class AuthService:
    BLACKLIST = set()

    @staticmethod
    def register_user(data) -> User | tuple:
        if User.query.filter_by(email=data['email']).first():
            return error_response('Email already exists', 400)

        user = User()
        user.email = data['email']
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.user_type = data.get('user_type', 3)
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(email: str, password: str) -> User | None:
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None
        return user

    @staticmethod
    def blacklist_token(jti):
        AuthService.BLACKLIST.add(jti)

    @staticmethod
    def is_token_blacklisted(jti):
        return jti in AuthService.BLACKLIST

    @staticmethod
    def get_all_users() -> list[User]:
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id: int, data) -> User | None:
        user = User.query.get(user_id)
        if not user:
            return None
        for key in ('email', 'first_name', 'last_name', 'phone', 'is_active'):
            if key in data:
                setattr(user, key, data[key])
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True


class StudentService:
    @staticmethod
    def get_all_students() -> list[Student]:
        return Student.query.all()

    @staticmethod
    def get_student_by_id(student_id: int) -> Student | None:
        return Student.query.get(student_id)

    @staticmethod
    def create_student(data) -> Student | tuple:
        # Create user first
        user_data = data.get('user') or {}
        if User.query.filter_by(email=user_data.get('email')).first():
            return error_response('Email already exists', 400)

        user = User()
        user.email = user_data.get('email')
        user.first_name = user_data.get('first_name')
        user.last_name = user_data.get('last_name')
        user.user_type = 3  # Student
        user.set_password(user_data.get('password', 'default_password'))
        db.session.add(user)
        db.session.flush()

        # Create student profile
        student = Student()
        student.student_id = data.get('student_id')
        student.dob = datetime.strptime(data.get('dob'), '%Y-%m-%d').date() if data.get('dob') else None
        student.gender = data.get('gender')
        student.address = data.get('address', '')
        student.user_id = user.id
        db.session.add(student)

        # Assign parents if provided
        if 'parents' in data:
            for parent_email in data['parents']:
                parent = User.query.filter_by(email=parent_email, user_type=4).first()
                if parent:
                    student.parents.append(parent)

        db.session.commit()
        return student

    @staticmethod
    def update_student(student_id: int, data) -> Student | None:
        student = Student.query.get(student_id)
        if not student:
            return None

        if 'student_id' in data:
            student.student_id = data['student_id']
        if 'dob' in data:
            student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        if 'gender' in data:
            student.gender = data['gender']
        if 'address' in data:
            student.address = data['address']
        if 'current_class_id' in data:
            student.current_class_id = data['current_class_id']

        # Update linked user fields if provided
        user_fields = {}
        for key in ('email', 'first_name', 'last_name'):
            if key in data:
                setattr(student.user, key, data[key])

        db.session.commit()
        return student

    @staticmethod
    def delete_student(student_id: int) -> bool:
        student = Student.query.get(student_id)
        if not student:
            return False

        db.session.delete(student)
        db.session.commit()
        return True


class CourseService:
    @staticmethod
    def get_all_courses() -> list[Course]:
        return Course.query.all()

    @staticmethod
    def get_course_by_id(course_id: int) -> Course | None:
        return Course.query.get(course_id)

    @staticmethod
    def create_course(data) -> Course:
        course = Course()
        course.name = data['name']
        course.code = data.get('code')
        course.description = data.get('description', '')
        db.session.add(course)
        db.session.commit()
        return course

    @staticmethod
    def update_course(data) -> Course | None:
        course_id = data.get('id') or data.get('course_id')
        course = Course.query.get(course_id)
        if not course:
            return None
        if 'name' in data:
            course.name = data['name']
        if 'description' in data:
            course.description = data['description']
        db.session.commit()
        return course

    @staticmethod
    def delete_course(course_id: int) -> bool:
        course = Course.query.get(course_id)
        if not course:
            return False
        db.session.delete(course)
        db.session.commit()
        return True


class ClassService:
    @staticmethod
    def get_all_classes() -> list[Class]:
        return Class.query.all()

    @staticmethod
    def get_class_by_id(class_id: int) -> Class | None:
        return Class.query.get(class_id)

    @staticmethod
    def create_class(data) -> Class:
        class_obj = Class()
        class_obj.name = data['name']
        class_obj.course_id = data['course_id']
        class_obj.teacher_id = data['teacher_id']
        class_obj.schedule = data.get('schedule')
        db.session.add(class_obj)
        db.session.commit()
        return class_obj

    @staticmethod
    def update_class(data) -> Class | None:
        class_id = data.get('id') or data.get('class_id')
        class_obj = Class.query.get(class_id)
        if not class_obj:
            return None
        for key in ('name', 'course_id', 'teacher_id', 'schedule'):
            if key in data:
                setattr(class_obj, key, data[key])
        db.session.commit()
        return class_obj

    @staticmethod
    def delete_class(class_id: int) -> bool:
        class_obj = Class.query.get(class_id)
        if not class_obj:
            return False
        db.session.delete(class_obj)
        db.session.commit()
        return True


class AttendanceService:
    @staticmethod
    def create_attendance(data) -> Attendance:
        attendance = Attendance()
        attendance.student_id = data['student_id']
        attendance.class_id = data['class_id']
        attendance.date = datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None
        attendance.status = data.get('status', 'present')
        db.session.add(attendance)
        db.session.commit()
        return attendance

    @staticmethod
    def get_all_attendance() -> list[Attendance]:
        return Attendance.query.all()

    @staticmethod
    def get_attendance_by_id(attendance_id: int) -> Attendance | None:
        return Attendance.query.get(attendance_id)

    @staticmethod
    def update_attendance(data) -> Attendance | None:
        attendance_id = data.get('id') or data.get('attendance_id')
        attendance = Attendance.query.get(attendance_id)
        if not attendance:
            return None
        if 'status' in data:
            attendance.status = data['status']
        if 'date' in data:
            attendance.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        db.session.commit()
        return attendance

    @staticmethod
    def delete_attendance(attendance_id: int) -> bool:
        attendance = Attendance.query.get(attendance_id)
        if not attendance:
            return False
        db.session.delete(attendance)
        db.session.commit()
        return True


class GradeService:
    @staticmethod
    def create_grade(data) -> Grade:
        grade = Grade()
        grade.student_id = data['student_id']
        grade.course_id = data['course_id']
        grade.grade = data.get('value', data.get('grade'))
        grade.term = data.get('term')
        db.session.add(grade)
        db.session.commit()
        return grade

    @staticmethod
    def get_all_grades() -> list[Grade]:
        return Grade.query.all()

    @staticmethod
    def get_grade_by_id(grade_id: int) -> Grade | None:
        return Grade.query.get(grade_id)

    @staticmethod
    def update_grade(data) -> Grade | None:
        grade_id = data.get('id') or data.get('grade_id')
        grade = Grade.query.get(grade_id)
        if not grade:
            return None
        if 'value' in data:
            grade.grade = data['value']
        if 'term' in data:
            grade.term = data['term']
        db.session.commit()
        return grade

    @staticmethod
    def delete_grade(grade_id: int) -> bool:
        grade = Grade.query.get(grade_id)
        if not grade:
            return False
        db.session.delete(grade)
        db.session.commit()
        return True
