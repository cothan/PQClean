import os
from glob import glob

import pqclean
import helpers


def test_clang_tidy():
    for scheme in pqclean.Scheme.all_schemes():
        for implementation in scheme.implementations:
            if helpers.permit_test('linter', implementation):
                yield check_tidy, implementation


def check_tidy(implementation: pqclean.Implementation):
    helpers.ensure_available('clang-tidy')
    cfiles = glob(os.path.join(implementation.path(), '*.c'))
    common_files = glob(os.path.join('..', 'common', '*.c'))
    helpers.run_subprocess(['clang-tidy',
                    '-quiet',
                    '-header-filter=.*',
                    *cfiles,
                    *common_files,
                    '--',
                    '-iquote', os.path.join('..', 'common'),
                    '-iquote', implementation.path(),
                    ])


if __name__ == "__main__":
    try:
        import nose2
        nose2.main()
    except ImportError:
        import nose
        nose.runmodule()