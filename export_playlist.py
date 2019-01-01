import sys

# globals
FIRST_NEW_LINE = '#EXTPlayListM3U::M3U\n'
EXPORT_TAG = '.exported'
SMB_PREFIX = 'smb:'
OLD_SEPARATOR = '\\'
NEW_SEPARATOR = '/'
EXT_LEN = 4
SCRIPT_NAME = sys.argv[0]
SCRIPT_COMPLETE_MSG = 'Export of \'%s\' completed successfully.' % sys.argv[1]
ENCODING = 'utf8'
USAGE_MSG = '%s FILE1 ...\nwhere \'FILE1\' ... are M3U playlists to be exported.' % SCRIPT_NAME
NO_ARGS_ERROR = '%s must be called with at least one argument.' % SCRIPT_NAME


def print_error(msg):
    print('error: %s' % msg)


def print_usage():
    print(USAGE_MSG)


def check_args():
    args = sys.argv[1:]
    result = False

    # check for at least one arg
    if not len(args):
        print_error(NO_ARGS_ERROR)
        print_usage()

    else:
        result = True

    return result


def export_playlists(playlists):
    for playlist in playlists:
        export_playlist(playlist)


def export_playlist(playlist):
    with open(playlist, 'rt', encoding=ENCODING) as oldf:
        # last four chars of playlist name assumed to be '.m3u'.
        # new name is '*.exported.m3u'.
        newf_name = playlist[:-EXT_LEN] + EXPORT_TAG + playlist[-EXT_LEN:]
        new_lines = list(oldf.readlines())

        with open(newf_name, 'wt', encoding=ENCODING) as newf:
            # add EXT boilerplate
            newf.write(FIRST_NEW_LINE)

            # main logic for script
            format_new_lines(new_lines)
            newf.writelines(new_lines)


def format_new_lines(new_lines):
    for i in range(len(new_lines)):
        new_lines[i] = SMB_PREFIX + new_lines[i]
        new_lines[i] = new_lines[i].replace(OLD_SEPARATOR, NEW_SEPARATOR)


def print_complete_msg():
    print(SCRIPT_COMPLETE_MSG)


def main():
    if not check_args():
        sys.exit(-1)
    else:
        export_playlists(sys.argv[1:])
        print_complete_msg()
        sys.exit(0)


if __name__ == '__main__':
    main()
