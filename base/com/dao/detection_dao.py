from datetime import datetime

from base import db, app
from base.com.vo.detection_vo import DetectionVO


class DetectionDAO:

    def save(self, detection_vo):
        db.session.add(detection_vo)
        db.session.commit()

    def view(self):
        return DetectionVO.query.filter(DetectionVO.is_deleted == 0).all()

    def soft_delete(self, detection_id, user_id):
        detection_table = DetectionVO.query.get(detection_id)

        if detection_table:
            detection_table.is_deleted = 1
            detection_table.modified_by = user_id
            detection_table.modified_on = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            db.session.commit()