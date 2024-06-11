def my_repository():
    print('my_repository - this is the real thing')
    return True


def my_service():
    print('my_service - calling my_repository')
    return my_repository()
