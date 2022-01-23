from bundlewrap.exceptions import BundleError

defaults = {}

APT_AGENT_VERSIONS = {
    '2.0.0p2': 'de14f88bf8b6668151086ac4a8e156d5eea2315a159d208136dfee24838d2e2c',
    '2.0.0p13': '870d7a622dfc38b98d596b0c6cb110503f363ccaeec80aa0414958415492961c',
}


@metadata_reactor
def add_apt_pkg_to_check_mk(metadata):
    if not node.has_bundle('check_mk_agent'):
        raise DoNotRunAgain

    check_mk_server_version = metadata.get('check_mk/servers_version', None)
    if not check_mk_server_version:
        return {}

    if check_mk_server_version not in APT_AGENT_VERSIONS.keys():
        raise BundleError(f"unsupported Agent version {check_mk_server_version}")

    return {
        'check_mk': {
            'plugins': {
                'mk_apt': {
                    'type': 'check_mk_plugin',
                    'run_every': 3600,
                    'sha256': APT_AGENT_VERSIONS[check_mk_server_version],
                }
            }
        }
    }
