import json
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core import serializers
from .models import Vendor


class BurritoViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            vendor_data = request.data["vendorData"]
            vendor = Vendor(
                name=vendor_data["name"],
                description=vendor_data["review"],
                url=vendor_data["url"],
                img_url=vendor_data["imageUrl"],
                rating=vendor_data["rating"]
            )
            vendor.save()
        except Exception as e:
            print(f"Error: {e}")
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
            vendors = Vendor.objects.all()
            data = serializers.serialize('json', vendors)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to get items: {e}"},
                status=status.HTTP_200_OK,
            )

    def retrieve(self, request, pk=None):
        try:
            print("Retrieving")
            vendor = Vendor.objects.get(pk=pk)
            response = vendor
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to retrieve item: {e}"},
                status=status.HTTP_200_OK,
            )

    def partial_update(self, request, pk=None):
        try:
            print(("here"))
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
            vendor_data = json.loads(request.data["vendorData"])
            vendor = Vendor.objects.get(pk=pk)
            vendor.name = vendor_data["name"]
            vendor.description = vendor_data["review"]
            vendor.url = vendor_data["url"]
            vendor.img_url = vendor_data["imageUrl"]
            vendor.rating = vendor_data["rating"]
            vendor.save()
        except Exception as e:
            print(e)
            return Response(
                {"responseType": "error", "status": f"Failed to update id {pk}: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"responseType": "complete", "job_id": pk}, status=status.HTTP_200_OK
        )
