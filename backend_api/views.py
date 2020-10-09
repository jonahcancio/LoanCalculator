from backend_api.serializers import CalcSerializer, InquirerSerializer

from .models import Calculation, Inquirer
from rest_framework.views import APIView
from rest_framework.response import Response

import numpy_financial as npf
from datetime import date
import datedelta
from dateutil.parser import parse






class CalculateView(APIView):

    # Effective Annual Interest Rate
    eair = 0.24 / 12

    # handle get requests to the calculator
    # queries database for previous calculations
    def get(self, request, format=None):
        calc_obj = Calculation.objects.all()
        print(request.query_params)
        if ('type' in request.query_params):
            calc_obj = calc_obj.filter(loan_type=request.query_params['type'])
        
        serializer = CalcSerializer(calc_obj, many=True)
        return Response(serializer.data)

    # handle post requests to the calculator
    # triggers the calculation functions and saves to database
    def post(self, request, format=None):
        data = request.data
        errors = {}

        # processing and error checking for loan types
        if ('loan_type' in data and data['loan_type'] == 'A'):
            data = self.calculate_typeA(data)
        elif ('loan_type' in data and data['loan_type'] == 'B'):
            data = self.calculate_typeB(data)
        else:
            errors['loan_type'] = 'Invalid Loan Type'

        # processing and error checking for loan dates
        if ('loan_start_date' in data and self.is_date_parsable(data['loan_start_date'])):
            data = self.calculate_loan_dates(data)
        else:
            errors['loan_start_date'] = 'Invalid Loan Start Date'

        if (errors):
            return Response(errors, 400)

        saved_calc = self.save_to_database(data)
        if (not saved_calc):
            errors['database'] = "failed to store in database"
            errors['data'] = saved_calc
            return Response(errors, 400)


        return Response(data, 200)

    # calculates monthly_amortization for typeA loans using PMT function
    # result is added to data
    def calculate_typeA(self, data):
        data['monthly_amortization'] = npf.pmt(
            self.eair, data['loan_term'], -data['principal_amount'])
        data['sum_payments'] = data['monthly_amortization'] * data['loan_term']
        data['total_interest'] = data['sum_payments'] - \
            data['principal_amount']
        return data

    # calculates principal_amount for typeB loans using PV function
    # result is added to data
    def calculate_typeB(self, data):
        data['principal_amount'] = npf.pv(
            self.eair, data['loan_term'], -data['monthly_amortization'])
        data['sum_payments'] = data['monthly_amortization'] * data['loan_term']
        data['total_interest'] = data['sum_payments'] - \
            data['principal_amount']
        return data

    # returns true if string can be parsed into date
    def is_date_parsable(self, string):
        try:
            parse(string)
            return True
        except:
            return False

    # calculates future loan dates based on loan_start_date
    # result is added to data
    def calculate_loan_dates(self, data):
        loan_start_date = date.fromisoformat(data['loan_start_date'])
        first_payment_date = loan_start_date + datedelta.MONTH
        if (loan_start_date.day <= 15):
            first_payment_date = first_payment_date.replace(day=7)
        else:
            first_payment_date = first_payment_date.replace(day=22)

        loan_maturity_date = first_payment_date + \
            (data['loan_term'] - 1) * datedelta.MONTH

        data['first_payment_date'] = first_payment_date
        data['loan_maturity_date'] = loan_maturity_date
        return data

    # saves calculated data to the database
    # adds a new inquirer if full_name is given
    # returns the data of the newly saved calc_object
    def save_to_database(self, data):
        inquirer_name = 'full_name' in data and data['full_name'] or None
        inquirer_obj = None
        if (inquirer_name):
            inquirer_obj, _ = Inquirer.objects.update_or_create(full_name=data['full_name'], defaults={
                'email': data['email'],
                'mobile_number': data['mobile_number'],
                'city': data['city'],
                'province': data['province']
            })

        calc_obj = Calculation.objects.create(**{
            'loan_type': data['loan_type'],
            'principal_amount': data['principal_amount'],
            'monthly_amortization': data['monthly_amortization'],
            'total_interest': data['total_interest'],
            'loan_term': data['loan_term'],
            'sum_payments': data['sum_payments'],
            'loan_start_date': data['loan_start_date'],
            'first_payment_date': data['first_payment_date'],
            'loan_maturity_date': data['loan_maturity_date'],
            'inquirer': inquirer_obj
        })
        return CalcSerializer(calc_obj).data
