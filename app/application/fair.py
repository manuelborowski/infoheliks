from app import log
from app.data import fair as mfair, utils as mutils

def add_fair(school, wonder=''):
    try:
        fair = mfair.get_first_fair(school=school)
        if fair:
            return None
        fair = mfair.add_fair(school, wonder)
        return fair
    except Exception as e:
        mutils.raise_error(f'could not add fair {school}', e)
    return None


def update_fair_by_id(id, value):
    try:
        fair = mfair.get_first_fair(id=id)
        return mfair.update_fair(fair, wonder=value)
    except Exception as e:
        mutils.raise_error(f'could not update fair {id}, {value}', e)
    return None


add_fair('Campus Sint-Ursula')
add_fair('Vrij Technisch Instituut')
add_fair(('Sint-Aloysiusinstituut'))
add_fair(('Sint-Aloysiusinstituut internaat'))
add_fair(('De Regenboog'))
add_fair(('Sint-Gummaruscollege'))
add_fair(('CLB'))

# De wonderkamers: SAL internaat – CLB – SAL – DR - SGC – Campus Sint-Ursula – VTI. Schoolmedewerkers moeten inderdaad een keuze maken.

