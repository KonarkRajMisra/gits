#Image testing will be apart of selenium testing

from gitsapp.models import Suspect, Report

def test_suspect_lookup(test_client, create_report, login_inspector, drop_suspects):
    response = test_client.post('/inspector/legi/1', data=dict
    (search_first_name='Test', search_last_name="Doe"))

    #Suspect does not exist yet
    assert response.status_code == 404

    #Add gang information and then create suspect
    response = test_client.post('/inspector/legi/1', data=dict(gang='CS Department', status='Identified'))

    assert Suspect.query.all()[0].gang == "CS Department"

def test_report_edit(test_client,create_report, login_inspector):
    response = test_client.post('/inspector/legi/1', data=dict(zipcode=92106, type_of_building='No Change', cleanup='No Change', investigation_status='No Change', street_address="5500 Campanile Drive"))

    assert Report.query.all()[0].zipcode == 92106