
books_authors_table = Table('association', Base.metadata,
    Column('auhtor_id', Integer, ForeignKey('left.id')),
    Column('book_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",secondary=association_table,
                    backref="parents")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)