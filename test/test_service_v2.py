from service_v2 import my_service_with_dep_injection


# This is a bit of a side track. It does poor-mans dependency injection, so we don't have to mock anything
def test_my_service_v2():
    def my_repository():
        return False

    assert my_service_with_dep_injection(my_repository) == False
