from django.db import models
from datetime import datetime

# Create your models here.
class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"

def load_data():
    Voter.objects.all().delete()
    filename = 'voter_analytics/data/newton_voters.csv'
    f = open(filename, 'r')
    headers = f.readline() 

    for line in f:
        fields = [field.strip() for field in line.split(",")]
        voter = Voter()
        voter.last_name = fields[1]
        voter.first_name = fields[2]
        voter.street_number = fields[3]
        voter.street_name = fields[4]
        voter.apartment_number = fields[5]
        voter.zip_code = fields[6]
        voter.date_of_birth = fields[7]
        voter.date_of_registration = fields[8]
        voter.party_affiliation = fields[9] 
        voter.precinct_number = fields[10]
        voter.v20state = fields[11].lower() == 'true' 
        voter.v21town = fields[12].lower() == 'true'
        voter.v21primary = fields[13].lower() == 'true'
        voter.v22general = fields[14].lower() == 'true'
        voter.v23town = fields[15].lower() == 'true'
        voter.voter_score = int(fields[16]) 
        voter.save()
        print(f'Created result: {voter}')
