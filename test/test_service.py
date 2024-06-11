from service import my_service


# This fails because we're mocking the wrong thing

def test_my_service(mocker):
    mocker.patch('repository.my_repository', return_value=False)
    assert my_service() == False
