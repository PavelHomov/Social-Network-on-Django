import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import PostForm
from ..models import Group, Post, User, Comment


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='TestAuthor')
        cls.auth_user = User.objects.create_user(username='TestAuthUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст поста',
            group=cls.group,
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.auth_user)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(PostCreateFormTests.author)

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        posts = set(Post.objects.all())
        image = SimpleUploadedFile(
            name='1_small.gif',
            content=(
                b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
            ),
            content_type='image/gif'
        )
        form_data = {
            'text': 'Введенный в форму текст',
            'group': self.group.pk,
            'image': image,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:profile', kwargs={'username': self.auth_user.username}
            )
        )
        new_posts = set(Post.objects.all())
        difference_sets_of_posts = new_posts.difference(posts)
        self.assertEqual(len(difference_sets_of_posts), 1)
        last_posts = difference_sets_of_posts.pop()
        self.assertEqual(last_posts.text, form_data['text'])
        self.assertEqual(last_posts.group.pk, form_data['group'])
        self.assertEqual(last_posts.image, 'posts/1_small.gif')
        self.assertEqual(last_posts.author, self.auth_user)

    def test_author_edit_post(self):
        """Валидная форма изменяет запись в Posts."""
        new_group = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug2',
            description='Тестовое описание 2',
        )
        self.authorized_client_author.get(f'/posts/{self.post.pk}/edit/')
        form_data = {
            'text': 'Отредактированный в форме текст',
            'group': new_group.pk,
        }
        response = self.authorized_client_author.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        post_edit = Post.objects.get(id=self.group.pk)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(post_edit.text, form_data['text'])
        self.assertEqual(post_edit.group.pk, form_data['group'])
        self.assertEqual(post_edit.author, self.author)

    def test_create_comment(self):
        """Валидная форма создает комментарий."""
        comments = set(Comment.objects.all())
        form_data = {
            'author': self.auth_user,
            'text': 'Новый комментарий',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            )
        )
        new_comments = set(Comment.objects.all())
        difference_sets_of_comments = new_comments.difference(
            comments
        )
        self.assertEqual(len(difference_sets_of_comments), 1)
        last_comments = difference_sets_of_comments.pop()
        self.assertEqual(last_comments.text, form_data['text'])
        self.assertEqual(last_comments.author, form_data['author'])

    def test_commenting_is_available_only_authorized_user(self):
        """Комментирование доступно только авторизованному пользователю."""
        form_data = {
            'text': 'Комментарий',
        }
        response_authorized = self.authorized_client.get(
            reverse('posts:add_comment', kwargs={
                'post_id': self.post.pk}
            ),
            data=form_data,
            follow=True
        )
        self.assertEqual(response_authorized.status_code, HTTPStatus.OK)
        response_not_authorized = self.client.get(
            reverse('posts:add_comment', kwargs={
                'post_id': self.post.pk}
            ),
            data=form_data
        )
        self.assertEqual(
            response_not_authorized.status_code,
            HTTPStatus.FOUND
        )
