engine_name = 'SHUKA'
milestone = 'pre-alpha'
version_letter = '1'
very_short_description = 'basic run'


def get_version_string():
    return '{0}:{1}.{2} ({3}).'.format(engine_name, milestone, version_letter, very_short_description)
