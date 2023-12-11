"""database storage engine module
"""
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session

from ..base_model import Base, BaseModel


class DBStorage:
    """Database storage class
    """
    __engine = None
    __session = None

    from ..user import User
    from ..state import State
    from ..city import City
    from ..amenity import Amenity
    from ..place import Place
    from ..review import Review

    __classes = [User, State, City, Amenity, Place, Review]

    def __init__(self):
        """Initialization method of the DBStorage class
        """

        import os
        hbnb_mysql_user = os.environ.get("HBNB_MYSQL_USER")
        hbnb_mysql_pwd = os.environ.get("HBNB_MYSQL_PWD")
        hbnb_mysql_host = os.environ.get("HBNB_MYSQL_HOST")
        hbnb_env = os.environ.get("HBNB_ENV")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                                      .format("hbnb_dev", "hbnb_dev_pwd", "hbnb_dev_db"), pool_pre_ping=True)

        if hbnb_env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Query all objects of a provided class
        """
        obj_dict = {}
        if cls:
            for obj in self.__session.scalars(select(cls)):
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj.to_dict()
            return obj_dict
        for cls in DBStorage.__classes:
            for obj in self.__session.scalars(select(cls)):
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj.to_dict()
        return obj_dict

    def new(self, obj):
        """Adds a new object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj from  the current database session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session()
