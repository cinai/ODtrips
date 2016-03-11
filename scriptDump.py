# python manage.py shell
import csv
from ODmaps.models import Transaction

fields = ['tiempo_subida','user_id','x_subida','y_subida','tipo_transporte','serviciosentidovariante','tipo_dia','nviaje','netapa','x_bajada','y_bajada','tiempo_bajada','par_subida','par_bajada','zona_subida','zona_bajada','adulto']
for row in csv.reader(open('etapas.csv')):
    Transaction.objects.create(**dict(zip(fields, row)))