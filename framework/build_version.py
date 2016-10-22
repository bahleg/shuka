engine_name = 'SHUKA'
milestone = 'pre-alpha'
version_letter = '0'
very_short_description = 'nothing works'


def get_version_string():
    return '{0}:{1}.{2} ({3}).'.format(engine_name, milestone, version_letter, very_short_description)
