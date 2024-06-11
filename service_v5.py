import repository


def my_service():
    print('my_service - calling my_repository')
    return repository.my_repository()
