import argparse
from functools import lru_cache
import sys
import csv
import pathlib
from invoke import run
import simplejson as json

DEFAULT_CODEOWNERS_FILE = 'CODEOWNERS'
DEFAULT_OWNERSHIP_THRESHOLD = 25

cache = lru_cache(maxsize=None)


class CodeOwnersUpdater:
    def __init__(
        self,
        files,
        owners,
        ownership_threshold=DEFAULT_OWNERSHIP_THRESHOLD,
        codeowners_filename=DEFAULT_CODEOWNERS_FILE
    ):
        self.files = files,
        self.original_codeowner_data = {}
        self.updated_codeowner_data = {}
        self.updated = False
        self.owners = owners
        self.ownership_threshold = ownership_threshold
        self.codeowners_file = codeowners_filename

        with open(self.codeowners_file,newline='') as csvfile:
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
            file_committers = self.get_committers_for_file(file)
            # Some files may be not meet committer threshold, so we ignore those.
            if file_committers:
                codeowners_data[file] = file_committers
        for key, value in self.original_codeowner_data.items():
            self.updated_codeowner_data[key] = codeowners_data.get(key, value)
        for key, value in codeowners_data.items():
            self.updated_codeowner_data[key] = value

        self.update_file(self.updated_codeowner_data)

    def update_file(self, updated_data):
        if updated_data != self.original_codeowner_data:
            with open(self.codeowners_file, 'w', newline='', encoding='utf-8') as csvfile:
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
        for key, value in self.owners.items():
            commiter_frequency = self.get_committer_line_frequency_percentage(key, filename)
            committer_line_frequency_map[value] = committer_line_frequency_map.get(value, 0) + commiter_frequency
        return [
            a[0] for a in sorted(
                committer_line_frequency_map.items(),
                key=lambda item: item[1]
            ) if a[1] > self.ownership_threshold
        ]

    def main(self):
        self.check_files(self.files)
        return 1 if self.updated else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--ownership_threshold')
    parser.add_argument('--codeowners_filename')
    args = parser.parse_args()
    files = args.filenames[0]
    ownership_threshold = int(args.ownership_threshold)
    codeowners_filename = args.codeowners_filename

    if len(files) == 0:
        parser.error('No filenames provided')
    try:
        owners_raw = pathlib.Path('.gitownrc').read_text('utf-8')
        owners = json.loads(owners_raw)
    except FileNotFoundError as e:
        message = "A .gitownrc file is required. Please see the github repo for details"
        raise Exception(message).with_traceback(e.__traceback__)

    codeowners = CodeOwnersUpdater(
        files,
        owners,
        ownership_threshold=ownership_threshold or DEFAULT_OWNERSHIP_THRESHOLD,
        codeowners_filename=codeowners_filename or DEFAULT_CODEOWNERS_FILE
    )
    codeowners.main()


if __name__ == '__main__':
    sys.exit(main())
