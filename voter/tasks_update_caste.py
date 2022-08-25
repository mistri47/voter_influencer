
from unicodedata import category
from .models import Caste, Voter

def update_caste():
    castes = Caste.objects.all()
    other_caste = Caste.objects.get(title='OTHER', category='GENERAL')

    voters = Voter.objects.filter(caste=None, data_hin__isnull=False)[:100]
    for voter in voters:
        for caste in castes:
            surnames = caste.related_surnames.split(",")
            for surname in surnames:
                print(surname)
                if surname in voter.data_hin:
                    voter.caste = caste
                    voter.category = caste.category
                    voter.save()
                    print(caste.title)
        if voter.caste is None:
            voter.caste=other_caste
            voter.save()
        
