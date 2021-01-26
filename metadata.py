defaults = {}

if node.has_bundle('check_mk_agent'):
    defaults['check_mk'] = {
        'plugins': {
            'mk_apt': {
                'type': 'check_mk_plugin',
                'run_every': 3600,
                'sha256': "d9d9865087b1ae20ba4bd45446db84a96d378c555af687d934886219f31fecb0",
            }
        }
    }
