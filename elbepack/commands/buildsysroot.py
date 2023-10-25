# ELBE - Debian Based Embedded Rootfilesystem Builder
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2014-2017 Linutronix GmbH

import logging
from optparse import OptionParser
import sys

from elbepack.elbeproject import ElbeProject
from elbepack.elbexml import ValidationError
from elbepack.log import elbe_logging


def run_command(argv):
    oparser = OptionParser(
        usage="usage: %prog buildsysroot [options] <builddir>")
    oparser.add_option("--skip-validation", action="store_true",
                       dest="skip_validation", default=False,
                       help="Skip xml schema validation")
    oparser.add_option("--buildtype", dest="buildtype",
                       help="Override the buildtype")

    (opt, args) = oparser.parse_args(argv)

    if len(args) != 1:
        print("wrong number of arguments")
        oparser.print_help()
        sys.exit(20)

    with elbe_logging({"streams":sys.stdout}):
        try:
            project = ElbeProject(args[0], override_buildtype=opt.buildtype,
                                  skip_validate=opt.skip_validation)
        except ValidationError:
            logging.exception("XML validation failed.  Bailing out")
            sys.exit(20)

        project.build_sysroot()
