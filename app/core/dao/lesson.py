from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query
from app.utils.Error import CustomError
from datetime import datetime


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(16))
    begin_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, term):
        term_dict = {
            'name': term.name,
            'begin_time': str(term.begin_time),
            'end_time': str(term.end_time)
        }
        return term_dict

    @classmethod
    def reformatter_insert(cls, data):
        return data

    @classmethod
    def reformatter_update(cls, data):
        return data

    @classmethod
    def query_terms(cls, query_dict: dict = None, unscoped: bool = False):
        name_map = {'terms': Term}
        url_condition = UrlCondition(query_dict)
        query = Term.query
        if not unscoped:
            query = query.filter(Term.using == True)
        if 'time' in query_dict:
            query = query.filter(Term.begin_time < query_dict['time']).filter(
                Term.end_time >= query_dict['time'])
        try:
            (query, total) = process_query(query, url_condition.filter_dict,
                                           url_condition.sort_limit_dict, url_condition.page_dict,
                                           name_map, Term)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def get_term(cls, term_name: str, unscoped: bool = False):
        term = Term.query
        if not unscoped:
            term = term.filter(Term.using == True)
        try:
            term = term.filter(Term.name == term_name).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if term is None:
            raise CustomError(404, 404, 'term not found')
        return cls.formatter(term)

    @classmethod
    def get_now_term(cls):
        try:
            term = Term.query.order_by(Term.name.desc()).filter(Term.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if term is None:
            raise CustomError(404, 404, 'term not found')
        return cls.formatter(term)


class LessonRecord(db.Model):
    __tablename__ = 'lesson_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    term = db.Column(db.String(32), default='')
    username = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    group_name = db.Column(db.String(64), nullable=False, default='')
    to_be_submitted = db.Column(db.Integer, nullable=False, default=0)
    has_submitted = db.Column(db.Integer, nullable=False, default=0)
    total_times = db.Column(db.Integer, nullable=False, default=0)
    using = db.Column(db.Boolean, nullable=True, default=True)

    @classmethod
    def formatter(cls, lesson_record):
        try:
            lesson_record_dict = {
                'id': lesson_record.id,
                'username': lesson_record.username,
                'name': lesson_record.name,
                'term': lesson_record.term,
                'group_name': lesson_record.group,
                'to_be_submitted': lesson_record.to_be_submitted,
                'has_submitted': lesson_record.has_submitted,
                'total_times': lesson_record.total_times
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return lesson_record_dict

    @classmethod
    def reformatter_insert(cls, data):
        return data

    @classmethod
    def reformatter_update(cls, data):
        return data

    @classmethod
    def get_lesson_record(cls, id: int, unscoped: bool = False):
        lesson_record = LessonRecord.query
        if not unscoped:
            lesson_record = lesson_record.filter(Term.using == True)
        try:
            lesson_record = lesson_record.filter(LessonRecord.id == id).filter(LessonRecord.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if lesson_record is None:
            raise CustomError(404, 404, 'lesson record not found')
        return cls.formatter(lesson_record)

    @classmethod
    def insert_lesson_record(cls, ctx: bool = True, data: dict = {}):
        data = cls.reformatter_insert(data)
        lesson_record = LessonRecord()
        for key, value in data.items():
            if hasattr(lesson_record, key):
                setattr(lesson_record, key, value)
        db.session.add(lesson_record)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_lesson_records(cls, query_dict: dict = {}, unscoped: bool = False):
        name_map = {'lesson_records': LessonRecord}
        query = LessonRecord.query
        if not unscoped:
            query = query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict,
                                           url_condition.sort_limit_dict, url_condition.page_dict,
                                           name_map, LessonRecord)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_lesson_record(cls, ctx: bool = True, query_dict: dict = {}):
        name_map = {'lesson_records': LessonRecord}
        lesson_records = LessonRecord.query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (lesson_records, total) = process_query(lesson_records, url_condition.filter_dict,
                                                    url_condition.sort_limit_dict, url_condition.page_dict,
                                                    name_map, LessonRecord)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_record in lesson_records:
            lesson_record.using = False
            db.session.add(lesson_record)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_lesson_record(cls, ctx: bool = True, query_dict: dict = {}, data: dict = {}):
        data = cls.reformatter_insert(data)
        name_map = {'lesson_records': LessonRecord}
        lesson_records = LessonRecord.query.filter(LessonRecord.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (lesson_records, total) = process_query(lesson_records, url_condition.filter_dict,
                                                    url_condition.sort_limit_dict, url_condition.page_dict,
                                                    name_map, LessonRecord)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_record in lesson_records:
            for key, value in data.items():
                if hasattr(lesson_record, key):
                    setattr(lesson_record, key, value)
            db.session.add(lesson_record)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)  # lesson_notice id 关注课程id
    lesson_id = db.Column(db.String(32), default='')  # 被关注课程的id
    lesson_attribute = db.Column(db.String(8), default='')
    lesson_state = db.Column(db.String(8), default='')
    lesson_level = db.Column(db.String(8), default='')
    lesson_name = db.Column(db.String(32), default='')
    lesson_teacher_id = db.Column(db.String(48), default='')
    lesson_teacher_letter = db.Column(db.String(32), default='')
    lesson_teacher_name = db.Column(db.String(8), default='')
    lesson_teacher_unit = db.Column(db.String(16), default='')
    lesson_unit = db.Column(db.String(16), default='')
    lesson_year = db.Column(db.String(32), default='')
    lesson_semester = db.Column(db.Integer, default='')
    lesson_class = db.Column(db.String(255), default='')
    lesson_type = db.Column(db.String(8), default='')
    lesson_grade = db.Column(db.String(64), default='')
    lesson_model = db.Column(db.String(32), default='')
    term = db.Column(db.String(32), default='')
    notices = db.Column(db.Integer, default=0)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, lesson):
        lesson_dict = {'id': lesson.id, 'lesson_id': lesson.lesson_id, 'lesson_attribute': lesson.lesson_attribute,
                       'lesson_state': lesson.lesson_state, 'lesson_teacher_id': lesson.lesson_teacher_id,
                       'lesson_name': lesson.lesson_name, 'lesson_teacher_name': lesson.lesson_teacher_name,
                       'lesson_semester': lesson.lesson_semester, 'lesson_level': lesson.lesson_level,
                       'lesson_teacher_unit': lesson.lesson_teacher_unit, 'lesson_unit': lesson.lesson_unit,
                       'lesson_year': lesson.lesson_year, 'lesson_type': lesson.lesson_type,
                       'lesson_class': lesson.lesson_class, 'lesson_grade': lesson.lesson_grade,
                       'lesson_model': lesson.lesson_model, 'term': lesson.term}
        return lesson_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        allow_column = ['lesson_id', 'lesson_attribute', 'lesson_state', 'lesson_level', 'lesson_name',
                        'lesson_teacher_id', 'lesson_teacher_letter', 'lesson_teacher_name', 'lesson_teacher_unit',
                        'lesson_unit', 'lesson_year', 'lesson_semester', 'lesson_class', 'lesson_type', 'lesson_grade',
                        'lesson_model', 'term', 'notices']
        new_data = dict()
        for key, value in data.items():
            if key in allow_column:
                new_data[key] = value
        return new_data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def get_lesson(cls, id: int, unscoped: bool = False):
        lesson = Lesson.query
        if not unscoped:
            lesson = lesson.filter(Term.using == True)
        try:
            lesson = lesson.filter(Lesson.id == id).filter(Lesson.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if lesson is None:
            raise CustomError(404, 404, 'lesson not found')
        return cls.formatter(lesson)

    @classmethod
    def insert_lesson(cls, ctx: bool = True, data: dict = {}):
        data = cls.reformatter_insert(data)
        lesson = Lesson()
        for key, value in data.items():
            if hasattr(lesson, key):
                setattr(lesson, key, value)
        db.session.add(lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_lessons(cls, query_dict: dict = {}, unscoped: bool = False):
        name_map = {'lessons': Lesson}
        query = Lesson.query
        if not unscoped:
            query = query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                           url_condition.page_dict, name_map, Lesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_lesson(cls, ctx: bool = True, query_dict: dict = {}):
        name_map = {'lessons': Lesson}
        lessons = Lesson.query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (lessons, total) = process_query(lessons, url_condition.filter_dict, url_condition.sort_limit_dict,
                                             url_condition.page_dict, name_map, Lesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson in lessons:
            lesson.using = False
            db.session.add(lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_lesson(cls, ctx: bool = True, query_dict: dict = {}, data: dict = {}):
        data = cls.reformatter_insert(data)
        name_map = {'lessons': Lesson}
        lessons = Lesson.query.filter(Lesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (lessons, total) = process_query(lessons, url_condition.filter_dict, url_condition.sort_limit_dict,
                                             url_condition.page_dict, name_map, Lesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson in lessons:
            for key, value in data.items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)
            db.session.add(lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class LessonCase(db.Model):
    __tablename__ = 'lesson_cases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.Integer, default=-1)
    lesson_room = db.Column(db.String(48), default='')
    lesson_weekday = db.Column(db.Integer, default=0)
    lesson_week = db.Column(db.String(48), default='')
    lesson_time = db.Column(db.String(48), default='')
    lesson_date = db.Column(db.Date, default=datetime.now)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, lesson_case):
        lesson_case_dict = {'lesson_week': lesson_case.lesson_week, 'lesson_time': str(lesson_case.lesson_time),
                            'lesson_date': str(lesson_case.lesson_date.strftime('%Y-%m-%d')),
                            'lesson_weekday': lesson_case.lesson_weekday,
                            'lesson_room': lesson_case.lesson_room}
        return lesson_case_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def get_lesson_case(cls, id: int, unscoped: bool = False):
        lesson_case = LessonCase.query
        if not unscoped:
            lesson_case = lesson_case.filter(Term.using == True)
        try:
            lesson_case = lesson_case.filter(LessonCase.id == id).filter(LessonCase.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if lesson_case is None:
            raise CustomError(404, 404, 'lesson_case not found')
        return cls.formatter(lesson_case)

    @classmethod
    def insert_lesson_case(cls, ctx: bool = True, data: dict = {}):
        data = cls.reformatter_insert(data)
        lesson_case = LessonCase()
        for key, value in data.items():
            if hasattr(lesson_case, key):
                setattr(lesson_case, key, value)
        db.session.add(lesson_case)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_lesson_cases(cls, query_dict: dict = {}, unscoped: bool = False):
        name_map = {'lesson_cases': LessonCase}
        query = LessonCase.query
        if not unscoped:
            query = query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                           url_condition.page_dict, name_map, LessonCase)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_lesson_case(cls, ctx: bool = True, query_dict: dict = {}):
        name_map = {'lesson_cases': LessonCase}
        lesson_cases = LessonCase.query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (lesson_cases, total) = process_query(lesson_cases, url_condition.filter_dict,
                                                  url_condition.sort_limit_dict,
                                                  url_condition.page_dict, name_map, LessonCase)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_case in lesson_cases:
            lesson_case.using = False
            db.session.add(lesson_case)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_lesson_case(cls, ctx: bool = True, query_dict: dict = {}, data: dict = {}):
        data = cls.reformatter_insert(data)
        name_map = {'lesson_cases': LessonCase}
        lesson_cases = LessonCase.query.filter(LessonCase.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (lesson_cases, total) = process_query(lesson_cases, url_condition.filter_dict,
                                                  url_condition.sort_limit_dict,
                                                  url_condition.page_dict, name_map, LessonCase)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for lesson_case in lesson_cases:
            for key, value in data.items():
                if hasattr(lesson_case, key):
                    setattr(lesson_case, key, value)
            db.session.add(lesson_case)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class NoticeLesson(db.Model):
    __tablename__ = 'notice_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(32), default=-1)
    assign_group = db.Column(db.String(32), default='')
    term = db.Column(db.String(32), default='')
    notice_reason = db.Column(db.String(128), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, notice_lesson):
        notice_lesson_dict = {
            'id': notice_lesson.id,
            'lesson_id': notice_lesson.lesson_id,
            'notice_reason': notice_lesson.notice_reason,
            'assign_group': notice_lesson.assign_group
        }
        return notice_lesson_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def get_notice_lesson(cls, id: int, unscoped: bool = False):
        notice_lesson = NoticeLesson.query
        if not unscoped:
            notice_lesson = notice_lesson.filter(Term.using == True)
        try:
            notice_lesson = notice_lesson.filter(NoticeLesson.id == id).filter(NoticeLesson.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if notice_lesson is None:
            raise CustomError(404, 404, 'notice_lesson not found')
        return cls.formatter(notice_lesson)

    @classmethod
    def insert_notice_lesson(cls, ctx: bool = True, data: dict = {}):
        data = cls.reformatter_insert(data)
        notice_lesson = NoticeLesson()
        for key, value in data.items():
            if hasattr(notice_lesson, key):
                setattr(notice_lesson, key, value)
        db.session.add(notice_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_notice_lessons(cls, query_dict: dict = {}, unscoped: bool = False):
        name_map = {'notice_lessons': NoticeLesson}
        query = NoticeLesson.query
        if not unscoped:
            query = query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                           url_condition.page_dict, name_map, NoticeLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_notice_lesson(cls, ctx: bool = True, query_dict: dict = {}):
        name_map = {'notice_lessons': NoticeLesson}
        notice_lessons = NoticeLesson.query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (notice_lessons, total) = process_query(notice_lessons, url_condition.filter_dict,
                                                    url_condition.sort_limit_dict,
                                                    url_condition.page_dict, name_map, NoticeLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for notice_lesson in notice_lessons:
            notice_lesson.using = False
            db.session.add(notice_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_notice_lesson(cls, ctx: bool = True, query_dict: dict = {}, data: dict = {}):
        data = cls.reformatter_insert(data)
        name_map = {'notice_lessons': NoticeLesson}
        notice_lessons = NoticeLesson.query.filter(NoticeLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (notice_lessons, total) = process_query(notice_lessons, url_condition.filter_dict,
                                                    url_condition.sort_limit_dict,
                                                    url_condition.page_dict, name_map, NoticeLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for notice_lesson in notice_lessons:
            for key, value in data.items():
                if hasattr(notice_lesson, key):
                    setattr(notice_lesson, key, value)
            db.session.add(notice_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class ModelLesson(db.Model):
    __tablename__ = 'model_lessons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id = db.Column(db.String(32), default='')
    term = db.Column(db.String(32), default='')
    status = db.Column(db.String(32), default='推荐课')  # 好评课 推荐课
    votes = db.Column(db.Integer, default=0)
    assign_group = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, model_lesson):
        model_lesson_dict = {
            'id': model_lesson.id,
            'lesson_id': model_lesson.lesson_id,
            'assign_group': model_lesson.assign_group,
            'status': model_lesson.status,
            'votes': model_lesson.votes,
        }
        return model_lesson_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        allow_column = ['lesson_id', 'assign_group', 'status', 'votes', 'term']
        new_data = dict()
        for key, value in data.items():
            if key in allow_column:
                new_data[key] = value
        return new_data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def get_model_lesson(cls, id: int, unscoped: bool = False):
        model_lesson = ModelLesson.query
        if not unscoped:
            model_lesson = model_lesson.filter(Term.using == True)
        try:
            model_lesson = model_lesson.filter(ModelLesson.id == id).filter(ModelLesson.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if model_lesson is None:
            raise CustomError(404, 404, 'model_lesson not found')
        return cls.formatter(model_lesson)

    @classmethod
    def insert_model_lesson(cls, ctx: bool = True, data: dict = {}):
        data = cls.reformatter_insert(data)
        model_lesson = ModelLesson()
        for key, value in data.items():
            if hasattr(model_lesson, key):
                setattr(model_lesson, key, value)
        db.session.add(model_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_model_lessons(cls, query_dict: dict = {}, unscoped: bool = False):
        name_map = {'model_lessons': ModelLesson}
        query = ModelLesson.query
        if not unscoped:
            query = query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                           url_condition.page_dict, name_map, ModelLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_model_lesson(cls, ctx: bool = True, query_dict: dict = {}):
        name_map = {'model_lessons': ModelLesson}
        model_lessons = ModelLesson.query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (model_lessons, total) = process_query(model_lessons, url_condition.filter_dict,
                                                   url_condition.sort_limit_dict,
                                                   url_condition.page_dict, name_map, ModelLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for model_lesson in model_lessons:
            model_lesson.using = False
            db.session.add(model_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_model_lesson(cls, ctx: bool = True, query_dict: dict = {}, data: dict = {}):
        data = cls.reformatter_insert(data)
        name_map = {'model_lessons': ModelLesson}
        model_lessons = ModelLesson.query.filter(ModelLesson.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (model_lessons, total) = process_query(model_lessons, url_condition.filter_dict,
                                                   url_condition.sort_limit_dict,
                                                   url_condition.page_dict, name_map, ModelLesson)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for model_lesson in model_lessons:
            for key, value in data.items():
                if hasattr(model_lesson, key):
                    setattr(model_lesson, key, value)
            db.session.add(model_lesson)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True