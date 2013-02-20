import argparse
import os.path
import ConfigParser

import tldt


def main():
    user_home = os.path.expanduser("~")
    parser = argparse.ArgumentParser(description="cacat")
    parser.add_argument("head_repo")
    parser.add_argument("head_sha")
    parser.add_argument("base_repo")
    parser.add_argument("base_sha")
    parser.add_argument("--configuration", default=os.path.join(user_home, "tldt.ini"))
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config.read(args.configuration)
    username = config.get("Auth", "username")
    password = config.get("Auth", "password")

    comment = tldt.Comment(username=username, password=password)
    runner = tldt.Project(head_repo=args.head_repo,
                          head_sha=args.head_sha,
                          base_repo=args.base_repo,
                          base_sha=args.base_sha,
                          config=config,
                          comment=comment)
    runner.tldt()

if __name__ == '__main__':
    main()
