import operator

from django.db.models import Q
from django.conf import settings

from halalmas.server.objects.tags.models import Tag  # , TagGroup
from halalmas.server.hosts.branches.models import BranchTags, Branch

# qs = Company.objects.all()
# if self.q:
#     qs = qs.filter(
#         Q(branch_name__icontains=self.q) |
#         Q(branch_name__icontains=self.q) |
#         Q(branch_name__icontains=self.q)).order_by(
#         '-cdate')[:50]


class BranchTagsHalal(object):
    def __init__(self, *args, **kwargs):
        self.branch_filter_add = ['sapi', 'ikan', 'roti', 'bakery', 'pizza', 'cfc', 'burger king',
                                  'ayam', 'kfc', 'starbuck', 'solaria', 'donald', 'kopi', 'coffee']
        self.branch_filter_add = ['hokben',
                                  'bensu',
                                  'cost',
                                  'martabak',
                                  'A&W',
                                  'solaria',
                                  ]

        self.branch_filter_remove = ['ayam', ]
        self.bulk_max = 50

    def add_branch_tags(self):
        print(f'add_branch_tags')

        for branch_search in self.branch_filter_add:
            obj_data = Branch.objects.filter(
                branch_name__icontains=branch_search).order_by('id')
            cnt_ = obj_data.count()
            print(f'{branch_search} count data: {cnt_}')
            if cnt_ >= 1:
                # get Tag
                obj_tag = Tag.objects.get(tag='Halal')

                obj_b_tag_arr = []
                bulk_count = 0
                for obj_branch in obj_data:
                    # Add Branch Tags
                    obj_b_tag = BranchTags(branch=obj_branch, tag=obj_tag)
                    obj_b_tag_arr.append(obj_b_tag)

                    bulk_count = bulk_count + 1
                    if bulk_count >= self.bulk_max:
                        BranchTags.objects.bulk_create(obj_b_tag_arr)
                        print(
                            f'add branch tags with key: {branch_search} with count: {bulk_count} SUCCESS')

                        # reset bulk counter and array
                        obj_b_tag_arr = []
                        bulk_count = 0

                if len(obj_b_tag_arr) >= 1:
                    # insert bulk branch tag
                    BranchTags.objects.bulk_create(obj_b_tag_arr)
                    print(
                        f'add branch tags with key: {branch_search} with count: {bulk_count} SUCCESS')
                print(
                    f'add branch tags with key: {branch_search} SUCCESS')

        print(f'add_branch_tags DONE')

    def remove_branch_tags(self):
        print(f'remove_branch_tags')

        for branch_search in self.branch_filter_remove:
            obj_data = Branch.objects.filter(
                branch_name__icontains=branch_search).order_by('id')
            cnt_ = obj_data.count()
            print(f'count data: {cnt_}')
            if cnt_ >= 1:
                branch_id_remove = [item.pk for item in obj_data]
                # get Tag
                obj_tag = Tag.objects.get(tag='Halal')

                # insert bulk branch tag
                BranchTags.objects.filter(
                    branch__id__in=branch_id_remove, tag=obj_tag).delete()
                print(
                    f'remove branch tags with key: {branch_search} with count: {cnt_} SUCCESS')

        print(f'remove_branch_tags DONE')


def test_add():
    cls_branch_tag = BranchTagsHalal()
    cls_branch_tag.add_branch_tags()


def test_remove():
    cls_branch_tag = BranchTagsHalal()
    cls_branch_tag.remove_branch_tags()
