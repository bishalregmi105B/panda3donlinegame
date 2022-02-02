from setuptools import setup

setup(
    name="Ashlya Game",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.py',
                '**/*.wav',
            ],
            'gui_apps': {
                'tester': 'main.py',
            },
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'platforms':['win_amd64']
        }
    }
)
