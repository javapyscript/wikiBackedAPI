from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from .logic import Logic

import datetime
from .models import Document, DocumentHistory
lg = Logic()

#The method below is not part of the assignment but was used to add some docs to the db
@api_view(["POST"])
def add_document(request):
    json_text = json.loads(request.body)
    lg.add_document(json_text)

@api_view(["GET"])
def get_documents(request):
    docs = lg.get_documents()
    if len(docs)>0:
        docs = [doc["title"] for doc in docs]
        return Response({"data": docs}, status.HTTP_200_OK)
    else:
        return Response({"Warning": "No such document exists"}, status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def get_revisions_by_title(request, title):
    if request.method == "POST":
        try:
            content = json.loads(request.body)
            if "content" in content.keys():
                lg.post_document(title, ["content"])
                return Response({"message": "Document Updated"}, status.HTTP_200_OK)
            else:
                return Response({"Error": "Invalid Content format"}, status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"Warning": "No such document exists"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"Error": "Operation failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        try:
            docs = lg.get_revisions_by_title(title)
            if len(docs)>0:
                return Response({"versions": docs}, status.HTTP_200_OK)
            else:
                return Response({"Warning": "No such document exists"}, status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"Warning": "No such document exists"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"Error": "Operation failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_doc_by_timestamp(request, title, timestamp):

    try:
        doc = lg.get_doc_by_timestamp(title, timestamp)
        if doc is not None:
            return Response({"content": getattr(doc, "content")}, status.HTTP_200_OK)
        else:
            return Response({"Warning": "No such document exists"}, status.HTTP_204_NO_CONTENT)

    except Exception:
        return Response({"Error": "Operation failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_latest_version(request, title):
    try:
        doc = lg.get_latest_version(title)
        return Response({"content": getattr(doc, "content")}, status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"Warning": "No such document exists"}, status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response({"Error": "Operation failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR)