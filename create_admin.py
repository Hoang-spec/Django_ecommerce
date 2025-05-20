from django.contrib.auth.models import User
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()


def create_superuser():
    try:
        # Xóa superuser cũ nếu có
        User.objects.filter(is_superuser=True).delete()

        # Tạo superuser mới
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123456'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f'Superuser "{username}" đã được tạo thành công!')
            print(f'Username: {username}')
            print(f'Password: {password}')
        else:
            print(f'Superuser "{username}" đã tồn tại!')

    except Exception as e:
        print(f'Có lỗi xảy ra: {str(e)}')


if __name__ == '__main__':
    create_superuser()
