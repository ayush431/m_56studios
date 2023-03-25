from .serializer import StatusSerializer
from .model import status_log
class StatusController():
    def save_status_log(self, qn_id, questionObj, user_id):
        if not questionObj.get("old_status") == questionObj.get("status"):
            status_data = {
                "old_status": questionObj["old_status"],
                "new_status": questionObj["status"],
                "qn_id": qn_id,
                "user_id": user_id
            }
            return self.save_data(obj=StatusSerializer(data=status_data))

    def save_data(self, obj):
        if obj.is_valid(raise_exception=True):
            obj.save()
            return obj.data
    
    def get_status_by_user_id(self, user_id, start_date, end_date):
        return StatusSerializer(status_log.objects.filter(user_id=user_id, created_at__date__gte=start_date, created_at__date__lte=end_date), many=True).data

    def get_status_bw_dates(self, start_date, end_date):
        return StatusSerializer(status_log.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date), many=True).data
