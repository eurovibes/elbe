# ELBE - Debian Based Embedded Rootfilesystem Builder
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2013-2017 Linutronix GmbH
# SPDX-FileCopyrightText: 2015 Matthias Buehler <Matthias.Buehler@de.trumpf.com>

from optparse import OptionParser
import sys
import logging

from sqlalchemy.exc import OperationalError

from elbepack.shellhelper import CommandError
from elbepack.elbeproject import ElbeProject
from elbepack.elbexml import ValidationError
from elbepack.db import ElbeDB
from elbepack.cdroms import CDROM_SIZE
from elbepack.log import elbe_logging


def run_command(argv):
    oparser = OptionParser(
        usage="usage: %prog buildchroot [options] <xmlfile>")

    oparser.add_option("-t", "--target", dest="target",
                       help="directoryname of target")

    oparser.add_option("-o", "--output", dest="output",
                       help="name of logfile")

    oparser.add_option("-n", "--name", dest="name",
                       help="name of the project (included in the report)")

    oparser.add_option("--skip-pbuild", action="store_true",
                       dest="skip_pbuild", default=False,
                       help="skip building packages from <pbuilder> list")

    oparser.add_option(
        "--build-bin",
        action="store_true",
        dest="build_bin",
        default=False,
        help="Build Binary Repository CDROM, for exact Reproduction")

    oparser.add_option("--build-sources", action="store_true",
                       dest="build_sources", default=False,
                       help="Build Source CD")

    oparser.add_option("--buildtype", dest="buildtype",
                       help="Override the buildtype")

    oparser.add_option(
        "--cdrom-size",
        action="store",
        dest="cdrom_size",
        default=CDROM_SIZE,
        help="Source ISO CD size in bytes")

    oparser.add_option("--skip-validation", action="store_true",
                       dest="skip_validation", default=False,
                       help="Skip xml schema validation")

    oparser.add_option("--skip-pkglist", action="store_true",
                       dest="skip_pkglist", default=False,
                       help="ignore changes of the package list")

    oparser.add_option("--skip-cdrom", action="store_true",
                       dest="skip_cdrom", default=False,
                       help="(now obsolete) Skip cdrom iso generation")

    (opt, args) = oparser.parse_args(argv)

    if len(args) != 1:
        print("wrong number of arguments")
        oparser.print_help()
        sys.exit(20)

    if not opt.target:
        print("No target specified")
        sys.exit(20)

    if opt.skip_cdrom:
        print("WARNING: Skip CDROMS is now the default, "
              "use --build-bin to build binary CDROM")

    with elbe_logging({"files": opt.output}):
        try:
            project = ElbeProject(opt.target, args[0], opt.name,
                                  opt.buildtype, opt.skip_validation)
        except ValidationError:
            logging.exception("XML validation failed.  Bailing out")
            sys.exit(20)

        try:
            project.build(
                opt.build_bin,
                opt.build_sources,
                opt.cdrom_size,
                opt.skip_pkglist,
                opt.skip_pbuild)
        except CommandError as ce:
            logging.error("Command in project build failed: %s", ce.cmd)
            sys.exit(20)

        try:
            db = ElbeDB()
            db.save_project(project)
        except OperationalError:
            logging.exception("Failed to save project in database")
            sys.exit(20)
