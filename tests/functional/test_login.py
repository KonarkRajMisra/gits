def test_reporter_login(test_client, new_reporter):

    response = test_client.post('/login_reporter', data=dict(email=new_reporter.email,password='12345678'))
    assert response.status_code == 200

