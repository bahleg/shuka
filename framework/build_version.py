import fnmatch
import os


engine_name = 'SHUKA'
milestone = 'pre-alpha'
version_letter = '1'
very_short_description = 'basic run'


def get_version_string():
    return '{0}:{1}.{2} ({3}).'.format(engine_name, milestone, version_letter, very_short_description)


def get_full_info():
    print 'engine:'+engine_name
    print 'version:'+milestone+'.'+version_letter
    print 'TL;DR:'+very_short_description
    print 'current description:'
    with open('../README.md') as inp:
        print inp.read()
    print 'stats:'
    line_count = 0
    comment_count = 0
    matches = []
    for root, dirnames, filenames in os.walk('..'):
        for filename in fnmatch.filter(filenames, '*.py'):
            matches.append(os.path.join(root, filename))
    for f in matches:
        with open(f) as inp:
            cur_file_code_lines = 0
            comment = False
            for line in inp:
                if len(line.strip())==0:
                    continue
                if line.strip().startswith('#'):
                    comment_count+=1
                    continue
                if line.strip().startswith('"""'):
                    comment=not comment #not True for long string, however mostly can be used
                    continue
                if comment:
                    comment_count+=1
                else:
                    cur_file_code_lines+=1
                    line_count+=1
            print f, cur_file_code_lines
    print 'code lines:', line_count
    print 'comment lines:', comment_count
    print 'total siginificant lines:', line_count+comment_count

if __name__=='__main__':
    get_full_info()