from app import flask_app, log
from app.data import visit as mvisit
import datetime

def execute_test(args):
    try:
        test_code = flask_app.config['ENTER_TEST_CODE']
        if 'help' in args:
            return '''
            enter?code=umagbinnen : test gebruiker, gebruik test delay settings<br>
            enter?code=droogloop : test gebruiker, gebruik guest delay settings<br>
            test?umagbinnen=delay: test gebruiker (umagbinnen), timeslot wordt gezet op NU + delay<br> 
            '''
        if test_code in args:
            visit = mvisit.get_first_visit(code=test_code)
            delay = int(args[test_code])
            timeslot = datetime.datetime.now() + datetime.timedelta(seconds=delay)
            log.info(f'test ({test_code}/{timeslot})')
            mvisit.update_visit(visit, timeslot=timeslot)
        return f'test ({test_code}/{timeslot})'
    except Exception as e:
        log.error(f'test: could not do test {args}: {e}')
    return f'sorry, niet gelukt'