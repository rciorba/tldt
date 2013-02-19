import argparse

import tldt


def main():
    parser = argparse.ArgumentParser(description="cacat")
    parser.add_argument("head_repo")
    parser.add_argument("head_sha")
    parser.add_argument("base_repo")
    parser.add_argument("base_sha")
    args = parser.parse_args()
    tldt.main(head_repo=args.head_repo,
                   head_sha=args.head_sha,
                   base_repo=args.base_repo,
                   base_sha=args.base_sha)


if __name__ == '__main__':
    main()
