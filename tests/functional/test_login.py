def test_correct_reporter_login(test_client, new_reporter):

    response = test_client.post('/login_reporter', data=dict(email=new_reporter.email,password='12345678'))
    assert response.status_code == 302

    response = test_client.get('/reporter/sign_out')
    assert response.status_code == 302

def test_incorrect_reporter_login(test_client, new_reporter):
    response = test_client.post('/login_reporter', data=dict(email=new_reporter.email,password='not_correct_password'))
    assert response.status_code == 200


def test_correct_inspector_login(test_client, new_inspector):
    response = test_client.post('/login_inspector', data=dict(email=new_inspector.email,password='12345678'))
    assert response.status_code == 302

    response = test_client.get('/inspector/sign_out')
    assert response.status_code == 302

def test_incorrect_inspector_login(test_client, new_inspector):
    response = test_client.post('/login_inspector', data=dict(email=new_inspector.email,password='not_correct_password'))
    assert response.status_code == 200

#Test if logging in with inspector fails on reporter login and vice versa
def test_inspector_on_reporter(test_client, new_inspector, new_reporter):
    response = test_client.post('/login_inspector', data=dict(email=new_reporter.email,password='12345678'))
    assert response.status_code == 200

    response = test_client.post('/login_reporter', data=dict(email=new_inspector.email,password='12345678'))
    assert response.status_code == 200