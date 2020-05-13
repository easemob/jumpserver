# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.views import APIView

from common.permissions import IsValidUser
from rest_framework.response import Response


class UploadFileApi(APIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        f = request.FILES.get('local-file', None)
        path = settings.UPLOAD_DIR + '/' + f.name
        with open(path, 'wb') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
        return Response({"path": path, "filename": f.name, "size": f.size})


class DeleteFileApi(APIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        return Response({"path": 1})
