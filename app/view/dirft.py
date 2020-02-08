from app.libs.enums import PendingStatus

class DriftView:
    def __init__(self, drift, user_id):
        self.data = {}
        self.data.update(self.__parse(drift, user_id))

    @staticmethod
    def requester_or_gifter(drift, user_id):
        if drift.requester_id == user_id:
            return "requester"
        else:
            return "gifter"

    def __parse(self, drift, user_id):
        you_are = self.requester_or_gifter(drift, user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        return {
            "you_are": you_are,
            "drift_id": drift.ID,
            "book_title": drift.book_title,
            "book_author": drift.book_author,
            "book_img": drift.book_img,
            "date": drift.create_time.strftime("%Y-%m-%d"),
            "message": drift.message,
            "address": drift.address,
            "recipient_name": drift.recipient_name,
            "mobile": drift.mobile,
            "status": drift.pending,
            "operator": drift.requester_nickname if you_are != "requester" else drift.gifter_nickname,
            "status_str": pending_status
        }


class DriftCollection:
    def __init__(self, drifts, user_id):
        self.data = []
        self.data.extend(self.__parse(drifts, user_id))

    def __parse(self, drifts, user_id):
        return [DriftView(drift, user_id).data for drift in drifts]
    
