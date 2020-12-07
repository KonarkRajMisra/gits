
def test_gr_correct_backend(test_client, login_inspector):

    data = dict(search="John")

    response = test_client.post('/inspector/gr/',data=data)

    assert response.status_code == 302

def test_gr_incorrect_backend(test_client, login_inspector):

    data = dict(search="#_#_$")

    response = test_client.post('/inspector/gr/',data=data)

    assert response.status_code == 200
