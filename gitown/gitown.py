import optparse
from functools import lru_cache
import sys
import csv
from invoke import run

CODEOWNERS_FILE = 'CODEOWNERS'
PERCENTAGE_THRESHOLD = 10

COMMITTERS = {
    'mshakya@tripadvisor.com': '@milind-shakya-sp',
    'mshakya@singleplatform.com': '@milind-shakya-sp',
    'sacharya@tripadvisor.com': '@sacharya-sp',
    'dpanofsky@tripadvisor.com': '@davidpanofsky',
    'dpanofsky@singleplatform.com': '@davidpanofsky',
    'ytoruno@tripadvisor.com': '@ytorunoSP',
    'ytoruno@singleplatform.com': '@ytorunoSP',
    'gchen@tripadvisor.com': '@ta-gchen',
    'krchen@tripadvisor.com': '@krchen-ta',
    'micmartine@tripadvisor.com': '@sp-mmartin',
    'mmartin@tripadvisor.com': '@sp-mmartin',
}


cache = lru_cache(maxsize=None)


class CodeOwnersUpdater:
    def __init__(self):
        self.original_codeowner_data = {}
        self.updated_codeowner_data = {}
        self.updated = False

        with open(CODEOWNERS_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                try:
                    if row[0] == '#':
                        continue
                except IndexError:
                    continue
                self.original_codeowner_data[row[0]] = row[1:]

    def check_files(self, files):
        codeowners_data = {}
        for file in files:
            codeowners_data[file] = self.get_committers_for_file(file)
        for key, value in self.original_codeowner_data.items():
            self.updated_codeowner_data[key] = codeowners_data.get(key, value)
        for key, value in codeowners_data.items():
            self.updated_codeowner_data[key] = value

        self.update_file(self.updated_codeowner_data)

    def update_file(self, updated_data):
        if updated_data != self.original_codeowner_data:
            with open(CODEOWNERS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                csvfile.write("# Lines starting with '#' are comments.\n")
                csvfile.write("# Each line is a file pattern followed by one or more owners.\n")
                csvfile.write("# These owners will be the default owners for everything in the repo.\n")
                csvfile.write("# * <@insert_github_username>\n")
                csvfile.write("#\n")
                csvfile.write("# Order is important. The last matching pattern has the most precedence.\n")
                csvfile.write("\n")

                writer = csv.writer(csvfile, delimiter=' ', lineterminator='\n')
                for key, value in updated_data.items():
                    writer.writerow([key] + value)
            self.updated = True

    def get_committer_line_frequency_percentage(self, committer_email, filename):
        blame_file_content = self.get_blame_file_content(filename)
        total_lines = blame_file_content.count('\n')
        total_lines_by_committer = blame_file_content.count(committer_email)
        return (total_lines_by_committer / total_lines) * 100

    @cache
    def get_blame_file_content(self, filename):
        return run(f"git blame {filename} -e", hide=True).stdout

    def get_committers_for_file(self, filename):
        """
        Returns a list of committers usernames sorted by blame frequency
        """
        committer_line_frequency_map = {}
        for key, value in COMMITTERS.items():
            commiter_frequency = self.get_committer_line_frequency_percentage(key, filename)
            committer_line_frequency_map[value] = commiter_frequency
        return [
            a[0] for a in sorted(
                committer_line_frequency_map.items(),
                key=lambda item: item[1]
            ) if a[1] > PERCENTAGE_THRESHOLD
        ]

    def main(self):
        parser = optparse.OptionParser(
            usage='%prog [options] file [files]',
            description='Updates CODEOWNERS File'
        )
        (opts, files) = parser.parse_args()

        if len(files) == 0:
            parser.error('No filenames provided')

        self.check_files(files)
        return 1 if self.updated else 0


if __name__ == '__main__':
    codeowners = CodeOwnersUpdater()
    sys.exit(codeowners.main())
