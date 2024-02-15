import datetime
from sqlalchemy import Column, create_engine, ForeignKey, func, select, text, extract, desc, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Text, Time, Interval, String, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from pprint import pprint
from sqlalchemy.ext.associationproxy import association_proxy


# from database.connect import engine, Base, session

# engine = create_engine('sqlite:///library.db')
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()


from sqlalchemy import Column, String, Integer
from database.connect import Base, engine, session


class UserInfo(Base):
    __tablename__ = "user_info"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer)
    telegramm_id = Column(Integer, nullable=False, primary_key=True)

    full_name = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=True)
    blocked = Column(Boolean)
    last_visit_date = Column(String(50), nullable=True)


class RecordDate(Base):
    __tablename__ = "record_dates"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    date = Column(String(50), nullable=False)
    hour = Column(Integer, nullable=False)
    blocked = Column(Boolean)



# class Recipe(Base):
#     __tablename__ = 'recipe'
#     id = Column(Integer, primary_key=True)
#     name_dish = Column(String)
#     number_views = Column(Integer, index=True)
#     cooking_time = Column(Integer)
#     list_ingredients = Column(String)
#     description = Column(String)
#
#     __table_args__ = {'extend_existing': True}




#
#
# class Author(Base):
#     __tablename__ = "authors"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     surname = Column(String(50), nullable=False)
#     book = relationship("Book", cascade="all", backref=backref('authors', passive_deletes=True), lazy="select")
#
#     __table_args__ = {'extend_existing': True}
#
#     def __repr__(self):
#         return f"[{self.id}, {self.name}, {self.surname}]"
#
#
# class Book(Base):
#     __tablename__ = "books"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     count = Column(Integer, default=1)
#     release_date = Column(Date)
#     author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
#     receiving_book = relationship("ReceivingBook", cascade="all", backref=backref('books', passive_deletes=True),
#                                   lazy="subquery")
#
#     __table_args__ = {'extend_existing': True}
#
#
#     def __repr__(self):
#         return f"[{self.id}, {self.name}, {self.release_date}, {self.author_id}]"
#
#     def to_json(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# class Student(Base):
#     __tablename__ = "students"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     surname = Column(String(50), nullable=False)
#     phone = Column(String(50), nullable=False)
#     email = Column(String(50), nullable=False)
#     average_score = Column(Float)
#     scholarship = Column(Boolean)
#
#     # receiving_books = relationship("ReceivingBook",
#     #                               secondary=student_receiving_book,
#     #                               back_populates="students")
#
#     receiving_book = association_proxy("student_receiving_book", "receivingbook")
#
#     __table_args__ = {'extend_existing': True}
#
#
#     def __repr__(self):
#         return f"({self.id}, {self.name}, {self.surname}, {self.phone}," \
#                f" {self.email}, {self.average_score}, {self.scholarship})"
#
#     @classmethod
#     def get_all_students(cls):
#         return session.query(Student).all()
#
#     @classmethod
#     def get_students_by_higher_avg_score(cls, enter_avg_score):
#         return session.query(Student).filter(Student.average_score > enter_avg_score).all()
#
#     def to_json(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# class ReceivingBook(Base):
#     __tablename__ = "receiving_books"
#
#     id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
#     student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
#     date_of_issue = Column(Date, nullable=False)
#     date_of_return = Column(Date)
#
#     # students = relationship("Student",
#     #                         secondary=student_receiving_book,
#     #                         back_populates="receiving_books")
#
#     student = association_proxy("student_receiving_book", "student")
#
#     __table_args__ = {'extend_existing': True}
#
#
#     def __repr__(self):
#         return f"[{self.id}, {self.book_id}, {self.student_id}, {self.date_of_issue}, {self.date_of_return}]"
#
#     @hybrid_method
#     def count_date_with_book(self, id_book_search):
#         result = session.query(ReceivingBook).filter(self.book_id == id_book_search).all()
#         answers = tuple(
#             {"book_id": book.book_id, "count_date_with_book": (book.date_of_return - book.date_of_issue).days}
#             if book.date_of_return is not None
#             else {"book_id": book.book_id,
#                   "count_date_with_book": f"{int(-(datetime.date.today() - book.date_of_issue).days)}"}
#             for book in result)
#         if len(answers) == 1:
#             answers, *_ = answers
#         return answers
#
#     def to_json(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# class StudentReceivingBookAssociation(Base):
#     __tablename__ = "student_receiving_book"
#
#     id = Column(Integer, primary_key=True)
#     students_id = Column(Integer, ForeignKey("students.id"), nullable=False)
#     receiving_books_id = Column(Integer, ForeignKey("receiving_books.id"), nullable=False)
#
#     student = relationship('Student',
#                            backref=backref('student_receiving_book',
#                                            cascade='all, delete-orphan'),
#                            lazy='joined', innerjoin=True,
#                            order_by='Student.id')
#     receiving_book = relationship('ReceivingBook', backref=backref('student_receiving_book',
#                                                                    cascade='all, delete-orphan'))
#
#     __table_args__ = {'extend_existing': True}
#
#
#
# def get_all_books():
#     return session.query(Book).all()
#
#
# def students_debtors():
#     debtors = session.query(ReceivingBook, Student). \
#         join(Student). \
#         filter(ReceivingBook.date_of_return == None)
#
#     student_debtor = [info_debtors[1]
#                       for info_debtors in debtors
#                       if (datetime.date.today() - info_debtors[0].date_of_issue).days > 14]
#     return student_debtor
#
#
# def issue_a_book(data):
#     check_student = session.query(Student).filter(Student.id == data["student_id"]).one_or_none()
#     if not check_student:
#         return ""
#
#     answer = session.query(Book).filter(Book.id == data["book_id"]).filter(Book.count > 0).all()
#
#     if answer:
#         new_receiving_book = ReceivingBook(book_id=data["book_id"],
#                                            student_id=data["student_id"],
#                                            date_of_issue=datetime.date.today())
#         session.add(new_receiving_book)
#
#         reduce_number_books = session.query(Book).filter(Book.id == data["book_id"]).one_or_none()
#         reduce_number_books.count -= 1
#
#         session.commit()
#         return session.query(ReceivingBook).filter(ReceivingBook.student_id == data["student_id"]).all()
#
#
# def hand_over_the_book(data):
#     answer = session.query(ReceivingBook, Book).join(Book). \
#         filter(ReceivingBook.student_id == data["student_id"]). \
#         filter(ReceivingBook.book_id == data["book_id"]). \
#         filter(ReceivingBook.date_of_return == None).first()
#
#     if answer:
#         answer[0].date_of_return = datetime.date.today()
#         answer[1].count += 1
#         session.commit()
#         return session.query(ReceivingBook).filter(ReceivingBook.student_id == data["student_id"]).all()
#     return ""
#
#
# def insert_data():
#     if not session.query(Author).all():
#         authors = [Author(name="Александр", surname="Пушкин"),
#                    Author(name="Лев", surname="Толстой"),
#                    Author(name="Михаил", surname="Булгаков"),
#                    ]
#         authors[0].book.extend([Book(name="Капитанская дочка",
#                                      count=5,
#                                      release_date=datetime.date(1836, 1, 1)),
#                                 Book(name="Евгений Онегин",
#                                      count=3,
#                                      release_date=datetime.date(1838, 1, 1))
#                                 ])
#         authors[1].book.extend([Book(name="Война и мир",
#                                      count=10,
#                                      release_date=datetime.date(1867, 1, 1)),
#                                 Book(name="Анна Каренина",
#                                      count=7,
#                                      release_date=datetime.date(1877, 1, 1))
#                                 ])
#         authors[2].book.extend([Book(name="Морфий",
#                                      count=5,
#                                      release_date=datetime.date(1926, 1, 1)),
#                                 Book(name="Собачье сердце",
#                                      count=3,
#                                      release_date=datetime.date(1925, 1, 1))
#                                 ])
#         session.add_all(authors)
#
#     if not session.query(Student).all():
#         students = [Student(name="Nik", surname="1", phone="2", email="3",
#                             average_score=4.5,
#                             scholarship=True),
#                     Student(name="Vlad", surname="1", phone="2", email="3",
#                             average_score=4,
#                             scholarship=True),
#                     ]
#
#         session.add_all(students)
#
#     if not session.query(ReceivingBook).all():
#         receiving_books = [
#             ReceivingBook(book_id=1, student_id=1, date_of_issue=datetime.date(2023, 3, 1)),
#             ReceivingBook(book_id=2, student_id=1, date_of_issue=datetime.date(2023, 4, 10),
#                           date_of_return=datetime.date(2023, 4, 13))
#         ]
#         session.add_all(receiving_books)
#
#     session.commit()
#
#
# def quantity_remaining_books(author_id):
#     return session.query(func.sum(Book.count)).filter(Book.author_id == author_id).one_or_none()
#
#
# def book_student_has_read(student_id):
#     check_stud = session.query(Student).filter(Student.id == student_id).one_or_none()
#     if check_stud:
#         subquery = session.query(ReceivingBook.book_id.label("book_id_sq")). \
#             filter(ReceivingBook.student_id == student_id).subquery()
#         return session.query(Book).filter(Book.id.not_in(subquery)).all()
#     else:
#         return None
#
#
# def avg_reading_books_by_month():
#     curr_month = session.query(func.count(), ReceivingBook, Student).join(Student).filter(
#         extract('year', ReceivingBook.date_of_issue) == datetime.date.today().year). \
#         filter(extract('month', ReceivingBook.date_of_issue) == datetime.date.today().month).group_by(
#         Student.id).subquery()
#     return session.query(func.round(func.avg(curr_month.c.count), 2)).select_from(curr_month).scalar()
#
#
# def top_books():
#     subquery = session.query(func.count().label("count_books"), ReceivingBook.book_id).join(Student). \
#         filter(Student.average_score >= 4).group_by(ReceivingBook.book_id). \
#         order_by(desc("count_books")).limit(1).subquery()
#     return session.query(Book).filter(Book.id == subquery.c.book_id).scalar()
#
#
# def top_10_readers_curr_year():
#     subquery = session.query(func.count().label("took_books"), ReceivingBook.student_id). \
#         filter(extract('year', ReceivingBook.date_of_issue) == datetime.date.today().year). \
#         group_by(ReceivingBook.student_id).order_by(desc("took_books")).limit(10).all()
#
#     stud_tpl = tuple(i[1] for i in subquery)
#     return session.query(Student).filter(Student.id.in_(stud_tpl)).all()
#
#
# # def mass_insertion_students(stud_lts):
# #     session.bulk_insert_mappings(Student, stud_lts)
# #     session.commit()
# #     return session.query(Student).all()
#
#

if __name__ == "__main__":
    Base.metadata.create_all(engine)