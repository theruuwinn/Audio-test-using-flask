

from application.compat import basestring
from application.extensions import db


Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    

    @classmethod
    def create(cls, **kwargs):
       
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    

    __abstract__ = True



class SurrogatePK(object):
    
    __table_args__ = {"extend_existing": True}
    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):

       
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.

	"""
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name), **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs
    )
