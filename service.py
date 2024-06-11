from repository import my_repository


def my_service():
    print('my_service - calling my_repository')
    return my_repository()
