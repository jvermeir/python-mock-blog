from service_v5 import my_service


# And this works because service_v5 imports the repository file and we can
# therefore mock repository.my_repository
def test_my_service(mocker):
    mocker.patch('repository.my_repository', return_value=False)
    assert my_service() == False
