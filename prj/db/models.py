from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = 'users2'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    test = Column(String)
    test2 = Column(String)


engine = create_engine('sqlite:///out/cc.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()

user_dict = {
    "name": "hoge",
    "email": "aiueo700",
    "test": "testdayo",
    "test2": "test22222",
}
new_user = User(**user_dict)
s.add(new_user)
s.commit()