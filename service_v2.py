
def my_service_with_dep_injection(my_repository):
    print('my_service_with_dep_injection - calling injected version of my_repository')
    return my_repository()
