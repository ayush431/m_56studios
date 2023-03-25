from django.db import connection
from common.utility import isValidFilterType
from app.status.controller import StatusController
from app.users.controller import UserController
from dateutil.parser import parse
from common.constant import CATEGORY_CHAPTER

class ManagerController():

    def sort_by_date(self, elem):
        return elem['date']
    
    def sort_by_label(self, elem):
        return elem['label']

    def sort_by_chapter(self, elem):
        return elem['chapter']

    def get_by_category(self, request):
        cursor = connection.cursor()
        filter_type = request.data.get('filter_type')
        filter_by = ''
        if filter_type == 1:
            filter_by = ' and status="For Review"'
        elif filter_type == 2:
            filter_by = ' and status="For Review" and resrc_url is not NULL'
        elif filter_type == 3:
            filter_by = ' and status="For Review" and resrc_url is NULL'
        elif filter_type == 4:
            filter_by = ' and status="Ready To Publish" and resrc_url is not NULL'
        elif filter_type == 5:
            filter_by = ' and status="Ready To Publish" and resrc_url is NULL'
        elif filter_type == 6:
            filter_by = ' and status="Published" and resrc_url is not NULL'
        elif filter_type == 7:
            filter_by = ' and status="Published" and resrc_url is NULL'


        query = '''SELECT category, COUNT(*) AS "Total", SUM(CASE WHEN difficulty_level="Easy" THEN 1 ELSE 0 END) AS "Easy", SUM(CASE WHEN difficulty_level="Medium" THEN 1 ELSE 0 END) AS "Medium", SUM(CASE WHEN difficulty_level="Hard" THEN 1 ELSE 0 END) AS "Hard", SUM(CASE WHEN difficulty_level="Very Hard" THEN 1 ELSE 0 END) AS "Very Hard", 1 FROM app_question where (((qn_submitted_date >= '{}' and qn_submitted_date <= '{}') or qn_submitted_date is NULL) {})  group by category  ORDER BY `app_question`.`category`  ASC'''.format(request.data.get('start_date'), request.data.get('end_date'), filter_by)
        cursor.execute(query)
        rows = cursor.fetchall()
        keys = ("label", "total", "easy", "medium", "hard", "very_hard", "chapter")
        results = [tuple(str(item) for item in t) for t in rows]
        response = []
        total = {
            'label': 'Total',
            'total': 0,
            'easy': 0,
            'medium': 0,
            'hard': 0,
            'very_hard': 0,
            'chapter': ''
        }
        response = []
        for result in results:
            each_result = dict(zip(keys,result))
            each_result["chapter"] = CATEGORY_CHAPTER[result[0]]
            response.append(each_result)
            try:
                total['total'] += int(result[1])
                total['easy'] += int(result[2])
                total['medium'] += int(result[3])
                total['hard'] += int(result[4])
                total['very_hard'] += int(result[5])
            except Exception:
                print('Exception occured while getting total')
        
        response.sort(key=self.sort_by_chapter)
        response.insert(0, total)
        
        return response


    def get(self, filter_type, start_date, end_date):
        if filter_type:
            if not isValidFilterType(filter_type):
                raise Exception("Invalid filter")
            cursor = connection.cursor()
            inactive_question_mapping = {}
            if filter_type == 'qn_submitted_date':
                filter_type = 'Date(created_at)'
            query = '''
                SELECT 
                    {}, 
                    COUNT(*), 
                    SUM(CASE WHEN status="Draft" and is_active=1 THEN 1 ELSE 0 END) AS "Draft", 
                    SUM(CASE WHEN status="For Review" and is_active=1 THEN 1 ELSE 0 END) AS "For Review", 
                    SUM(CASE WHEN status="Rejected" and is_active=1 THEN 1 ELSE 0 END) AS "Rejected", 
                    SUM(CASE WHEN status="Approved" and is_active=1 THEN 1 ELSE 0 END) AS "Approved", 
                    SUM(CASE WHEN status="Rejected" and is_active=1 and qn_rejected_by_reviewer THEN 1 ELSE 0 END) AS "Question Rejected", 
                    SUM(CASE WHEN status="Draft" and is_active=1 and img_rejected_by_reviewer THEN 1 ELSE 0 END) AS "Image Rejected", 
                    SUM(CASE WHEN status="Ready To Publish" and is_active=1 THEN 1 ELSE 0 END) AS "Ready To Publish", 
                    SUM(CASE WHEN status="Published" and is_active=1 THEN 1 ELSE 0 END) AS "Published",
                    SUM(CASE WHEN is_active=0 THEN 1 ELSE 0 END) AS "Inactive"
                FROM app_question 
                where 
                    (Date(created_at) >= '{}' and Date(created_at) <= '{}') or created_at is NULL  
                group by {}
                '''.format(filter_type, start_date, end_date, filter_type)
            cursor.execute(query)
            rows = cursor.fetchall()
            keys = ("label", "total", "draft", "for_review", "rejected", "approved", "question_rejected", "image_rejected", "ready_to_publish", "published", "inactive")
            results = [tuple(str(item) for item in t) for t in rows]
            response = []
            total = {
                'label': 'Total',
                'total': 0,
                'draft': 0,
                'for_review': 0,
                'rejected': 0,
                'approved': 0,
                'question_rejected': 0,
                'image_rejected': 0,
                'ready_to_publish': 0,
                'published': 0,
                'inactive': 0
            }
            for result in results:
                temp = dict(zip(keys,result))
                temp['inactive'] = int(inactive_question_mapping[result[0]]) if result[0] in inactive_question_mapping else int(result[10])
                temp['total'] = int(temp['draft']) + int(temp['for_review']) + int(temp['rejected']) + int(temp['approved']) + int(temp['question_rejected']) + int(temp['image_rejected']) + int(temp['ready_to_publish']) + int(temp['published']) + int(temp['inactive'])

                response.append(temp)
                try:
                    total['total'] += int(temp['total'])
                    total['draft'] += int(temp['draft'])
                    total['for_review'] += int(temp['for_review'])
                    total['rejected'] += int(temp['rejected'])
                    total['approved'] += int(temp['approved'])
                    total['question_rejected'] += int(temp['question_rejected'])
                    total['image_rejected'] += int(temp['image_rejected'])
                    total['ready_to_publish'] += int(temp['ready_to_publish'])
                    total['published'] += int(temp['published'])
                    total['inactive'] += int(temp['inactive'])
                except Exception as e:
                    print('Exception occured while getting total')
            response.sort(key=self.sort_by_label, reverse=True)
            response.insert(0, total)
            return response
        else:
            raise Exception("Missing query params filter_type")

    def get_editor(self, request):
        status_data = None
        cursor = connection.cursor()
        if request.data.get('filter') == 'Difficulty':
            filter_by = 'q.difficulty_level'
        else:
            filter_by = 'DATE(s.created_at)'
        query = '''SELECT 
                    {}, 
                    SUM(CASE WHEN s.old_status='DRAFT' and s.new_status='For Review' THEN 1 ELSE 0 END) as 'Submitted for review', 
                    SUM(CASE WHEN s.old_status='DRAFT' and s.new_status='Rejected' THEN 1 ELSE 0 END) as 'Rejected', 
                    SUM(CASE WHEN s.old_status='DRAFT' and s.new_status='Discarded' THEN 1 ELSE 0 END) as 'Discarded', 
                    SUM(CASE WHEN (q.resrc_url is NOT NULL and q.qn_id = s.qn_id_id and s.old_status='DRAFT' and s.new_status='For Review') THEN 1 ELSE 0 END) as 'qn image tagged',
                    SUM(CASE WHEN (q.resrc_url is NULL and q.qn_id = s.qn_id_id and s.old_status='DRAFT' and s.new_status='For Review') THEN 1 ELSE 0 END) as 'qn image not tagged'  
                from app_status_log as s 
                join app_question as q on s.qn_id_id = q.qn_id where 
                (s.created_at >= '{}' and s.created_at <= '{}') 
                group by {}'''.format(filter_by, parse(request.data.get('start_date')), parse(request.data.get('end_date')), filter_by)
        keys = ("date", "submitted_for_review", "rejected", "discarded", "qn_with_tagged_images", "qn_without_tagged_images")
        if request.data.get('user_email') == 'All':
            user_email = 'All'
        else:
            user_email = UserController().get_object_by_email(request.data.get('user_email'))
            if user_email:
                query = '''SELECT 
                            {}, 
                            SUM(CASE WHEN s.old_status='DRAFT' and s.new_status='For Review' THEN 1 ELSE 0 END) as 'Submitted for review', 
                            SUM(CASE WHEN s.old_status='DRAFT' and s.new_status='Rejected' THEN 1 ELSE 0 END) as 'Rejected', 
                            SUM(CASE WHEN s.old_status='DRAFT' and s.new_status='Discarded' THEN 1 ELSE 0 END) as 'Discarded', 
                            SUM(CASE WHEN (q.resrc_url is NOT NULL and q.qn_id = s.qn_id_id and s.old_status='DRAFT' and s.new_status='For Review') THEN 1 ELSE 0 END) as 'qn image tagged',  
                            SUM(CASE WHEN (q.resrc_url is NULL and q.qn_id = s.qn_id_id and s.old_status='DRAFT' and s.new_status='For Review') THEN 1 ELSE 0 END) as 'qn image not tagged'  
                        from app_status_log as s 
                        join app_question as q on
                        s.qn_id_id = q.qn_id 
                        where 
                            (s.created_at >= '{}' and s.created_at <= '{}') and s.user_id_id = '{}' 
                        group by {}'''.format(filter_by, parse(request.data.get('start_date')), parse(request.data.get('end_date')), str(user_email.user_id).replace('-', ''), filter_by)
            else:
                raise Exception('Cannot find specified user')
        group_by_date = {}
        cursor.execute(query)
        rows = cursor.fetchall()
        results = [tuple(str(item) for item in t) for t in rows]
        
        data_to_return = []
        total = {
            'date': 'Total',
            'total': 0,
            'submitted_for_review': 0,
            'rejected': 0,
            'discarded': 0,
            'qn_with_tagged_images': 0,
            'qn_without_tagged_images': 0
        }
        for result in results:
            value = dict(zip(keys,result))
            value["total"] = int(value["submitted_for_review"]) + int(value["rejected"]) + int(value["discarded"])
            total['total'] += int(value['total'])
            total['submitted_for_review'] += int(value['submitted_for_review'])
            total['rejected'] += int(value['rejected'])
            total['discarded'] += int(value['discarded'])
            total['qn_with_tagged_images'] += int(value['qn_with_tagged_images'])
            total['qn_without_tagged_images'] += int(value['qn_without_tagged_images'])
            data_to_return.append(value)
        data_to_return.sort(key=self.sort_by_date, reverse=True)
        data_to_return.insert(0, total)
        return data_to_return
    
    def get_flagged_questions(self, start_date, end_date):
        cursor = connection.cursor()
        query = '''
            SELECT 
                DATE(s.created_at),
                SUM(CASE WHEN s.new_status='FLAGGED' THEN 1 ELSE 0 END) as 'new_flagged',
                SUM(CASE WHEN (s.new_status='FLAGGED' and q.qn_id = s.qn_id_id and q.status='FLAGGED') THEN 1 ELSE 0 END) as 'total_flagged_in_mdb',
                SUM(CASE WHEN (s.new_status='FLAGGED' and q.qn_id = s.qn_id_id and q.status='Ready To Publish') THEN 1 ELSE 0 END) as 'flagged_changed_to_rtp',
                SUM(CASE WHEN (s.new_status='FLAGGED' and q.qn_id = s.qn_id_id and q.status='Rejected') THEN 1 ELSE 0 END) as 'flagged_changed_to_rej'  
            FROM app_status_log as s 
            JOIN app_question as q 
            ON s.qn_id_id = q.qn_id
            WHERE (s.created_at >= '{}' and s.created_at <= '{}') 
            GROUP BY DATE(s.created_at)'''.format(start_date, end_date)
        keys = ("date", "new_flagged", "total_flagged_in_mdb", "flagged_changed_to_rtp", "flagged_changed_to_rej")
        cursor.execute(query)
        rows = cursor.fetchall()
        results = [tuple(str(item) for item in t) for t in rows]
        data_to_return = []
        total = {
            'date': 'Total',
            'new_flagged': 0,
            'total_flagged_in_mdb': 0,
            'flagged_changed_to_rtp': 0,
            'flagged_changed_to_rej': 0
        }
        for result in results:
            value = dict(zip(keys,result))
            total['new_flagged'] += int(value['new_flagged'])
            total['flagged_changed_to_rtp'] += int(value['flagged_changed_to_rtp'])
            total['flagged_changed_to_rej'] += int(value['flagged_changed_to_rej'])
            total['total_flagged_in_mdb'] += int(value['total_flagged_in_mdb'])
            data_to_return.append(value)
        data_to_return.sort(key=self.sort_by_date, reverse=True)
        data_to_return.insert(0, total)
        return data_to_return    

