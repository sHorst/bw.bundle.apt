defaults = {}

if node.has_bundle('check_mk_agent'):
    defaults['check_mk'] = {
        'plugins': {
            'mk_apt': {
                'type': 'check_mk_plugin',
                'run_every': 3600,
                'sha256': "de14f88bf8b6668151086ac4a8e156d5eea2315a159d208136dfee24838d2e2c",
            }
        }
    }
