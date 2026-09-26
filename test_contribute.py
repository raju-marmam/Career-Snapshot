import unittest
import contribute
from subprocess import check_output


class TestContribute(unittest.TestCase):

    def test_arguments(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits, 9)
        self.assertTrue(3 <= contribute.contributions_per_day(args) <= 9)

    def test_contributions_per_day(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_default_weekday_activity_and_commit_range(self):
        args = contribute.arguments([])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits, 9)
        self.assertEqual(args.frequency, 100)
        self.assertTrue(3 <= contribute.contributions_per_day(args) <= 9)

    def test_commits(self):
        contribute.NUM = 11   # limiting the number only for unittesting
        contribute.main(['-nw',
                         '--user_name=sampleusername',
                         '--user_email=your-username@users.noreply.github.com',
                         '-mc=12',
                         '-fr=82',
                         '-db=10',
                         '-da=15'])
        self.assertTrue(1 <= int(check_output(
            ['git',
             'rev-list',
             '--count',
             'HEAD']
        ).decode('utf-8')) <= 20*(10 + 15))

    def test_repository_directory_name_without_git_suffix(self):
        self.assertEqual(
            contribute.repository_name('https://github.com/user/example'),
            'example'
        )
        self.assertEqual(
            contribute.repository_name('git@github.com:user/example.git'),
            'example'
        )

    def test_frequency_must_be_between_zero_and_hundred(self):
        with self.assertRaises(SystemExit):
            contribute.main(['--frequency=101'])
