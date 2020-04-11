import json
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class IndexViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            request_data = json.loads(request.data["data"])
            print(request_data)
        except Exception as e:
            return Response(
                {
                    "responseType": "error",
                    "status": f"Failed to submit data: {repr(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"responseType": "complete", "job_id": 1}, status=status.HTTP_200_OK
        )

    def list(self, request):
        try:
            items = []
            return Response(json.dumps(items), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to get items: {e}"},
                status=status.HTTP_200_OK,
            )

    def retrieve(self, request, pk=None):
        try:
            response = {}
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to retrieve item: {e}"},
                status=status.HTTP_200_OK,
            )

    def partial_update(self, request, pk=None):
        try:
            pass
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to modify id {pk}: {e}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"responseType": "complete", "job_id": pk}, status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        try:
            pass
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to update Id {pk}: {e}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"responseType": "complete", "job_id": pk}, status=status.HTTP_200_OK
        )
