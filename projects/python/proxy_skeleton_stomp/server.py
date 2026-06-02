from serviceImpl import serviceImpl
import logging

def main():

    logging.basicConfig(
        format = "[SERVER] %(processName)s %(levelname)s %(message)s",
        level = logging.INFO,
        handlers = [logging.StreamHandler()]
    )

    service = serviceImpl()
    service.runSkeleton()

if __name__ == "__main__":
    main()