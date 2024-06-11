from service_v3 import my_service


# This works because service_v3 defines both the service and the repository.
# And we're mocking the version of my_repository defined in service_v3.py.
def test_my_service(mocker):
    mocker.patch('service_v3.my_repository', return_value=False)
    assert my_service() == False
