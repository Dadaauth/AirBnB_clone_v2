#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
                      )

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    amenities = relationship('Amenity', secondary='place_amenity', viewonly=False)

    reviews = relationship('Review', backref="place", cascade="all, delete-orphan")

    @property
    def reviews(self):
        from models import storage
        from review import Review
        return [review for review in storage.all(Review).values() if review.id == self.id]

    @property
    def amenities(self):
        from models import storage
        from amenity import Amenity
        return [amenity for amenity in storage.all(Amenity).values() if amenity.id == self.id]

    @amenities.setter
    def amenities(self, obj):
        from amenity import Amenity
        if type(obj) == Amenity:
            self.amenity_ids.append(obj.id)
