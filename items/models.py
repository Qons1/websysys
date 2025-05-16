from django.db import models
from django.conf import settings
from bson import ObjectId

class Item:
    def __init__(self, _id=None, name="", description="", price=0.0, image="", user_id=None, username="", created_at=None):
        self._id = _id if _id else str(ObjectId())
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.user_id = user_id
        self.username = username
        self.created_at = created_at
        
    @property
    def id(self):
        return self._id

    @classmethod
    def from_mongo(cls, mongo_doc):
        if not mongo_doc:
            return None
        
        return cls(
            _id=str(mongo_doc.get('_id')),
            name=mongo_doc.get('name', ''),
            description=mongo_doc.get('description', ''),
            price=mongo_doc.get('price', 0.0),
            image=mongo_doc.get('image', ''),
            user_id=mongo_doc.get('user_id'),
            username=mongo_doc.get('username', ''),
            created_at=mongo_doc.get('created_at')
        )

    def to_mongo(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'image': self.image,
            'user_id': self.user_id,
            'username': self.username,
            'created_at': self.created_at
        }
