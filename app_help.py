import argparse

def main():
    parser = argparse.ArgumentParser(
        description="A basic script that prints a greeting.",
        epilog="Example: python app_runner.py --name 'Arsenii'"
    )

    parser.add_argument(
        '--name',
        type=str,
        default='World',
        help='The name to greet. Defaults to "World".'
    )

    args = parser.parse_args()

    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()