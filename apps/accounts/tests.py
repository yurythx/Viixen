from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import CustomUser
from .forms import CustomUserCreationForm, EditProfileForm

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertFalse(self.user.is_active)
        self.assertTrue(self.user.check_password('testpass123'))

    def test_get_avatar_url_no_avatar(self):
        self.assertEqual(self.user.get_avatar_url(), '/static/img/default_avatar.png')

class CustomUserCreationFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'weak',  # senha muito curta
            'password2': 'weak'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_duplicate_email(self):
        # Criar um usuário primeiro
        CustomUser.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )

        # Tentar criar outro usuário com o mesmo email
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # email duplicado
            'password1': 'strongpass123',
            'password2': 'strongpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class EditProfileFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_valid_avatar_upload(self):
        # Criar um arquivo de imagem simulado
        avatar = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'',  # conteúdo vazio para teste
            content_type='image/jpeg'
        )

        form_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        form_files = {'avatar': avatar}
        
        form = EditProfileForm(data=form_data, files=form_files, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_large_avatar_upload(self):
        # Criar um arquivo de imagem grande simulado (>2MB)
        large_avatar = SimpleUploadedFile(
            name='large_avatar.jpg',
            content=b'x' * (2 * 1024 * 1024 + 1),  # 2MB + 1 byte
            content_type='image/jpeg'
        )

        form_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        form_files = {'avatar': large_avatar}
        
        form = EditProfileForm(data=form_data, files=form_files, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('avatar', form.errors)


class LDAPAuthTests(TestCase):
    @patch('apps.accounts.auth_backends.LDAPBackend.authenticate')
    def test_ldap_auth_success(self, mock_auth):
        mock_auth.return_value = UserFactory()
        response = self.client.post(reverse('login'), {
            'username': 'ldap_user', 
            'password': 'valid_pass'
        })
        self.assertEqual(response.status_code, 302)
