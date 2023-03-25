from app.question.serializer import QuestionSerializer
from app.question.model import question
from common.constant import MISSING_STATUS
from urllib.request import urlopen
from PIL import Image
import os
import boto3
import shutil
from background_task import background
import logging
logging.basicConfig(filename="log/log.log", format='%(asctime)s -- %(message)s', level=logging.INFO)

class ThumbnailController():
    def save_db(image_url_ar, qn_id):
        question.objects.filter(qn_id=qn_id).update(images_x=image_url_ar)

    @background()
    def generate_thumbnail(image_url, qn_id):
        logging.info('Started Uploading images to S3 bucket')
        logging.info("Qn id %s", qn_id)

        # Check if the image_url is actually an image
        if image_url is None:
            logging.info("No Image found %s", qn_id)
            return
        
        if ".jpeg" not in image_url and ".jpg" not in image_url and ".png" not in image_url:
            logging.info("resource url might contain invalid image content %s", qn_id)
            return

        try:
            # Setup AWS creds (this can run parallely)
            region_name = os.environ.get('REGION_NAME')
            bucket_name = os.environ.get('BUCKET_NAME')
            session = boto3.Session(
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                region_name=region_name
            )
            s3 = session.resource('s3')
            bucket = s3.Bucket(bucket_name)

            # Create local directory
            if not os.path.exists(qn_id):
                os.makedirs(qn_id)
            img = Image.open(urlopen(image_url))
            original_img = f"{qn_id}"+ "/" + qn_id + ".jpeg"
            # save original image
            img.save(original_img)

            size_dict = {
                "720p": 720,
                "480p": 480,
                "360p": 360,
                "240p": 240
            }

            # Upload original image
            bucket.upload_file(original_img, (qn_id +'/'+ qn_id + '.jpeg'))
            logging.info("Uploading for Qn id %s image %s", qn_id, qn_id +'/'+ qn_id + '.jpeg')
            
            base_url = "https://" + bucket_name + ".s3." + region_name + ".amazonaws.com/"
            aa = "https://stable-diffusion-dummy.s3.us-east-2.amazonaws.com/1237838738/resize_2023-03-22-00-20-20-149452.jpg"
            image_url_ar = []
            for each_size in size_dict:
                resoltuion = each_size
                basewidth = size_dict[each_size]

                # Define image dimenions based on aspect ratio
                wpercent = (basewidth/float(img.size[0]))
                height = int((float(img.size[1])*float(wpercent)))

                rgb_im = img.convert('RGB')
                img = rgb_im.resize((basewidth, height), Image.ANTIALIAS)
                img_name = qn_id + "_" + resoltuion + '.jpeg'
                local_path = f"{qn_id}"+ "/" + img_name
                img.save(local_path)
                full_url = base_url + qn_id + "/" + img_name
                image_url_ar.append(full_url)
                bucket.upload_file(local_path, (qn_id +'/'+ img_name))
                logging.info("Uploading for Qn id %s image %s", qn_id, full_url)
                
            logging.info("All images Uploaded successfully for qn_id %s", qn_id)
            original_img_full_url = base_url + original_img
            image_url_ar.append(original_img_full_url)
            ThumbnailController.save_db(image_url_ar, qn_id)

            shutil.rmtree(qn_id)
        except Exception as e:
            # Add exception to log
            logging.info("Exception while generating thumbnail %s %s", e, image_url)

    @background()
    def generate_thumbnails_for_status(status):
        filters = {}
        exclude = {}
        if status:
            filters['status'] = status
            filters['images_x__isnull'] = True
            all_qus = question.objects.filter(**filters, is_active=True).exclude(**exclude)            
            serializeobj = QuestionSerializer(all_qus, many=True)
            for serialize_data in serializeobj.data:
                # TODO: Add this under a async operation using queues
                ThumbnailController.generate_thumbnail(serialize_data["resrc_url"], serialize_data["qn_id"])

    def perform(self, status=None, qn_id=None):
        filters = {}
        exclude = {}
        if status:
            ThumbnailController.generate_thumbnails_for_status(status)
        elif qn_id:
            filters['qn_id'] = qn_id
            ques = question.objects.filter(**filters, is_active=True).exclude(**exclude).first()
            if ques:
                # TODO: Add this under a async operation using queues
                ThumbnailController.generate_thumbnail(ques.resrc_url, str(ques.qn_id))
        else:
            raise Exception(MISSING_STATUS)
