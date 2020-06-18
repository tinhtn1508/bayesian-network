import graph
import argparse
import os
from typing import List


def handlerCommand(args: List[str]) -> None:
    print(args)
    # TODO


def checkedArguments(args: List[str]) -> str:
    if not os.path.exists(args[0]):
        return "[ERROR] The file {} does not exist.\n".format(args[0])
    if not os.path.exists(args[1]):
        return "[ERROR] The file {} does not exist.\n".format(args[1])
    if args[2] not in ["forward", "likelihood", "gibbs"]:
        return "[ERROR] Invalid algorithm: {}\n".format(args[2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="path file to model")
    parser.add_argument("-t", "--test", help="path file to queries")
    parser.add_argument(
        "-a", "--algorithm", default="forward", help="forward | likelihood | gibbs"
    )
    args = parser.parse_args()
    if args.model is None or args.test is None or args.algorithm is None:
        warning = "\nThe agruments [--model, --test, --algorithm] can not be empty\n"
        warning += "For more details, you can use the command [main.py -h]\n"
        print(warning)
        exit()

    err = checkedArguments([args.model, args.test, args.algorithm])
    if err is not None:
        print(err)
        exit()

    handlerCommand([args.model, args.test, args.algorithm])


if __name__ == "__main__":
    main()
