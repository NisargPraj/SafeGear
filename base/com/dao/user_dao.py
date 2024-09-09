from base import db, app
from base.com.vo.user_vo import UserVO


class UserDAO:
    def create_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()

    def get_user_by_username(self, username):
        return db.session.query(UserVO).filter(UserVO.username == username).first()

