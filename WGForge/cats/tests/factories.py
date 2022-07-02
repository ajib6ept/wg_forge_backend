import factory
import random
from faker import Factory
from WGForge.cats.models import Cats

faker = Factory.create()

CAT_COLORS = ("red & white", "black & white", "black", "red & black & white")


class CatsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cats

    name = factory.Sequence(lambda n: "Cat%s" % n)
    color = factory.LazyFunction(lambda: random.choice(CAT_COLORS))
    tail_length = factory.LazyFunction(lambda: random.randrange(1, 15))
    whiskers_length = factory.LazyFunction(lambda: random.randrange(1, 15))
