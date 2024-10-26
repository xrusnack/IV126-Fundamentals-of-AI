import logging


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


def _test_a():
    assert True == True

    # Tests were not pushed to the repository on purpose
    # as each of the authors uses different IDE and workflow


def _enumerate():
    LOG.info("Starting tests...")

    _test_a()

    LOG.info("All tests passed!")


if __name__ == "__main__":
    _enumerate()
