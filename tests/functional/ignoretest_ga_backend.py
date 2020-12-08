

def test_correct_ga_query(test_client, login_inspector):

    data = dict(start_date='12/6/20',end_date='12/6/20',start_gps_lat=33.0,start_gps_lng=33.0,end_gps_lat=33.0,end_gps_lng=33.0,suspect_name="John Doe",gang_name="JailBreakers")

    response = test_client.post('/inspector/graffiti_analysis',data=data)

    assert response.status_code == 302

def test_incorrect_ga_query(test_client, login_inspector):

    data = dict(start_date='12/6/20',end_date='12/6/20',start_gps_lat='33.0',start_gps_lng='33.0',end_gps_lat='33.0',end_gps_lng='33.0',suspect_name="John Doe",gang_name="JailBreakers")

    response = test_client.post('/inspector/graffiti_analysis',data=data)
    assert response.status_code == 200

