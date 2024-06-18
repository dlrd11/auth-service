from sqlalchemy import Column, String, Integer
from passlib.context import CryptoContext
from database import Base

pwd_contest = CryptoContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)

    def set_password(self, password):
        self.hashed_password = pwd_contest.encrypt(password)

    def verify_password(self, password) -> bool:
        return pwd_contest.verify(password, self.hashed_password)
