import factory
from django.contrib.auth.models import User

from posts.models import Category, Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "username-%d" % n)
    password = factory.Sequence(lambda n: "password-%d" % n)
    first_name = factory.Sequence(lambda n: "firstname-%d" % n)
    last_name = factory.Sequence(lambda n: "lastname-%d" % n)
    email = factory.Sequence(lambda n: "email%d@test.com" % n)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    tag = factory.Sequence(lambda n: "tag-%d" % n)
    name = factory.Sequence(lambda n: "test-tag-name-%d" % n)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        skip_postgeneration_save = True

    title = factory.Sequence(lambda n: "title-%d" % n)
    content = factory.Sequence(lambda n: "content-%d" % n)

    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.categories.add(*extracted)
