from .models import Document, DocumentHistory
from django.core.exceptions import ObjectDoesNotExist
import json
import datetime

class Logic():
    def get_documents(self):
        docs = Document.objects.values()
        return docs

    def get_revisions_by_title(self, title):
        try:
            docs = []
            for doc in DocumentHistory.objects.filter(title=title).values('title_id', 'createdDate'):
                doc["createdDate"] = doc["createdDate"].strftime("%Y-%m-%d %H:%M:%S")
                docs.append(doc)
            return docs
        except Exception:
            raise

    def post_document(self, title, content):
        try:
            doc = Document.objects.get(title=title)
            doc.content = content
            doc.save()
        except ObjectDoesNotExist:
            raise
        except Exception:
            raise


    def get_doc_by_timestamp(self, title, timestamp):
        try:
            doc = DocumentHistory.objects.filter(title=title, createdDate__lte=
                datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).last()
            return doc

        except Exception:
            raise

    def get_latest_version(self, title):
        try:
            doc = Document.objects.get(title=title)
            return doc
        except ObjectDoesNotExist:
            raise
        except Exception:
            raise

    def add_document(self, json_text):
        title = json_text["title"]
        content = json_text["content"]
        curr_date = datetime.datetime.now()
        new_doc, created = Document.objects.update_or_create(content=content, defaults={'title': title,
                                                                                        'createdDate': curr_date,
                                                                                        'content': content})
        new_doc.save()
        hist_doc = DocumentHistory.objects.create(title=new_doc, createdDate=curr_date, content=content)
        hist_doc.save()




