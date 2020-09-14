import json
from dataclasses import asdict
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.core import serializers
from .models import Vendor, HighScore
from .tabletop.character import Character
from .tabletop.constants import Styles, Classes, Subclasses
from .models import Weapon
import logging


class BurritoViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            vendor_data = request.data["vendorData"]
            vendor = Vendor(
                name=vendor_data["name"],
                description=vendor_data["review"],
                url=vendor_data["url"],
                img_url=vendor_data["imageUrl"],
                rating=vendor_data["rating"],
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
            data = serializers.serialize("json", vendors)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to get items: {e}"},
                status=status.HTTP_200_OK,
            )

    def retrieve(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            response = vendor
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to retrieve item: {e}"},
                status=status.HTTP_200_OK,
            )

    def update(self, request, pk=None):
        try:
            vendor_data = request.data["vendorData"]
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

    def delete(self, request, pk=None):
        try:
            Vendor.objects.get(id=pk).delete()
        except Exception as e:
            print(e)
            return Response(
                {"responseType": "error", "status": f"Failed to delete id {pk}: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"responseType": "complete", "job_id": pk}, status=status.HTTP_200_OK
        )


class SnakeViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data["data"]
            highScore, created = HighScore.objects.get_or_create(name=data["name"])
            if data["score"] > highScore.score:
                highScore.score = data["score"]
            highScore.save()
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
            highScores = HighScore.objects.all()
            data = serializers.serialize("json", highScores)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"responseType": "error", "status": f"Failed to get items: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CalculatorViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            data = Character(request.query_params).damage_data()
            data["weapons"] = list(Weapon.objects.values())
            data["fightingStyles"] = asdict(Styles())
            data["subclasses"] = asdict(Subclasses())
            data["classes"] = asdict(Classes())
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(e)
            return Response(
                {"responseType": "error", "status": f"Failed to get damage score: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
