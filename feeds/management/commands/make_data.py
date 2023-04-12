from django.core.management.base import BaseCommand
from feeds.models import Feed
from groups.models import Group
from users.models import User
import random
from categories.models import Category
from faker import Faker


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 테스트 유저 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=0,
            type=int,
            help="몇개의 게시글을 등록",
        )
        parser.add_argument(
            "--group",
            default="오즈코딩스쿨",
            type=str,
            help="몇개의 게시글을 등록",
        )

    def handle(self, *args, **options):
        total, group = options.get("total"), options.get("group")
        group = Group.objects.get_or_create(name=group)
        if User.objects.count() == 0:
            self.stdout.write(self.style.SUCCESS("유저를 먼저 생성해주세요."))
            return
        # Feed.objects.create(
        #     user=User.objects.get(
        #         pk=random.choice([i for i in range(User.objects.count() - 1)])
        #     ),
        #     group= group
        #     category = Category.objects.get(
        #         pk=random.choice([i for i in range(Category.objects.count() - 1)])
        #     )
        # )
        fake = Faker(["ko_KR"])
        print(fake.building_name())
