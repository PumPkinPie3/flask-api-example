from app import create_app

application = create_app()


def main():
    application.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
