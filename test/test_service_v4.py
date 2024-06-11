from service import my_service


# This also works because service has loaded a version of my_repository and that is the thing
# we're mocking here
def test_my_service(mocker):
    mocker.patch('service.my_repository', return_value=False)
    assert my_service() == False
