#Image testing will be covered with selenium

def test_correct_ccie_report(test_client, login_reporter):

    data=dict(first_name='John', last_name='Doe', sup_fname='Super', sup_lname='Visor', crew='1234', date='2020-03-01', cleanup='Moderate', building_type='Residential', city='San Diego', state='California', street_address='5500 Campanile Drive', zipcode=92182, notes='SDSU')

    response = test_client.post('/reporter/ccie', data=data)
    assert response.status_code == 302

def test_state_address_mixmatch(test_client, login_reporter):
    data=dict(first_name='John', last_name='Doe', sup_fname='Super', sup_lname='Visor', crew='1234', date='2020-03-01', cleanup='Moderate', building_type='Residential', city='Phoenix', state='Arizona', street_address='5500 Campanile Drive', zipcode=92182, notes='SDSU')

    response = test_client.post('/reporter/ccie', data=data)
    assert response.status_code == 200