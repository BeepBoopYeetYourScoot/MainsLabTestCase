from rest_framework.viewsets import ViewSet
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bill
from .serializers import BillSerializer
import pandas as pd


class BillViewSet(ViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    def list(self, request):
        """
        List all the Bills in the DB.
        Provides filters for 'client_name' and 'client_org' fields.
        Can be done with FilterBackend but I don't have the time to debug it
        """
        queryset = self.queryset
        if 'client_name' in request.query_params:
            queryset = queryset.filter(client_name=request.query_params['client_name'])
        if 'client_org' in request.query_params:
            queryset = queryset.filter(client_org=request.query_params['client_org'])

        serialized_model_data = self.serializer_class(queryset, many=True).data
        return Response(data=serialized_model_data, status=status.HTTP_200_OK)

    @parser_classes([FileUploadParser])
    def create(self, request):
        """
        Create Bills using provided Excel file.
        Saves all correct rows and returns errors on invalid rows.
        Can be optimized by using bulk creation of the model but the logic will be much wider than it is right now
        """
        uploaded_file = request.data['file']
        bills_df = pd.read_excel(uploaded_file).rename(columns={'№': 'number'})

        invalid_rows = []

        # Making sure we upload all rows that are valid and collecting all the incorrect rows
        for index, row in bills_df.iterrows():
            serializer = self.serializer_class(data=row.to_dict())
            if serializer.is_valid():
                serializer.save()
            else:
                invalid_rows.append({'row': index + 1, 'errors': serializer.errors})

        if any(invalid_rows):
            return Response(invalid_rows, status=status.HTTP_207_MULTI_STATUS)
        return Response(status=status.HTTP_200_OK)
