def test_correct_reporter_registration(test_client, new_reporter):

    response = test_client.post('/register_reporter', data=dict(email=new_reporter.email,password='12345678'))
    assert response.status_code == 302

def test_incorrect_reporter_registration(test_client, new_reporter):
    response = test_client.post('/register_reporter', data=dict(email=new_reporter.email,password='not_correct_password'))
    assert response.status_code == 200

def test_correct_inspector_registration(test_client, new_inspector):

    response = test_client.post('/register_inspector', data=dict(email=new_inspector.email,password='12345678'))
    assert response.status_code == 302

def test_incorrect_inspector_registration(test_client, new_inspector):

    response = test_client.post('/register_inspector', data=dict(email=new_inspector.email, password='not_correct_password'))
    assert response.status_code == 200
