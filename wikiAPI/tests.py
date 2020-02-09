from django.test import TestCase, RequestFactory
from .models import Document, DocumentHistory
from datetime import datetime
from .views import get_revisions_by_title, get_doc_by_timestamp, get_latest_version, get_documents
import time
import json
from django.urls import reverse

class GetDocsTestCase(TestCase):
    def setUp(self):
        Document.objects.create(title="Test Doc 1", createdDate=datetime.now(), content="This is a test doc 1")
        Document.objects.create(title="Test Doc 2", createdDate=datetime.now(), content="This is a test doc 2")
        Document.objects.create(title="Test Doc 3", createdDate=datetime.now(), content="This is a test doc 3")
        Document.objects.create(title="Test Doc 4", createdDate=datetime.now(), content="This is a test doc 4")
        self.factory = RequestFactory()

    def test_return_all_docs(self):
        """Test to check if view 'get_documents' runs fine with ok params"""
        request = self.factory.get('documents/')
        response = get_documents(request)
        self.assertEqual(response.status_code, 200)

    def test_return_empty(self):
        """Test to check if the view """
        Document.objects.all().delete()
        request = self.factory.get('documents/')
        response = get_documents(request)
        self.assertEqual(response.status_code, 204)


class GetAllDocRevisionsTestCase(TestCase):
    def test_get_revisions(self):
        """Test to check if the get view 'get_revisions_by_title' runs fine with correct parameters"""

        self.factory = RequestFactory()
        title = "Test Doc 1"
        Document.objects.create(title=title, createdDate=datetime.now(), content="This is a test doc 1")
        doc = Document.objects.get(title=title)
        DocumentHistory.objects.create(title=doc, createdDate=datetime.now(), content="This is a test doc 1")
        request = self.factory.get('documents/Test Doc 1')
        response = get_revisions_by_title(request, "Test Doc 1")
        self.assertEqual(response.status_code, 200)

    def test_doc_doesnt_exist(self):
        """Test to check if the get view 'get_revisions_by_title' throws 204 error if doc does not exist"""

        self.factory = RequestFactory()
        request = self.factory.get('documents/Test Doc 1')
        response = get_revisions_by_title(request, "Test Doc 1")
        self.assertEqual(response.status_code, 204)

class GetDocByTimestamp(TestCase):

    def setUp(self):
        # Insert few versions of the same doc with diff timestamp
        title = "Demo doc"
        time1 = datetime.now()
        Document.objects.create(title=title, createdDate=time1, content="This is a test doc 1")
        self.doc = Document.objects.get(title=title)
        DocumentHistory.objects.create(title=self.doc, createdDate=time1, content="This is a test doc 1")
        DocumentHistory.objects.create(title=self.doc, createdDate=datetime.now(), content="This is a test doc 5")
        time.sleep(1)
        DocumentHistory.objects.create(title=self.doc, createdDate=datetime.now(), content="This is a test doc 6")
        time.sleep(1)
        DocumentHistory.objects.create(title=self.doc, createdDate=datetime.now(), content="This is a test doc 7")
        time.sleep(1)
        curr_time = datetime.now()
        DocumentHistory.objects.create(title=self.doc, createdDate=curr_time, content="This is a test doc 8")
        self.hist_doc = DocumentHistory.objects.get(title=title, createdDate=curr_time)

    def test_get_doc_by_timestamp(self):
        """Test to check if the view 'get_doc_by_timestamp' runs fine without errors"""

        self.factory = RequestFactory()
        strtimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request = self.factory.get('documents/Demo doc/' + strtimestamp + '/')
        response = get_doc_by_timestamp(request, self.doc, strtimestamp)
        self.assertEqual(response.status_code, 200)

    def test_correct_version(self):
        """Test to check if the view 'get_doc_by_timestamp' returns the correct version by timestamp"""

        doc_test = DocumentHistory.objects.filter(title=self.doc, createdDate__lte=datetime.now()).last()
        self.assertEqual(doc_test.createdDate, self.hist_doc.createdDate)


class GetLatestDocument(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_get_latest_doc(self):
        """Test to check if the view 'get_latest_version' runs fine with correct parameters"""
        Document.objects.create(title="Latest doc", createdDate=datetime.now(), content="This is a test doc 1")
        request = self.factory.get('documents/Latest doc')
        response = get_latest_version(request, "Latest doc")
        self.assertEqual(response.status_code, 200)

    def test_doc_doesnt_exist(self):
        """Test to check if the view 'get_latest_version' returns 204 if the doc doesnt exist"""

        request = self.factory.get('documents/Fastest doc')
        response = get_latest_version(request, "Fastest doc")
        self.assertEqual(response.status_code, 204)


class PostDocUpdate(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def testDocUpdate(self):
        """Test to check if the post view 'get_revisions_by_title' runs fine with good params"""

        Document.objects.create(title="Latest doc", createdDate=datetime.now(), content="This is a test doc 1")
        self.post_data = {"content": "This is an updated test doc 1"}
        request = self.factory.post('documents/Latest doc',
                                   data=json.dumps(self.post_data),
                                   content_type='application/json'
                                   )
        response = get_revisions_by_title(request, "Latest doc")
        self.assertEqual(response.status_code, 200)

    def testDocMissing(self):
        """Test to check if the post view 'get_revisions_by_title' returns 204 if doc missing"""
        self.post_data = {"content": "This is an updated test doc 1"}
        request = self.factory.post('documents/Missing doc',
                                    data=json.dumps(self.post_data),
                                    content_type='application/json'
                                    )
        response = get_revisions_by_title(request, "Missing doc")
        self.assertEqual(response.status_code, 204)



