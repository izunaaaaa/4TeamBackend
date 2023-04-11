from django.core.management.base import BaseCommand


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
